import os
import filecmp

from tests import fixtures


def test_search():
    """Download file list and check same as reference"""
    test_data = os.path.dirname(fixtures.__file__)
    output = "saved_search.txt"
    ref = os.path.join(test_data, output)
    search_cmd = (
        "empiarreader search --entry 10934 --dir"
        " data/CL44-1_20201106_111915/Images-Disc1/GridSquare_6089277/Data"
        f' --select "*gain.tiff.bz2" --save_search {output} --verbose'
    )
    os.system(search_cmd)
    assert filecmp.cmp(ref, output)
    os.remove(output)


def test_download():
    """Download data file and check file is same as reference
    (which is available under a CC0 license from EMPIAR
    https://creativecommons.org/share-your-work/public-domain/cc0/)
    """
    test_data = os.path.dirname(fixtures.__file__)
    output = "10934.xml"
    download_file = os.path.join(test_data, "test_download.txt")
    ref = os.path.join(test_data, output)
    download_cmd = (
        "empiarreader download --save_dir tests"
        f" --download {download_file} --verbose"
    )
    output = os.path.join("tests", output)
    os.system(download_cmd)
    assert filecmp.cmp(ref, output)
    os.remove(output)
