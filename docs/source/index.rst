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
   contributing
   reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
