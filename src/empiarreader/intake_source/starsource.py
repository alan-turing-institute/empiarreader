import intake
import starfile
from fsspec.core import open_files


class StarSource(intake.source.base.DataSource):
    """Intake driver for starfiles as DataSource.

    Args:
        urlpath: URL for the starfile.
    """

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
            # starfile.read must be given a filename
            with tempfile.NamedTemporaryFile(suffix=".star") as tmp:
                tmp.file.write(f.read())
                tmp.file.flush()
                dfs = starfile.read(tmp.name, always_dict=True)

        attrs = {
            "filename": str(self._files[i].path),
        }

        try:
            ds = xr.concat(
                (df.to_xarray() for key, df in dfs.items()),
                dim=pd.RangeIndex(len(dfs), name="frame"),
                data_vars="all",
            )
        except ValueError:
            ds = xr.Dataset({"index": ("index", []), "frame": ("frame", [])})

        return ds.assign_attrs(attrs)

    def read(self):
        import xarray as xr

        self._load_metadata()

        dfs = [self._get_partition(i) for i in range(0, self.npartitions)]

        data = xr.combine_by_coords(dfs, combine_attrs="drop")

        filenames = [df.filename for df in dfs]

        return data.assign({"filename": ("partition", filenames)})
