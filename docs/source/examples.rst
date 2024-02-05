EMPIARreader Examples
=============================

Using the Python interface
--------------------------

For this example, we open the `EMPIAR entry 10943 <https://www.ebi.ac.uk/empiar/EMPIAR-10943/>`_ and load an image dataset from its available directories.

.. code:: python
    from empiarreader import EmpiarSource, EmpiarCatalog

    test_entry = 10943

Every EMPIAR entry has an associated xml file which contains the default order of the directory. This information can be accessed by loading the entry into an EmpiarCatalog.
.. code:: python
    test_catalog = EmpiarCatalog(test_entry)

To get the dataset from the catalog, one would need to specify which directory to load. In this case, there is only one so we choose the key in the position 0.

.. code:: python
    test_catalog_dir = list(test_catalog.keys())[0]
    dataset_from_catalog = test_catalog[test_catalog_dir]

However, the intended target is not always the directory present in the xml. We can further specify the directory to which directory we would like to get the images from.
EMPIARreader can load the dataset from an EmpiarSource, using the EMPIAR entry number and the directory of the images. In this case, we also specify that we want the MRC files from the specified directory.

.. code:: python
    ds = EmpiarSource(
    test_entry,
    directory="data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data",
    filename=".*EER\\.mrc",
    regexp=True,
    )
  
The dataset is loaded lazily (using Dask), so the images are loaded one at a time when ``read_partition`` is called. To choose an image, one can just pick the partition - in this case, it was the partition 10.

.. code:: python
    part = ds.read_partition(10)

This example can be visualised in the `Jupyter Notebook <https://github.com/alan-turing-institute/empiarreader/blob/main/examples/run_empiarreader.ipynb>`_ provided in the repository.

Using the command line interface
--------------------------------

You can use the EMPIARreader CLI to search the EMPIAR archive one directory at a time to find what you are looking for before then downloading those files to disk. First, you will need to choose an EMPIAR entry - in this example `EMPIAR entry 10934 <https://www.ebi.ac.uk/empiar/EMPIAR-10934/>`_ is used. Here we use a glob wildcard (``--select "*"``) to list every subdirectory and file in a readable format:
.. code:: bash
    empiarreader search --entry 10934  --select "*" --verbose

which returns:
.. code::
    Matching path #0: https://ftp.ebi.ac.uk/empiar/world_availability/10934//10934.xml
    Matching path #1: https://ftp.ebi.ac.uk/empiar/world_availability/10934//data/
    Subdirectories are: https://ftp.ebi.ac.uk/empiar/world_availability/10934
    Subdirectories are: https://ftp.ebi.ac.uk/empiar/world_availability/10934//data

We've found the xml containing the metadata for the entry and a subdirectory called `data`. To look inside you can add the `--dir` argument and repeat recursively until you find the directory you are interested in:
.. code:: bash
    empiarreader search --entry 10934  --select "*" --dir "data" --verbose

Once you have found one or more files which you want to download from a directory in the EMPIAR archive you can create a list of URLs using the `--save_search` argument:
.. code:: bash
    empiarreader search --entry 10934  --dir \
    "data/CL44-1_20201106_111915/Images-Disc1/GridSquare_6089277/Data" \
    --select "*gain.tiff.bz2" --save_search saved_search.txt

Using the workflow described above, a user can quickly search and identify datasets that fulfill their criteria. These can then be downloaded using the download utility of the CLI. A user simply needs to specify the file list and a directory to download the files into:
.. code:: bash
    empiarreader download --download saved_search.txt --save_dir new_dir --verbose

