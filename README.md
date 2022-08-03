# EMPIAR Reader
Reader for [EMPIAR](https://www.ebi.ac.uk/empiar/) datasets, using [intake](https://intake.readthedocs.io/en/latest/). 

The EMPIAR number allows that dataset to be loaded as an EmpiarCatalog.

## Component Description

- EmpiarCatalog (an Intake catalog, representing entries in the EMPIAR catalog)
- EmpiarSource (Intake driver for loading from EMPIAR)
- MrcSource (Intake driver for loading from a file in mrc format)
- StarSource (Intake driver for starfiles)


## To-Do

- [ ] Merge starsource with mrcsource/combine information from starfiles into mrcsource.
- [ ] Add feature to read particles when present as mrcfiles.
