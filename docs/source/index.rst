.. EMPIARreader documentation master file, created by
   sphinx-quickstart on Mon Sep 25 10:17:27 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to EMPIARreader's documentation!
==========================

EMPIARReader is a Python package to access any `EMPIAR <https://www.ebi.ac.uk/empiar/>`_ dataset using its entry number. 
EMPIARReader provides utilities to lazily load into a machine-learning-friendly dataset format or to locally download the files. 
The lazy-loading utility allows use of EMPIAR data without the local storage overhead of downloading data permanently. 
The local download functionality is available via a simple command line interface which allows the user to download EMPIAR data without requiring a user account or proprietary software. 
Command line utilities are also provided for searching for files within an EMPIAR entry.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   examples
   contributing
   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


EMPIARreader implementation details
===================================


EMPIARreader API
----------------
EMPIARreader is designed to be as lightweight as possible and easily extendable to other data formats. The API uses `Intake <https://github.com/intake/intake>`_ drivers to allow lazy loading of EMPIAR datasets into a machine learning-compatible format: `xarray <https://github.com/pydata/xarray>`_ for image data and `pandas <https://github.com/pandas-dev/pandas>`_ for metadata.

Furthermore, this is integrated with `Dask <https://www.dask.org>`_, which can load the images as they are needed rather than loading all at once. For large datasets, such as those in cryo-EM, this opens the chance for rapid testing of machine learning methods without needing the local space for entire datasets. This also allows machine learning models to be deployed to the cloud or in clusters without worrying about data management.

While Intake already has drivers for the most common image file types (such as TIFF or JPEG), cryo-EM has field-specific formats that needed to be accommodated as they are present in many datasets. As such, EMPIARreader extends the functionality of Intake for MRC files (an image file format) using the `mrcfile <https://mrcfile.readthedocs.io/en/stable/>`_  package and for STAR files (a metadata file format) using the `starfile <https://github.com/teamtomo/starfile>`_ package.

EMPIARreader CLI
----------------

The EMPIARreader CLI is designed as a simple and platform independent utility for downloading EMPIAR data to disk. In contrast to the other recommended download methods, it does not require proprietary software, a user account, a GUI or a web browser.

The CLI is composed of two utilities which work in tandem: search and download.

The search utility allows the user to browse the EMPIAR archive via the command line. Only one directory can be browsed at a time and files are returned which match user-provided file paths. These may contain glob wildcards or regular expressions. The CLI supports all file/data types. The user can output URLs for the files they have selected to a specified text file. 

The download utility retrieves the files listed in the text file specified via the ```--download``` argument.

This approach is designed to make it easy for users to customise or join files containing URLs before they download them. Downloads may proceed via three different methods depending on the whether they are available. Highest priority is via FTP using `wget <https://gitlab.com/gnuwget/wget>`_, followed by FTP using `curl <https://github.com/curl/curl>`_. If neither are available, the download proceeds via HTTP(S).

