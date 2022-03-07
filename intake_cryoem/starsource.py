import intake
import xarray
import dask
import io
import starfile
import fsspec
from fsspec.core import open_files

import numpy as np


class StarSource(intake.source.base.DataSource):
    """Starfile intake driver"""

    container = "xarray"
    name = "starfile"
    version = "0.0.1"
    partition_access = True

    def __init__(self, urlpath, metadata=None):
        super().__init__(metadata=metadata)
        self._urlpath = urlpath

    def _get_schema(self):

        # fsspec should work over ftp also?
        self._files = open_files(self._urlpath)

        return intake.source.base.Schema(
            datashape=None,
            dtype=None,
            shape=(None, None),
            npartitions=len(self._files),
            extra_metadata={},
        )

    def _get_partition(self, i=0):
        with self._files[i] as f:
            # if using FTP from EMPIAR, use a bytesIO stream
            if isinstance(f, fsspec.implementations.ftp.FTPFile):
                stream = io.BytesIO(f.read())
            else:
                stream = f

            data = starfile.read(f, always_dict=True)
            #data = {k: v for k, v in df['particles'].groupby('rlnMicrographName')}
            #data = df['particles'].merge(df['optics'])


        attrs = {
            "filename": str(self._files[i].path),
        }

        return xarray.DataArray(data, attrs=attrs)

    def read(self):
        self._load_metadata()
        for i in range(0, self.npartitions):
            self.dataset[i] = self._get_partition(i)
        return xarray.Dataset(self.dataset)
