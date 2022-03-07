import intake
import pandas as pd
import starfile


def test_load_star():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    starfile.write(df, "tmp.star", overwrite=True)

    ds = intake.open_star("tmp.star")

    ds_read = ds.read()
    df_read = (
        ds_read.sel(frame=0).isel(file=0).to_dataframe().drop(columns=["frame", "file"])
    )

    assert df.equals(df_read)


def test_load_remote_star():
    ds = intake.open_star(
        "https://github.com/alisterburt/starfile/blob/master/tests/data/one_loop.star?raw=true"
    )
    data = ds.read()
