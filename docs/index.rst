.. pancloud documentation master file, created by
   sphinx-quickstart on Mon Mar 26 09:03:37 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pancloud
====================================

.. _installation:

Release v\ |version|. (:ref:`Installation <installation>`)

Welcome to `pancloud's` documentation - the python idiomatic SDK for the Palo Alto Networks Application Framework!

The Palo Alto Networks Cloud Python SDK (or `pancloud`) was created to assist 3rd-party developers with
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

|requests| |pipenv| |pypi| |travis| |docs|

Overview (readme)
-----------------

.. toctree::
   :maxdepth: 2

   readme

User Guide
----------

Instructions for how to leverage `pancloud` in your Application Framework developer projects.

.. toctree::
   :maxdepth: 2

   guides/quickstart
   installation
   history
   contributing

API
---
.. toctree::
   :maxdepth: 2

   source/pancloud

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. |pypi| image:: https://img.shields.io/pypi/v/pancloud.svg
        :target: https://pypi.python.org/pypi/pancloud

.. |travis| image:: https://img.shields.io/travis/PaloAltoNetworks/pancloud.svg
        :target: https://travis-ci.org/PaloAltoNetworks/pancloud

.. |docs| image:: https://readthedocs.org/projects/pancloud/badge/?version=latest
        :target: https://pancloud.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. |requests| image:: https://img.shields.io/badge/docs-requests-blue.svg
    :target: http://docs.python-requests.org/en/master
    :alt: Documentation Status

.. |pipenv| image:: https://img.shields.io/badge/docs-pipenv-green.svg
    :target: https://docs.pipenv.org
    :alt: Documentation Status
