===================================
Palo Alto Networks Cloud Python SDK
===================================

Python idiomatic SDK for the Palo Alto Networks Cortex™ platform.

The Palo Alto Networks Cloud Python SDK (or `pancloud` for short) was created to assist developers with
programmatically interacting with the Palo Alto Networks Cortex™ platform.

The primary goal is to provide full, low-level API coverage for the following Cortex™ services:

    - Query Service
    - More coming soon!

The secondary goal is to provide coverage, in the form of helpers, for common tasks/operations.

    - Log/event pagination
    - OAuth 2.0 and token refreshing
    - More, coming soon!

* Documentation: https://pancloud.readthedocs.io
* Free software: ISC license

-----

|requests| |pipenv| |pypi| |travis| |docs|

-----

Features
--------

- HTTP client wrapper for the popular Requests library with full access to its features.
- Language bindings for Query Service.
- Helper methods for performing common tasks, such as log/event pagination.
- Support for OAuth 2.0 grant code authorization flow.
- Library of example scripts illustrating how to leverage `pancloud`.
- Support for API Explorer Developer Tokens (Introduced in v1.5.0).

Status
------

The Palo Alto Networks Cloud Python SDK is considered **production/stable** at this time.

Installation
------------

From PyPI::

    $ pip install pancloud==2.0.0a2

Install From GitHub
-------------------

Clone the repo::

    $ git clone https://github.com/PaloAltoNetworks/pancloud.git

Use |pipenv| to install all dependencies and create a virtualenv for your project::

    $ pipenv install

You can specify which python version to use by adding "--two" or "--three"::

    $ pipenv --three install

Activate the pipenv shell::

    $ pipenv shell

Obtaining and Using OAuth 2.0 Tokens
------------------------------------

Work with your Developer Relations representative to register your
application and receive the credentials needed to obtain an `access_token`.
Normally, this requires a `client_id`, `client_secret`, and `refresh_token`.
API Explorer may optionally be used to generate a Developer Token, which can
be used in place of the `client_id`, `client_secret`, and `refresh_token`.

For more information visit the following RTD page: `Credentials <https://pancloud.readthedocs.io/en/latest/guides/credentials.html>`__

Example
-------

.. code-block:: python

    >>> import pancloud
    >>> c = pancloud.Credentials()
    >>> qs = pancloud.QueryService(credentials=c)
    >>> query_params = {
    ...     "query": "SELECT * FROM `587718190.firewall.traffic` LIMIT 1",
    ...     "language": "bigquery"
    ... }
    >>> q = qs.create_query(query_params=query_params)
    >>> q.status_code
    201
    >>> q.json()
    {'jobId': '40fedce6-ddf5-44cf-9af2-7c3d5303f388', 'uri': '/query/v2/jobs/40fedce6-ddf5-44cf-9af2-7c3d5303f388'}
    >>> results = qs.get_job_results(job_id='40fedce6-ddf5-44cf-9af2-7c3d5303f388')
    >>> results.json()
    
Contributors
------------

- Kevin Steves - `github <https://github.com/kevinsteves>`__
- Steven Serrata - `github <https://github.com/sserrata>`__

.. |pypi| image:: https://img.shields.io/pypi/pyversions/pancloud.svg
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
