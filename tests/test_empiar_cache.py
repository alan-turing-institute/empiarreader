# flake8: noqa

from unittest.mock import patch
from intake.config import conf

from empiarreader.empiar.empiar import EmpiarCatalog, EmpiarSource

import os
import pytest


# stolen from test_empiar_retrieval.test_empiar
# and adapting to test caching and renamed cache
def test_empiar_cache():
    conf["cache_download_progress"] = True
    conf["cache_dir"] = os.path.join(os.getcwd(), "test_cache_dir")
    for attr in dir(conf):
        print("conf attr {} is {}".format(attr, getattr(conf, attr)))
    print("\n\n")

    # now get all conf dict entries
    for k, v in conf.items():
        print("Key: {} is: {}".format(k, v))
    print("\n\n")

    cat = EmpiarCatalog(10340)
    print(cat)
    print(list(cat))
    print("\n\n")

    ##############################
    # now looking at the EmpiarCatalog.fetch_entry_data
    print(
        "EmpiarCatalog.fetch_entry_data:{}".format(cat.fetch_entry_data(10340))
    )

    # I think cat(alogue) is a list of imagesets
    # So EmpiarCatalogue() starts by grabbing the name of the imagesets by reading them
    # from the online path (EmpiarCatalogue.fetch_entrydata()).
    # This list ??? should be accessible via EmpiarCatalogue.imagesets

    # Now checking after initialisation of EmpiarCatalogue what actually is
    # present in it:
    print("\n\nDir of EmpiarCatalogue.entry_data: {}".format(dir(cat)))
    for thing in dir(cat):
        print("Cat thing {} is {}".format(thing, getattr(cat, thing)))
    print("\n\n")

    # print the args
    for i, entry in enumerate(cat._entries):
        print("Entry {} has {} and is {}".format(i, entry, type(entry)))
        # for j, arg in enumerate(entry.args):
        #    print('Entry {} has arg {} of {}'.format(i, j, arg))

    print("\n\n")

    # partition = cat.read_partition(0)
    # print('Partition: {}'.format(partition))

    # I don't think you re actually using the cache yet as you seem to only have grabbed metadata
    # Try grabbing an actual data file and see what happens... do you use cache?
    ds = cat["Unaligned movies for Case 1"]
    """
    ds = EmpiarSource(
        10340,
        directory="data/Micrographs/Case1",
        filename="FoilHole_21756216_Data_21768957_21768958_20181221_2054-115048.mrc",
        regex=True,
    )
    """

    # now because empiar entry 10340 doesn't play nice, swap to 10943
    ds = EmpiarSource(
        10943,
        directory="data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data",
        filename=".*EER\\.mrc",
        regexp=True,
    )

    ds.read_partition(0)

    assert "Unaligned movies for Case 1" in cat.keys()

    ds = cat["Unaligned movies for Case 1"]

    assert isinstance(ds, EmpiarSource)

    assert ds.directory == "data/Movies/Case1"

    # Note: ds.read() is expensive


def test_empiar_download():
    conf["cache_download_progress"] = True
    conf["cache_dir"] = os.path.join(os.getcwd(), "test_cache_dir")
    # Grab the metadata from MEPIAR entry 10340
    cat = EmpiarCatalog(10340)
    print("Cat start")
    print(cat)
    print(list(cat))
    print("\n\n")
    # Grab the first entry (an EmpiarSource)
    ds = cat[list(cat)[0]]
    print("ds start")
    print("ds type {}".format(type(ds)))
    print(ds)
    # print(list(ds))
    assert isinstance(ds, EmpiarSource)
    assert ds.directory == "data/Movies/Case1"
    print("Imageset EMPIAR index: {}".format(ds.empiar_index))
    print("Imageset directory: {}".format(ds.directory))
    print("Imageset metadata: {}".format(ds.imageset_metadata))
    print("Imageset driver: {}".format(ds._driver))
    print("Imageset image urls: {}".format(ds._image_urls))
    print("Imageset datasource: {}".format(ds._datasource))

    # ds read breaks it http err
    # read_data = ds.read()
    # print(type(read_data))
    # print('Read data: {}'.format(read_data))

    # new
    """
    ds = EmpiarSource(
        10340,
        directory="data/Micrographs/Case1",
        filename="FoilHole_21756216_Data_21768957_21768958_20181221_2054-115048.mrc",
        regex=True,
    )
    part = ds.read_partition(0)
    print("Partition start:")
    print(part)
    print("Filename: {}".format(part.filenmae))

    """
    ds = EmpiarSource(
        10943,
        directory="data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data",
        filename=".*EER\\.mrc",
        regexp=True,
    )

    # Downloads data from first mrc file
    part = ds.read_partition(0)

    assert (
        part.filename
        == "https://ftp.ebi.ac.uk/empiar/world_availability/10943/data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data/FoilHole_11161627_Data_11149751_11149753_20210911_222712_EER.mrc"
    )

    assert part[0][0] == pytest.approx(2.9199, 1.0e-4)


if __name__ == "__main__":
    # test_empiar_cache()
    test_empiar_download()
