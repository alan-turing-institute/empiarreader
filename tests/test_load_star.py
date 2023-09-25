import os
import intake
import pandas as pd
import starfile


def test_load_star():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})

    tmp_star = "tests/tmp.star"

    starfile.write(df, tmp_star, overwrite=True)

    ds = intake.open_star(tmp_star)

    ds_read = ds.read()
    df_read = (
        ds_read.sel(frame=0, partition=0)
        .to_dataframe()
        .drop(columns=["filename", "frame"])
    )
    assert df.equals(df_read)
    os.remove(tmp_star)


def test_load_remote_star():
    ds = intake.open_star(
        "https://github.com/alisterburt/starfile/blob/master/tests/data/"
        + "one_loop.star?raw=true"
    )
    ds.read()
