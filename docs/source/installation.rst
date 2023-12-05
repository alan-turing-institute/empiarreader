.. _installation-instructions:

Installation instructions
=========================

Installing EMPIARReader from PyPI
---------------------------------

This is recommended for most users.

.. code:: bash

   pip install empiarreader
   
If you want to install the latest version, use:

.. code:: bash

   pip install git+https://github.com/alan-turing-institute/empiarreader/

Installing EMPIARreader with Poetry (for developers)
----------------------------------------------------

This project uses `Poetry <https://python-poetry.org/>`_ for
dependency management and packaging.

.. code:: bash
   git clone https://github.com/alan-turing-institute/empiarreader/
Use ``cd empiarreader`` to change to the ``empiarreader`` directory. Then install via poetry:
.. code:: bash
   poetry install