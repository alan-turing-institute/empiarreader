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

Cryogenic electron microscopy (cryo-EM) [@cryoem-drug-review; @cryoem-challenges] is an imaging technique used to obtain the structure of objects of near-atomic scales experimentally via transmission electron microscopy of cryogenically frozen samples. Deep learning-based image processing approaches have been applied to many steps of the cryo-EM reconstruction workflow [@ai-in-cryoem]. Many of the resulting algorithms have been widely adopted as they enable quicker processing or improved interpretation of the data. Deep learning-based approaches require large amounts of data to train the algorithms. The Electron Microscopy Public Image Archive (EMPIAR) [@empiar] is a public resource for the raw image data collected by cryo-EM experiments and facilitates access to this data for methods development and validation. It has been vital for developing the existing cryo-EM deep-learning algorithms, however as datasets can have hundreds of files and sizes on the order of terabytes or hundreds of gigabytes, downloading and managing these datasets can become a barrier to the development of deep-learning methods. Additionally, the currently recommended tools to download data from EMPIAR either use proprietary software, require a user account or necessitate a web-browser.
To address this we have developed EMPIARReader, an open source tool which provides a Python API to allow lazy loading of EMPIAR datasets into a machine learning-compatible format using intake drivers [@intake]. It parses EMPIAR metadata, uses the mrcfile library [@mrcfile] to interpret MRC files, supports common image file formats and uses the starfile library [@starfile] to interpret STAR files. To our knowledge, there are no other tools to effectively make use of EMPIAR in a dynamic manner for data intensive tasks such as machine-learning. EMPIARReader additionally provides a simple, lightweight CLI which allows users to search and download EMPIAR entries using glob patterns or regular expressions and then download files via FTP or HTTP.
EMPIARReader is easily installed in a python environment via pip or poetry and has been released as a pypi package ([EmpiarReader](https://pypi.org/project/empiarreader/)).

# Statement of need

In cryo-EM, the diffraction of the electron beam by the electrostatic potential of the molecules in the sample is recorded in the images captured by the detector. 
Due to advancements in hardware and software since 2013, the resolution achievable via cryo-EM reconstruction rivals that possible through x-ray crystallography [@cryoem-resolution], with cryoEM being the preferable technique for determining the conformations of many macromolecules [@cryoem-development]. The effectiveness of cryoEM has been recognised with the awarding of the 2017 Nobel prize in chemistry to pioneers of the method.  
The images which make up cryo-EM datasets commonly have a very low resolution and a low signal to noise ratio (SNR) germane to minimisation of radiation damage induced disorder. Consequently, the structures are obtained by averaging through thousands of examples of the structures in the samples, which translates into a very large dataset per experiment.
Raw image datasets are deposited into the online public image archive, EMPIAR [@empiar]. There is a loose structure to follow, but generally each deposited dataset has a different internal organisation of folders. With over 1300 entries and >3PB of data hosted, EMPIAR has become an important resource for the structural biology community, amassing over 700 citations in published works. 

Deep learning-based artifical intelligence has developed significantly in recent years [@dl-development] and a number of algorithms have been developed for use in cryo-EM data processing. Deep-learning has been applied to the particle picking [@topaz; @cryolo], 3D classification [@cryodrgn; @3dflex], postprocessing [@deepemhancer] and model building [@jamali2023automated; @backbonepred] stages of the reconstruction pipeline among many more examples [@ai-in-cryoem]. Datasets from EMPIAR have been used extensively for training and validating cryo-EM related deep learning algorithms, particularly for those which rely on raw image data. To make optimal use of the archive it is essential that the datasets are easily accessible and their size does not hinder accessibility or algorithm performance.

The current recommended methods to download data from EMPIAR are via:

1. the IBM Aspera Connect web interface [@aspera-connect]
2. the IBM Aspera command line interface [@aspera-cli]
3. Globus [@globus-1; @globus-2]
4. http or ftp from the entry web page using an internet browser [@empiar]

These methods all require that data is downloaded and persisted before use and offer limited configurability and automation in data selection and access. In contrast, EMPIARReader allows data and metadata to be downloaded in a dynamic manner through lazy loading whilst also providing a simple interface for downloading EMPIAR files persistently to disk if required. Additionally, the only prerequisites for EMPIARReader are Python 3 and either pypi or poetry for installation.

With EMPIARReader, the granularity of downloads can be configured from an entire EMPIAR entry down to individual files and is easily automated. This makes EMPIARReader flexible enough to handle tasks from downloading a single file to downloading custom subsets of data from different EMPIAR entries. In principle, EMPIARReader allows any user to make use of the entire data archive without any storage overheads. It is envisioned that this utility will be particularly useful for the training of ML models and allow improved algorithmic performance by allowing fast and lightweight access to diverse training data. To see how to use the EMPIARReader API and CLI please refer to the [examples](#example) or the [jupyter notebook](https://github.com/alan-turing-institute/empiarreader/blob/main/examples/run_empiarreader.ipynb) accessible on the EMPIARReader github page. EMPIARReader documentation can otherwise be found [here](https://github.com/alan-turing-institute/empiarreader/tree/main) REPLACE WITH SHPIX LOCATION.

EMPIARReader is easily installed in a python environment via pip or poetry and has been released as a pypi package ([EmpiarReader](https://pypi.org/project/empiarreader/)). It benefits from an BSD 3-clause license and can be utilised either from a CLI or via a python API. It is currently in active use by researchers at the Alan Turing Institute and the STFC Scientific Computing Department.

(contact kyle morris)

# EMPIARReader implementation details

## EMPIARReader API
EMPIARReader is designed to be as lightweight as possible and easily extendable to other data formats. The API uses intake drivers [@intake] to allow lazy loading of EMPIAR datasets into a machine learning-compatible format. 

how intake works (catalogue, etc)

libraries used (mrc/star)

file types supported - star, mrc, tif, png?, jpeg?, etc?

## EMPIARReader CLI

The EMPIARReader CLI is designed as a simple and platform independent utility for downloading EMPIAR data to disk. Unlike the API, it does not support lazy loading and is not intended to. In contrast to the other recommended download methods, it does not require proprietary software, a user account, a GUI or an internet browser.

The EMPIARReader CLI allows the user to browse the EMPIAR archive via the command line using glob wildcards or regular expressions and supports all file/data types. Only one directory can be browsed at a time. The user can specify a file to output HTTP file paths for the files they have selected to a text file. To download all files in this file, the user simply needs to pass the CLI the file path and the `--download` argument as well .

If the user wishes to download files from multiple directories to a single location or make alterations they could alter this file manually.  

glob or regular expressions (navigation)

output HTTP paths to file

download from a simple carrage return delimited list of http paths via
FTP (wget or curl) or failing that HTTP (urllib)

# Example

## API Example
API from notebook

## CLI Example
CLI from README

# Figures

# Acknowledgements
Need to figure out correct way to attribute Ada Lovelace centre funding and potentially ATI funding for previous work - JG

# References