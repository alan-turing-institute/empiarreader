import pytest

from empiarreader.empiar.empiar import EmpiarCatalog, EmpiarSource


def test_empiar():
    cat = EmpiarCatalog(10340)

    assert "Unaligned movies for Case 1" in cat.keys()

    ds = cat["Unaligned movies for Case 1"]

    assert isinstance(ds, EmpiarSource)

    assert ds.directory == "data/Movies/Case1"

    # Note: ds.read() is expensive


def test_empiar_filename_pattern():
    """Check that the 'filename' argument of EmpiarSource returns
    data from an mrc file in a directory containing several types of file.
    """
    ds = EmpiarSource(
        10943,
        directory=(
            "data/MotionCorr/job003/Tiff/EER/Images-Disc1/"
            + "GridSquare_11149061/Data"
        ),
        filename=".*EER\\.mrc",
        regexp=True,
    )

    # Downloads data from first mrc file
    part = ds.read_partition(0)

    assert (
        part.filename
        == "https://ftp.ebi.ac.uk/empiar/world_availability/10943/data/"
        + "MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data/"
        + "FoilHole_11161627_Data_11149751_11149753_20210911_222712_EER.mrc"
    )

    assert part[0][0] == pytest.approx(2.9199, 1.0e-4)
