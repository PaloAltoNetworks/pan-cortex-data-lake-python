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

The Palo Alto Networks Cloud Python SDK, or ``pancloud``, was created to assist developers with
programmatically interacting with the Palo Alto Networks Application Framework.

The primary goal is to provide full, low-level API coverage for the following Application Framework services:

    - Logging Service
    - Directory Sync Service
    - Event Service

The secondary goal is to provide coverage, in the form of helpers, for common tasks/operations.

    - Log/event pagination
    - OAuth 2.0 and token refreshing
    - More, coming soon.

* Free software: ISC license

The User Guide
--------------

Instructions for how to get started using ``pancloud`` and some additional
background on how ``Credentials`` works. You'll also find a few blurbs on how
to install and contribute to ``pancloud``, as well as the version history.

.. toctree::
   :maxdepth: 2

   guides/quickstart
   guides/credentials
   installation
   history
   contributing

The API Reference Guide
-----------------------

Explore ``pancloud's`` API to learn more about the various classes, methods,
modules and functions you can leverage in your developer projects.

.. toctree::
   :maxdepth: 2

   source/pancloud

Indices and Tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
