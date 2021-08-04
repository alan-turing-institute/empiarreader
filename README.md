# EMPIAR Reader
Reader for EMPIAR datasets, using `intake`. Input needed is the EMPIAR number.

## Component Description

`mrcsource` intake driver for mrc files

`starsource` intake driver for star files, to be merged with mrcsource

`empiardirectory` creates the directory for the EMPIAR files

`EMPIARReader` is the class that iterates through the directory and retrieves the files.

## To-Do

- [ ] Merge starsource with mrcsource
- [ ] Create tests
- [ ] Add feature to read particles when present as mrcfiles.
