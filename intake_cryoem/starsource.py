import intake
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
        self._files = open_files(self._urlpath)

        return intake.source.base.Schema(
            datashape=None,
            dtype=None,
            shape=(None, None),
            npartitions=len(self._files),
            extra_metadata={},
        )

    def _get_partition(self, i=0):
        import tempfile
        import xarray as xr
        import pandas as pd

        with self._files[i] as f:
            # starfile must be given a filename
            with tempfile.NamedTemporaryFile(suffix=".star") as tmp:
                tmp.file.write(f.read())
                tmp.file.flush()
                dfs = starfile.read(tmp.name, always_dict=True)

        attrs = {
            "filename": str(self._files[i].path),
        }

        ds = xr.concat(
            [df.to_xarray() for key, df in dfs.items()],
            dim=pd.Index(range(len(dfs)), name="frame"),
            data_vars="all",
        )

        return xr.Dataset(ds, attrs=attrs)

    def read(self):
        import xarray as xr
        import pandas as pd

        self._load_metadata()

        dfs = [self._get_partition(i) for i in range(0, self.npartitions)]

        return xr.Dataset(
            xr.concat(
                dfs,
                dim=pd.Index([df.filename for df in dfs], name="file"),
                data_vars="all",
            ),
            attrs={},
        )
