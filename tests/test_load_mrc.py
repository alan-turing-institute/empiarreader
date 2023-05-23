import intake
import numpy as np
import mrcfile


def test_load_mrc():
    data = np.arange(9, dtype="float32").reshape((3, 3))

    with mrcfile.new("tests/fixtures/tmp.mrc", overwrite=True) as example_mrc:
        example_mrc.set_data(data)

    ds = intake.open_mrc("tests/fixtures/tmp.mrc")

    data_read = ds.read()
    
    assert (data_read.sel(partition=0).raster.to_numpy() == data).all()


def test_load_remote_mrc():
    ds = intake.open_mrc(
        "https://github.com/ccpem/mrcfile/blob/master/tests/test_data/epu2.9_example.mrc?raw=true"
    )
    data = ds.read()
