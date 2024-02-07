---
title: 'EMPIARreader: A Python package interface to EMPIAR'
tags:
  - Python
  - cryoEM
  - cryoET
  - data retrieval
authors:
  - name: Beatriz Costa-Gomes
    equal-contrib: true
    corresponding: true
    affiliation: 1
  - name: Oliver Strickson
    equal-contrib: true 
    affiliation: 1
  - name: Joel Greer
    equal-contrib: true
    affiliation: 2
  - name: Alan R. Lowe
    corresponding: true
    affiliation: 1,3
     
affiliations:
 - name: The Alan Turing Institute, London, England, NW1 2DB, United Kingdom
   index: 1
 - name: Scientific Computing Department, Science and Technology Facilities Council, Research Complex at Harwell, Didcot, OX11 0FA, United Kingdom
   index: 2
 - name: University College London, UK
   index: 3
date:  2024
bibliography: paper.bib

---


# Summary

Cryogenic electron microscopy (cryo-EM) [@cryoem-drug-review; @cryoem-challenges] is an imaging technique used to obtain the structure of biomolecular objects at near-atomic scales experimentally via transmission electron microscopy of cryogenically frozen samples. The Electron Microscopy Public Image Archive (EMPIAR) [@empiar] is a public resource for the raw image data collected by cryo-EM experiments and facilitates free access to this data, allowing it to be used for methods development and validation. Deep learning-based image processing approaches have been applied to many steps of the cryo-EM reconstruction workflow [@ai-in-cryoem]. Many of the resulting algorithms have been widely adopted as they enable quicker processing and/or improved interpretation of the data. Deep learning-based approaches require large amounts of data to train the algorithms. However, as datasets can have hundreds of files and sizes on the order of terabytes or hundreds of gigabytes, downloading and managing these datasets can become a barrier to the development of deep-learning methods. Additionally, the currently recommended tools to download data from EMPIAR either use proprietary software, require a user account or necessitate a web browser.
To address this and to provide a way to integrate EMPIAR data into machine learning codebases, we have developed EMPIARreader. This is an open source tool which provides a Python library to allow lazy loading of EMPIAR datasets into a machine learning-compatible format. It parses EMPIAR metadata, uses the mrcfile library [@mrcfile] to interpret MRC files, supports common image file formats and uses the starfile library [@starfile] to interpret STAR files. To our knowledge, there are no other tools to effectively make use of EMPIAR in a dynamic manner for data intensive tasks such as machine learning. EMPIARreader additionally provides a simple, lightweight command line interface (CLI) which allows users to search and download EMPIAR entries using glob patterns or regular expressions and then download files via FTP or HTTP(S).
EMPIARreader is easily installed in a Python environment via the standard Python package management tools pip and Poetry and has been released as a PyPI [@pypi] package ([EMPIARreader](https://pypi.org/project/empiarreader/)).

# Statement of need

In cryo-EM, the scattering of the electron beam by the electrostatic potential of the molecules in the sample is recorded in the images captured by the detector. 
Due to advancements in hardware and software since 2013, the resolution achievable via cryo-EM reconstruction rivals that possible through x-ray crystallography [@cryoem-resolution], with cryo-EM being the preferable technique for determining the conformations of many macromolecules [@cryoem-development].
The images which make up cryo-EM datasets commonly have a very low signal to noise ratio (SNR) germane to minimisation of radiation damage induced disorder. Consequently, the structures are obtained by averaging through thousands of examples of the structures in the samples, which necessitates a very large dataset per experiment.
Raw image datasets can be deposited into the online public image archive, EMPIAR [@empiar]. There is a loose structure to follow, but generally each deposited dataset is structured according to the needs or preferences of the depositing user with no particular directory structure enforced. With over 1300 entries and >3PB of data hosted, EMPIAR has become an important resource for the structural biology community, amassing over 700 citations in published works. 

Deep-learning-based methods have developed significantly in recent years [@dl-development] and a number of algorithms have been developed for use in cryo-EM data processing. Deep-learning has been applied to stages of the image processing and reconstruction pipeline, including particle picking [@topaz; @cryolo], 3D classification and dynamics [@cryodrgn; @3dflex; @dynamight] and model building [@jamali2023automated; @backbonepred] among many more examples [@ai-in-cryoem]. Datasets from EMPIAR have been used extensively for training and validating cryo-EM related deep learning algorithms, particularly for those which rely on raw image data. To make optimal use of the archive it is essential that the datasets are easily accessible and their size does not hinder accessibility or algorithm performance.

The current recommended methods to download data from EMPIAR are via:

1. the IBM Aspera Connect web interface [@aspera-connect]
2. the IBM Aspera command line interface [@aspera-cli]
3. Globus [@globus-1; @globus-2]
4. HTTP(S) or FTP from the entry web page using an internet browser [@empiar]

These methods all require that data is downloaded and persisted before use and offer limited configurability and automation in data selection and access. In contrast, EMPIARreader allows data and metadata to be downloaded in a dynamic manner through lazy loading whilst also providing a simple interface for downloading EMPIAR files persistently to disk if required. Additionally, the only prerequisites for EMPIARreader are Python 3 and either pip [@pip] or Poetry [@poetry] for installation.

EMPIARreader allows the granularity of downloads to be configured from an entire EMPIAR entry down to individual files. This makes EMPIARreader flexible enough to handle tasks from downloading a single file to downloading custom subsets of data from different EMPIAR entries. In principle, EMPIARreader allows any user to make use of the entire data archive without utilising local disk storage resources. It is envisioned that this utility will be particularly useful for the training of ML models and allow improved algorithmic performance by allowing fast and lightweight access to diverse training data. To see examples of the EMPIARreader API and CLI please refer to the [examples](#example) or the [Jupyter Notebook](https://github.com/alan-turing-institute/empiarreader/blob/main/examples/run_empiarreader.ipynb) accessible on the EMPIARreader github page. EMPIARreader documentation can otherwise be found [here](https://empiarreader.readthedocs.io/en/latest/).


# Licensing and userbase
EMPIARreader is offered under a BSD 3-clause license and can be utilised either from a CLI or via a Python library. It is currently in active use by researchers at the Alan Turing Institute and STFC Scientific Computing Department.

# Acknowledgements

This work was supported by Wave 1 of The UKRI Strategic Priorities Fund under the EPSRC Grant EP/W006022/1, particularly the “AI for Science” theme within that grant & The Alan Turing Institute.

Joel Greer would like to acknowledge support from the Ada Lovelace Centre for this work.

The authors are grateful to Dr. Tom Burnley (Scientific Computing Department, Science and Technology Facilities Council, Research Complex at Harwell) for his advice and discussions regarding EMPIARreader.

# References
