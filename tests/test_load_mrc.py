import os
import intake
import numpy as np
import mrcfile


def test_load_mrc():
    data = np.arange(9, dtype="float32").reshape((3, 3))

    tmp_mrc = "tests/tmp.mrc"
    with mrcfile.new(tmp_mrc, overwrite=True) as example_mrc:
        example_mrc.set_data(data)

    ds = intake.open_mrc(tmp_mrc)

    data_read = ds.read()

    assert (data_read.sel(partition=0).raster.to_numpy() == data).all()
    os.remove(tmp_mrc)


def test_load_remote_mrc():
    ds = intake.open_mrc(
        "https://github.com/ccpem/mrcfile/blob/master/tests/test_data/"
        + "epu2.9_example.mrc?raw=true"
    )
    ds.read()
