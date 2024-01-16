import re

import requests
import fnmatch

from urllib.parse import urlparse
from pathlib import Path
from intake.source.base import Schema, DataSource
from intake.catalog.base import Catalog
from intake.catalog.local import LocalCatalogEntry
from bs4 import BeautifulSoup

from empiarreader.intake_source.mrcsource import MrcSource
from empiarreader.intake_source.starsource import StarSource


class EmpiarCatalog(Catalog):
    """Catalog for the EMPIAR entries

    Args:
        empiar_index: Index for the dataset in the archive.
    """

    name = "empiar_catalog"

    _empiar_url_api_base = "https://www.ebi.ac.uk/empiar/api"

    def __init__(self, empiar_index, metadata=None, **kwargs):
        self.empiar_index = empiar_index

        super().__init__(name=self.name, metadata=metadata, **kwargs)

    @classmethod
    def fetch_entry_data(cls, empiar_index):
        """Requests the data from the entry according to the EMPIAR index."""
        req = requests.get(f"{cls._empiar_url_api_base}/entry/{empiar_index}")
        entry_data = list(req.json().values())[0]
        return entry_data

    def _load(self):
        """Loads the dataset metadata after fetching the online information."""
        entry_data = self.fetch_entry_data(self.empiar_index)

        imagesets = entry_data["imagesets"]

        # TODO load other metadata

        for imageset in imagesets:
            self._entries[imageset["name"]] = LocalCatalogEntry(
                name=imageset["name"],
                description=imageset["details"],
                driver=EmpiarSource,
                catalog=self,
                args={
                    "empiar_index": self.empiar_index,
                    "directory": imageset["directory"],
                    "imageset_metadata": imageset,
                },
            )


class EmpiarSource(DataSource):
    """General EMPIAR intake driver, as DataSource.

    Args:
        empiar_index: EMPIAR entry number
        directory: directory for the relevant files, within the EMPIAR entry
        driver: type of intake driver needed for the data (mrc, starfile or ...
                any image)
        filename: [Optional] Name for a specific file to download
        regexp: [Optional] Name for a specific file type to download
        imageset_metadata: [Optional] Metadata relative to the specific ...
                            imageset needed
        metadata: [Optional] Metadata relative to the entry
        storage_options: [Optional] Option to save the data, or cache

    """

    name = "empiar"
    container = "xarray"
    version = "0.0.1"
    partition_access = True

    _empiar_url_ftp_over_https_base = (
        "https://ftp.ebi.ac.uk/empiar/world_availability"
    )

    _drivers = {
        "mrc": MrcSource,
        "mrcs": MrcSource,
        "star": StarSource,
    }

    def __init__(
        self,
        empiar_index,
        directory,
        driver=None,
        filename=None,
        regexp=False,
        imageset_metadata=None,
        metadata=None,
        storage_options=None,
    ):
        super().__init__(metadata=metadata)

        self.empiar_index = empiar_index
        self.directory = directory
        self.image_url_regexp = None
        if filename and regexp:
            self.image_url_regexp = re.compile(filename)
        elif filename:
            self.image_url_regexp = re.compile(fnmatch.translate(filename))

        self.imageset_metadata = imageset_metadata

        self._driver = driver

        self._image_urls = None
        self._datasource = None

    @property
    def data_directory_url(self):
        """Retrieve the current selected data directory for the dataset."""
        return (
            f"{self._empiar_url_ftp_over_https_base}/"
            + f"{self.empiar_index}/{self.directory}"
        )

    def _parse_data_dir(self, data_dir_url):
        soup = BeautifulSoup(requests.get(data_dir_url).text, "html.parser")

        all_links = [
            data_dir_url + "/" + a["href"]
            for a in soup.find_all("a")
            if "../" not in a
        ]

        return all_links

    def _get_driver(self, data_format):
        from intake_xarray import ImageSource

        return self._drivers.get(data_format.lower(), ImageSource)

    def _get_schema(self):
        if self._image_urls is None:
            all_urls = self._parse_data_dir(self.data_directory_url)
            if self.image_url_regexp:
                self._image_urls = [
                    url for url in all_urls if self.image_url_regexp.match(url)
                ]
            else:
                self._image_urls = all_urls

        try:
            if self.imageset_metadata is None:
                entry_data = EmpiarCatalog.fetch_entry_data(self.empiar_index)
                self.imageset_metadata = next(
                    imageset
                    for imageset in entry_data["imagesets"]
                    if imageset["directory"] == self.directory
                )

            npartitions, frames, h, w = (
                int(self.imageset_metadata[k])
                for k in [
                    "num_images_or_tilt_series",
                    "frames_per_image",
                    "image_height",
                    "image_width",
                ]
            )
            if self._driver is None:
                self._driver = self._get_driver(
                    self.imageset_metadata["data_format"]
                )

        # Given directory was not included in the EMPIAR metadata
        except StopIteration:
            self.imageset_metadata = {}

            npartitions = len(self._image_urls)
            frames = None
            h = None
            w = None

            if self._driver is None:
                one_image_url_path = urlparse(self._image_urls[0]).path
                one_image_url_ext = Path(one_image_url_path).suffix.replace(
                    ".", ""
                )
                self._driver = self._get_driver(one_image_url_ext)

        self._schema = Schema(
            dtype=None,
            shape=(frames, h, w, 1),
            npartitions=npartitions,
            extra_metadata=self.metadata,
        )

        if self._datasource is None:
            self._datasource = self._driver(urlpath=self._image_urls)

        return self._schema

    def read(self):
        """Reads the DataSource according to the metadata."""
        self._load_metadata()

        return self._datasource.read()

    def read_partition(self, i):
        """ " Reads an individual element of the dataset.

        Args:
            i (int): Position of the element in the dataset"""
        self._load_metadata()

        return self._datasource.read_partition(i)

    def to_dask(self):
        """Lazily read the DataSource according to the metadata, using Dask."""
        self._load_metadata()

        return self._datasource.to_dask()
