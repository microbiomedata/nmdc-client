NMDC Client Documentation
=================================

NMDC Client is a Python package for interacting with selected endpoints of the `NMDC Runtime API <https://api.microbiomedata.org/docs>`_.
It supports querying public NMDC metadata and, for authorized users, working with privileged submission and staging endpoints.

NMDC Client is published on PyPI as ``nmdc-client`` and imported in Python as ``nmdc_client``.

.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   usage
   filters
   example_usage

API Reference
=============

Public and privileged APIs are documented separately. Most will want to start with public search classes.
Privileged API classes are for users with submission and staging permissions and are not needed for general querying of public metadata.

.. toctree::
   :maxdepth: 1
   :caption: Public API Reference:

   functions
   public_subclasses

.. toctree::
   :maxdepth: 1
   :caption: Privileged API Reference:

   privileged_api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
