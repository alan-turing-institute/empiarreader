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

Cryogenic electron microscopy (cryo-EM) [@cryoem-drug-review; @cryoem-challenges] is an imaging technique used to obtain the structure of objects of near-atomic scales experimentally via transmission electron microscopy of cryogenically frozen samples. Deep learning-based image processing approaches have been applied to many steps of the cryo-EM reconstruction workflow [cite (https://europepmc.org/article/MED/36013446)]]. Many of the resulting algorithms have been widely adopted as they enable quicker processing or improved interpretation of the data. Deep learning-based approaches require large amounts of data to train the algorithms. The Electron Microscopy Public Image Archive (EMPIAR) [@empiar] is a public resource for the raw image data collected by cryo-EM experiments and facilitates access to this data for methods development and validation. It has been vital for developing the existing cryo-EM deep-learning algorithms, however as datasets can have hundreds of files and sizes on the order of terabytes or hundreds of gigabytes, downloading and managing these datasets can become a barrier to the development of deep-learning methods. Additionally, the currently recommended tools to download data from EMPIAR either use proprietary software, require a user account or necessitate a web-browser.
To address this we have developed EMPIARReader, an open source tool which provides a Python API to allow lazy loading of EMPIAR datasets into a machine learning-compatible format using intake drivers [@intake]. It parses EMPIAR metadata, uses the mrcfile library [@mrcfile] to interpret MRC files, supports common image file formats and uses the starfile library [@starfile] to interpret STAR files. To our knowledge, there are no other tools to effectively make use of EMPIAR in a dynamic manner for data intensive tasks such as machine-learning. EMPIARReader additionally provides a simple, lightweight CLI which allows users to search and download EMPIAR entries using glob patterns or regular expressions and then download files via FTP or HTTP.
EMPIARReader is easily installed in a python environment via pip or poetry and has been released as a pypi package ([EmpiarReader](https://pypi.org/project/empiarreader/)).

# Statement of need

In cryo-EM, the diffraction of the electron beam by the electrostatic potential of the molecules in the sample is recorded in the images captured by the detector. 
Due to advancements in hardware and software since 2013, the resolution achievable via cryo-EM reconstruction rivals that possible through x-ray crystallography [cite https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4409662/], with cryoEM being the preferable technique for determining the conformations of many macromolecules [cite https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4913480/]. The effectiveness of cryoEM has been recognised with the awarding of the 2017 Nobel prize in chemistry to pioneers of the method [cite Nobel 2017]. 
The images which make up cryo-EM datasets commonly have a very low resolution and a low signal to noise ratio (SNR) germane to minimisation of radiation damage induced disorder. Consequently, the structures are obtained by averaging through thousands of examples of the structures in the samples, which translates into a very large dataset per experiment.
Raw image datasets are deposited into the online public image archive, EMPIAR [@empiar]. There is a loose structure to follow, but generally each deposited dataset has a different internal organisation of folders. With over 1300 entries and >3PB of data hosted, EMPIAR has become an important resource for the structural biology community, amassing over 700 citations in published works. 

Deep learning-based artifical intelligence has developed significantly in recent years and a number of algorithms have been developed for use in cryo-EM data processing. Deep-learning has been applied to the particle picking, 3D classification, postprocessing and model building stages of the reconstruction pipeline (add citations). (NOTE THE CHALLENGES WHICH THESE ADDRESS SUCH AS PREFERENTIAL ORIENTTATION/DATASET SIZE IN PICKING AND CONFORMATIONAL/COMPOSITINAL HETEROGENEITY IN 3D RECONSTRUCTION!). Datasets from EMPIAR have been used extensively for training and validating cryo-EM related deep learning algorithms. To make optimal use of the archive it is essential that the datasets are easily accessible and their size does not hinder accessibility.

The current recommended methods to download data from EMPIAR are via:

1. the IBM Aspera Connect web interface [@aspera-connect]
2. the IBM Aspera command line interface [@aspera-cli]
3. Globus [@globus-1; @globus-2]
4. http or ftp from the entry web page using an internet browser [@empiar]

These methods all require that data is downloaded and persisted before use and offer limited configurability and automation in data selection and access. In contrast, EMPIARReader allows data and metadata to be downloaded in a persistent or dynamic manner (through lazy loading). The granularity of downloads can be configured from an entire EMPIAR entry down to individual files and is easily automated.

This makes EMPIARReader flexible enough to handle tasks from downloading a single file to downloading custom subsets of data from different EMPIAR entries. This can be additionally configured to not require the downloaded data to be stored on local disk which, in principle, allows any user to make use of the entire data archive without any storage overheads. It is envisioned that this utility will be particularly useful for the training of ML models and allow improved generalisation by allowing fast and lightweight access to diverse training data. 

EMPIARReader is easily installed in a python environment via pip or poetry and has been released as a pypi package ([EmpiarReader](https://pypi.org/project/empiarreader/)). It benefits from an BSD 3-clause license and can be utilised either from a CLI or via a python API.

(add something more about web browser based methods not being possible on many compute machine/clusters? And that aspera cli and globus require either proprietary software or a user account (respectively)? wheras we are good to go, you just need python/pip)

(would be great to add current projects/organisations using it!)

(add documentation details)

(mention jpternotebook)

(contact kyle morris)

# EMPIARReader implementation details

API

how intake works (catalogue, etc)

libraries used (mrc/star)

file types supported

CLI

glob or regular expressions (navigation)

output HTTP paths to file

download from a simple carrage return delimited list of http paths via
FTP (wget or curl) or failing that HTTP (urllib)

# Example
API from notebook

CLI from README

# Figures

# Acknowledgements
Need to figure out correct way to attribute Ada Lovelace centre funding and potentially ATI funding for previous work - JG

# References