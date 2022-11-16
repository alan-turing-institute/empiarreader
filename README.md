<div align="center">
    <h1>EMPIAR Reader</h1>
</div>


Reader for any [EMPIAR](https://www.ebi.ac.uk/empiar/) dataset, using [intake](https://intake.readthedocs.io/en/latest/). 

The EMPIAR number allows that dataset to be loaded as an EmpiarCatalog.

## Installation

For easier installation and dependency handling, EMPIAR reader is packaged with [Poetry](https://python-poetry.org)

```
git clone https://github.com/alan-turing-institute/empiarreader/
cd empiarreader
poetry install
```

Otherwise, installation can be done with:

```
pip install git+https://github.com/alan-turing-institute/empiarreader/
```

## Usage

To retrieve a dataset from an Empiar entry, use the following code:

```
from intake_cryoem.empiar import EmpiarSource

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
