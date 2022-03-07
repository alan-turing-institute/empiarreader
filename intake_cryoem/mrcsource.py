import intake
import xarray
import dask
import io
import mrcfile
import fsspec
from fsspec.core import open_files

import numpy as np


class MrcSource(intake.source.base.DataSource):
    """Simple MRCfile intake driver"""

    container = "xarray"
    name = "mrc"
    version = "0.0.1"
    partition_access = True

    def __init__(self, urlpath, metadata=None):
        super().__init__(metadata=metadata)
        self.dataset = xarray.Dataset()
        self._urlpath = urlpath
        self.current_partition = 0

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
        # return the image data in an xarray container

        # lots more detail here
        # https://mrcfile.readthedocs.io/en/latest/source/mrcfile.html#module-mrcfile.mrcobject

        with self._files[i] as f:

            # if using FTP from EMPIAR, use a bytesIO stream
            if isinstance(f, fsspec.implementations.ftp.FTPFile):
                stream = io.BytesIO(f.read())
            else:
                stream = f

            # use the interpreter so that we can use a byte stream
            with mrcfile.mrcinterpreter.MrcInterpreter(stream, 'r') as mrc:

                if not mrc.is_single_image():
                    raise Exception

                data = mrc.data
                voxel_size = mrc.voxel_size

        # NOTE(arl): this assumes 2d
        ny, nx = data.shape
        coords = {"y": np.arange(ny), "x": np.arange(nx)}

        dims = list(coords.keys())

        attrs = {
            "filename": str(self._files[i].path),
            "voxel_size": voxel_size,
        }

        return xarray.DataArray(data, coords=coords, dims=dims, attrs=attrs)

    def read(self):
        self._load_metadata()
        # should build an xarray dataset by iterating over the partitions
        for i in range(0, self.npartitions):
            self.dataset[i] = self._get_partition(i)
        return xarray.Dataset(self.dataset)

    def _update_current_partition(self, new_partition: int):
        if new_partition is None:
            new_partition = self.current_partition + 1

        if new_partition > self.npartitions:
            self.current_partition = 0
        else:
            self.current_partition = new_partition

    def to_dask(self):
        """Return lazy loaded data"""
        self._load_metadata()
        return dask.delayed(self._get_partition(self.current_partition))

    def _close(self):
        # close any files, sockets, etc
        pass
