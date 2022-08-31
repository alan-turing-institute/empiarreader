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

An example of usage of this package can be found in: 

[Object Detection in CryoEM Datasets](https://github.com/scivision-gallery/cryoEM-object-detection) - with scivision

## Component Description

- EmpiarCatalog (an Intake catalog, representing entries in the EMPIAR catalog)
- EmpiarSource (Intake driver for loading from EMPIAR)
- MrcSource (Intake driver for loading from a file in mrc format)
- StarSource (Intake driver for starfiles)


## To-Do

Please check Issues.
