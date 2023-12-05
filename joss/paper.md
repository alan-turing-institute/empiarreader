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

# EMPIARReader implementation details

## EMPIARReader API
EMPIARReader is designed to be as lightweight as possible and easily extendable to other data formats. The API uses intake drivers [@intake] to allow lazy loading of EMPIAR datasets into a machine learning-compatible format. 

Intake is a package that allows for easier access of online data. Furthermore, it works with Dask [@dask], which can load the images as they are needed, without downloading them locally. For large datasets, as are the ones in CryoEM, this opens the chance for rapid testing of machine learning methods without needing the local space for the data. This also allows machine learning models to be deployed to the cloud or in clusters without worrying about data management.

While intake already has drivers for the most common image file types (such as TIFF or JPEG), cryoEM has field-specific formats that needed to be adapted as they are present in many datasets. As such, EMPIARReader has the DataSource for both mrc files (image file, using the mrcfile [@mrcfile] package) and star files (location of the particles, i.e., position information for each individual images, using the starfile [@starfile] package).

## EMPIARReader CLI

The EMPIARReader CLI is designed as a simple and platform independent utility for downloading EMPIAR data to disk. Unlike the API, it does not support lazy loading and is not intended to. In contrast to the other recommended download methods, it does not require proprietary software, a user account, a GUI or an internet browser.

The CLI is composed of two utilities which work in tandem: search and download.

The search utility allows the user to browse the EMPIAR archive via the command line. Only one directory can be browsed at a time and files are returned which match user-provided filepaths. These may contain glob wildcards or regular expressions. The CLI supports all file/data types. The user can specify a file to output HTTP file paths for the files they have selected to a text file. 

To download all files written to the text file, the user can use the download utility. They simply need to pass the CLI the file path via the `--download` argument as well a directory to save the files into.

This approach is designed to make it easy for users to customise or join files containing HTTP file paths before they download them. Downloads may proceed via 3 different methods depending on the whether they are available. Highest priority is via FTP using wget [@wget] utility, followed by FTP using curl [@curl]. If neither are available, the download proceeds via HTTP.

# Example

## API Example

For this example, we open the EMPIAR entry 10943, and load an image dataset from its available directories.

```
from empiarreader import EmpiarSource, EmpiarCatalog
import matplotlib.pyplot as plt 

test_entry = 10943
```

Every EMPIAR entry has an associated xml file which contains the default order of the directory. If that's the data the user would like to access, they can just load the entry onto an EmpiarCatalog.
```
test_catalog = EmpiarCatalog(test_entry)
```

To get the dataset from the catalog, one would need to specify which directory to load. In this case, there is only one so we choose the key in the position 0.

```
test_catalog_dir = list(test_catalog.keys())[0]

dataset_from_catalog = test_catalog[test_catalog_dir]

```

However, not always the directory present in the xml is the intended target. We can further specify the directory to which folder we would like to get the images from.
EMPIARreader can load the dataset from an EmpiarSource, using the entry number and the directory of the images. In this case, we also specify that we want the mrc files from the specified folder.

```
ds = EmpiarSource(
        test_entry,
        directory="data/MotionCorr/job003/Tiff/EER/Images-Disc1/GridSquare_11149061/Data",
        filename=".*EER\\.mrc",
        regexp=True,
    )
```
  
The dataset is loaded lazily (using dask), so the images are loaded one at a time when read_partition is called. To choose an image, one can just pick the partition - in this case, it was the partition 10.

```
part = ds.read_partition(10)
```

This example can be visualised in the notebook `examples/run_empiarreader.ipynb` provided in the repository.

## CLI Example

You can use the EMPIARReader CLI to search the EMPIAR archive one directory at a time to find what you are looking for before then downloading those files to disk. First, you will need to choose an EMPIAR entry. Here we use a glob wildcard (`--select`) to list every subdirectory and file in a readable format:
```
empiarreader search --entry 10934  --select "*" --verbose
```
which returns:
```
Matching path #0: https://ftp.ebi.ac.uk/empiar/world_availability/10934//10934.xml
Matching path #1: https://ftp.ebi.ac.uk/empiar/world_availability/10934//data/
Subdirectories are: https://ftp.ebi.ac.uk/empiar/world_availability/10934
Subdirectories are: https://ftp.ebi.ac.uk/empiar/world_availability/10934//data
```

We've found the xml containing the metadata for the entry and a subdirectory called `data`. To look inside you can add the `--dir` argument and repeat recursively until you find the directory you are interested in:
```
empiarreader search --entry 10934  --select "*" --dir "data" --verbose
```

Once you have found one or more files which you want to download from a directory in the EMPIAR archive you can create a list of HTTPS file paths using the `--save_search` argument:
```
empiarreader search --entry 10934  --dir "data/CL44-1_20201106_111915/Images-Disc1/GridSquare_6089277/Data" --select "*gain.tiff.bz2" --save_search saved_search.txt
```

You've now searched for the files you want, identified them and created a list of them. You can download them using the download utility of the CLI. You'll simply need to specify your file list and a directory to download the files into:
```
empiarreader download --download saved_search.txt --save_dir new_dir --verbose
```

# Acknowledgements
Need to figure out correct way to attribute Ada Lovelace centre funding and potentially ATI funding for previous work - JG

# References
