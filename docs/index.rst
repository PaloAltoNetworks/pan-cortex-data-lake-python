.. pancloud documentation master file, created by
   sphinx-quickstart on Mon Mar 26 09:03:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pancloud
========

.. _installation:

Release v\ |version|. (:ref:`Installation <installation>`)

====================================
Welcome to pancloud's documentation!
====================================

The Palo Alto Networks Cloud Python SDK, or ``pancloud``, was created to assist 3rd-party developers with
programmatically interacting with the various APIs implemented by the Palo Alto Networks Application Framework.
The primary goal is to provide full, low-level API coverage for the following Application Framework services:

    - Logging Service
    - Directory Sync Service
    - Event Service

The secondary goal is to provide coverage, in the form of helpers, for common tasks/operations.

    - Log pagination
    - OAuth and token refreshing
    - Response validation
    - Log schema enforcement
    - More, coming soon.

* Free software: ISC license

User Guide
----------

Instructions for how to leverage ``pancloud`` in your Application Framework developer projects.

.. toctree::
   :maxdepth: 2

   guides/quickstart
   guides/credentials
   installation
   history
   contributing

API Reference
-------------
.. toctree::
   :maxdepth: 2

   source/pancloud

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
