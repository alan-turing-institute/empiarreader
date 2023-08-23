---
title: 'EMPIARreader: A Python package interface to the EMPIAR archive'
tags:
  - Python
  - cryoEM
  - cryoET
  - data retrieval
authors:
  - name: Beatriz Costa-Gomes
    equal-contrib: true
    affiliation: 1
  - name: Oliver Strickson
    equal-contrib: true 
    affiliation: 1
  - name: Joel Greer
    affiliation: 2
  - name: Alan Lowe
    affiliation: 1
    
#corresponding: true 
affiliations:
 - name: The Alan Turing Institute, UK
   index: 1
 - name: Scientific Computing Department, Science and Technology Facilities Council, Research Complex at Harwell, Didcot, OX11 0FA, England
   index: 2
date:  2023
bibliography: paper.bib
# We use the ieee csl for citation style by Rintze M. Zelle, et al unaltered and
# under the CC BY-SA 3.0 license https://creativecommons.org/licenses/by-sa/3.0/
csl: https://github.com/citation-style-language/styles/blob/795ad0c77258cb7e01f3413123b5b556b4cb6a98/ieee.csl
---


# Summary

Cryogenic electron microscopy [@cryoem-drug-review; @cryoem-challenges] is an imaging technique used to obtain the structure of objects of near-atomic scales experimentally via transmission electron microscopy of cryogenically frozen samples. The diffraction of the electron beam by the electrostatic potential of the molecules in the sample is recorded in the images captured by the detector. These images commonly have a very low resolution and a low signal to noise ratio (SNR) germane to minimisation of radiation damage induced disorder. Consequently, the structures are obtained by averaging through thousands of examples of the structures in the samples, which translates into a very large dataset per experiment.

Raw image datasets are deposited into the online public image archive, EMPIAR [@empiar]. There is a loose structure to follow, but generally each deposited dataset has a different internal organisation of folders. The currently recommended tools to download from EMPIAR either use proprietary software, require a user account or necessitate a web-browser. Furthermore, there are no tools to effectively make use of the archive in a dynamic manner for data intensive tasks such as machine-learning.

EMPIARReader is an open source tool which provides a Python API to allow lazy loading of EMPIAR datasets into a machine learning-compatible format using intake drivers [@intake]. It parses EMPIAR metadata, uses the mrcfile library [@mrcfile] to interpret image data and uses the starfile library [@starfile] to interpret STAR files. It additionally provides a simple, lightweight CLI which allows users to search EMPIAR entries with glob patterns or regular expressions and download files over HTTP. (CHECK INTERNAL METHOD USES HTTP)

# Statement of need

With over 1300 entries and >3PB of data hosted, EMPIAR has become an important resource for the structural biology community, amassing over 700 citations in published works. To make optimal use of the archive it is essential that the datasets are easily accessible and their size does not hinder accessibility.

The current recommended methods to download data from EMPIAR are via:

1. the IBM Aspera Connect web interface [@aspera-connect]
2. the IBM Aspera command line interface [@aspera-cli]
3. Globus [@globus-1; @globus-2]
4. http or ftp from the entry web page using an internet browser [@empiar]

These methods all require that data is downloaded and persisted before use and offer limited configurability and automation in data selection and access. In contrast, EMPIARReader allows data and metadata to be downloaded in a persistent or dynamic manner. The granularity of downloads can be configured from an entire EMPIAR entry down to individual files and is easily automated.

This makes EMPIARReader flexible enough to handle tasks from downloading a single file to downloading custom subsets of data from different EMPIAR entries. This can be additionally configured to not require the downloaded data to be stored on local disk which, in principle, allows any user to make use of the entire data archive without any storage overheads. It is envisioned that this utility will be particularly useful for the training of ML models and allow improved generalisation by allowing fast and lightweight access to diverse training data.

EMPIARReader is easily installed in a python environment via pip or poetry and has been released as a pypi package ([EmpiarReader](https://pypi.org/project/empiarreader/)). It benefits from an BSD 3-clause license and can be utilised either from a CLI or via a python API.

(would be great to add current projects/organisations using it!)


# Figures

# Acknowledgements

# References