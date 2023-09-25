import os
import filecmp

from tests import fixtures


def test_search():
    """Download file list and check same as reference"""
    # reference file
    test_data = os.path.dirname(fixtures.__file__)
    textfile = "saved_search.txt"
    ref = os.path.join(test_data, textfile)

    # the output file
    output = os.path.join("tests", textfile)

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
    # reference version of file
    test_data = os.path.dirname(fixtures.__file__)
    xmlfile = "10934.xml"
    ref = os.path.join(test_data, xmlfile)

    download_file = os.path.join(test_data, "test_download.txt")
    download_cmd = (
        "empiarreader download --save_dir tests"
        f" --download {download_file} --verbose"
    )
    os.system(download_cmd)

    # this is the downloaded file
    output = os.path.join("tests", xmlfile)
    assert filecmp.cmp(ref, output)
    os.remove(output)
