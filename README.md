<div align="center">
    <h1>EMPIAR Reader</h1>
</div>


Reader for any [EMPIAR](https://www.ebi.ac.uk/empiar/) dataset, using [intake](https://intake.readthedocs.io/en/latest/). 

The EMPIAR entry number allows that dataset to be loaded as an EmpiarCatalog.

## Installation

### For Users
EMPIARReader can be installed as a [pypi package](https://pypi.org/project/empiarreader/) using Python >=3.8 via:
```
pip install empiarreader
```

Otherwise, installation can be done with:

```
pip install git+https://github.com/alan-turing-institute/empiarreader/
```

### For Developers

For easier installation and dependency handling, EMPIAR reader is packaged with [Poetry](https://python-poetry.org)

```
git clone https://github.com/alan-turing-institute/empiarreader/
cd empiarreader
poetry install
```

## Usage
EMPIARReader has a command line interface (CLI) and an application programming interface (API). The command line interface can be used to search the EMPIAR archive and to download files from the archive. The API can be used to lazily load EMPIAR datasets into a machine learning compatible format.

### EMPIARReader CLI

#### Search EMPIAR Entry For Files
To search a particular entry in the EMPIAR archive for files, the `empiarreader search` utility can be used:
```
empiarreader search --entry 10934  --select "*"
```
where `--entry` is the EMPIAR entry number, `--select` is the path to use to search for files in this EMPIAR entry (which supports bash-style wildcards). Please enclose this string in quotation marks (`""`).

Once you know the directory you want to search, you can provide the `--dir` argument, for example:
```
empiarreader search --entry 10934  --dir "data" --select "*"
```
To save the file paths output by the search in a text file the `--save_search` argument can be supplied:
```
empiarreader search --entry 10934  --dir "data/CL44-1_20201106_111915/Images-Disc1/GridSquare_6089277/Data" --select "*fractions.tiff.bz2" --save_search saved_search.txt
```
It is possible to use regex instead of bash-style wildcards to specify files using the `--regex` argument. To increase the interpretability of the terminal output you can use the `--verbose` argument. This numbers the matching files and separates files from subdirectories.
#### Download EMPIAR Files
To download files, first save a list of files to download with the `empiarreader search` utility. For example,
```
empiarreader search --entry 10934  --dir "data/CL44-1_20201106_111915/Images-Disc1/GridSquare_6089277/Data" --select "*gain.tiff.bz2" --save_search saved_search.txt
```
This will contain file paths from a given directory of the EMPIAR entry. You can then download these entries (currently via HTTPS) to a local directory with:


### EMPIARReader API

Data from `.star` format metadata files and `.mrc` format image files are currently supported for lazy loading into a machine learning compatible format via EMPIARReader.

To retrieve a dataset from an Empiar entry, use the following code:

```
from empiarreader import EmpiarSource

dataset = EmpiarSource(
            number,
            directory=directory,
            filename_regexp=pattern,
        )
```

where number is the entry number, directory is the folder path and filename_regexp the file pattern with which to search. For example, if the user wants only the mrc files from the entry number 10943 from a certain folder, the code would be:

```
ds = EmpiarSource(
            10943,
            directory="data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149304/Data",
            filename_regexp=".*EER\\.mrc",
        )
```

An example of usage of this package can be found in: 

[Object Detection in CryoEM Datasets](https://github.com/scivision-gallery/cryoEM-object-detection) - with scivision


## Component Description

- EmpiarCatalog (an Intake catalog, representing entries in the EMPIAR catalog)
- EmpiarSource (Intake driver for loading from EMPIAR)
- MrcSource (Intake driver for loading from a file in mrc format)
- StarSource (Intake driver for starfiles)


## To-Do

Please check Issues.
