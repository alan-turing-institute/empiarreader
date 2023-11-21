import xarray as xr
import pandas as pd
import io
import mrcfile

import numpy as np

from intake.source.base import DataSource, Schema

from fsspec.core import open_files


class MrcSource(DataSource):
    """Intake driver for mrcfiles as DataSource.

    Args:
        urlpath: URL for the mrcfile.
    """

    container = "xarray"
    name = "mrc"
    version = "0.0.1"
    partition_access = True

    def __init__(self, urlpath, metadata=None):
        super().__init__(metadata=metadata)
        self._ds = None
        self._urlpath = urlpath
        self.current_partition = 0

    def _get_schema(self):
        self._files = open_files(self._urlpath)

        # TODO Attempt to load one file (for its shape)

        self._schema = Schema(
            datashape=None,
            dtype=None,
            shape=None,
            npartitions=len(self._files),
            extra_metadata={},
        )

        return self._schema

    def _get_partition(self, i=0):
        # return the image data in an xarray container

        # lots more detail here
        # https://mrcfile.readthedocs.io/en/latest/source/mrcfile.html#module-mrcfile.mrcobject
        with self._files[i] as f:
            f_bytes = io.BytesIO(f.read())
            filename = str(f.path)

            # use the interpreter so that we can use a byte stream
            with mrcfile.mrcinterpreter.MrcInterpreter(f_bytes) as mrc:
                data = mrc.data
                voxel_size = mrc.voxel_size

        if len(data.shape) == 2:
            ny, nx = data.shape
            coords = {
                "y": np.arange(ny),
                "x": np.arange(nx),
            }

        else:
            nframe, ny, nx = data.shape
            coords = {
                "frame": np.arange(nframe),
                "y": np.arange(ny),
                "x": np.arange(nx),
            }

        dims = list(coords.keys())

        attrs = {
            "filename": filename,
            "voxel_size": voxel_size,
        }

        return xr.DataArray(data, coords=coords, dims=dims, attrs=attrs)

    def read(self):
        self._load_metadata()
        self._ds = self.to_dask().load()

        return self._ds

    def to_dask(self):
        self._load_metadata()

        if self._ds is not None:
            return self._ds

        # TODO: lazy loading

        dfs = [self._get_partition(i) for i in range(self.npartitions)]

        filenames = [df.filename for df in dfs]
        raster = xr.concat(
            dfs, dim=pd.RangeIndex(len(dfs), name="partition"), data_vars="all"
        )

        self._ds = xr.Dataset(
            {"raster": raster, "filename": ("partition", filenames)}, attrs={}
        )

        return self._ds

    def _close(self):
        self._ds = None
