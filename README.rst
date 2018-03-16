====================
Palo Alto Networks Cloud Python SDK
====================

Python idiomatic SDK for the Palo Alto Networks Application Framework.

The Palo Alto Networks Cloud Python SDK was created to assist 3rd-party developers programmatically interact
with the various APIs implemented by the Palo Alto Networks Application Framework. The primary goal
is to provide full, low-level API coverage for the following services:

    - Logging Service
    - Directory Sync Service
    - Event Service

The secondary goal is to provide coverage, in the form of helper methods, for common high-level tasks/operations.

* Overview: https://github.com/PaloAltoNetworks/pancloud
* Documentation: https://pancloud.readthedocs.io
* Free software: ISC license

-----

|requests| |pipenv| |pypi| |travis| |docs| |updates|

-----

Features
--------

- HTTP client wrapper for the popular Requests library with full access to its features.
- Language bindings for Logging Service, Event Service and Directory-Sync Service.
- Helper methods for performing common tasks, such as log/event pagination.
- Credentials support for OAuth2 tokens.
- Library of example scripts illustrating how to leverage the library.
- Library of sample JSON responses to common Logging Service queries.

Status
------

The Palo Alto Networks Cloud Python SDK is considered **beta** at this time.

Installation
------------

The easiest method to install the Palo Alto Networks Cloud Python SDK is to clone the repo to your dev machine::

    $ git clone https://github.com/PaloAltoNetworks/pancloud.git

Use |pipenv| to install all dependencies and create a virtualenv for your project::

    $ pipenv install

You can specify which python version to use by adding "--two" or "--three" to pipenv install or shell arguments::

    $ pipenv --three install

Enter a pipenv shell::

    $ pipenv shell

Example
--------------

To run the provided example scripts you'll first need to acquire a `client_id`, `client_secret`, `instanceId` and a registered `redirect_uri`. These items are necessary to perform OAuth and retrieve tokens.

The following example assumes an ACCESS_TOKEN environment variable has been exported::

    $ ./logging_query.py

    QUERY: {"queryId":"356a1975-18d5-4566-8c63-760b721644fa","pageNumber":0,"status":"RUNNING","clientParams":{},"result":{"esResult":null,"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":1}}}}

    JOB_FINISHED: queryId: 356a1975-18d5-4566-8c63-760b721644fa, pageNumber: 0, retrieving from 0, size: 1, took: 141 ms

    RESULT: {"queryId":"356a1975-18d5-4566-8c63-760b721644fa","pageNumber":0,"status":"JOB_FINISHED","clientParams":{},"result":{"esResult":{"took":141,"hits":{"total":51493,"maxScore":2,"hits":[{"_index":"117270002_panw.all_2018022000-2018022100_000000","_type":"traffic","_id":"117270002_lcaas:1:2722:0","_score":2,"_source":{"risk-of-app":"1","logset":"LGS-lfp","bytes_received":60,"natsport":0,"sessionid":7700,"type":0,"parent_start_time":0,"packets":2,"dg_hier_level_4":0,"dg_hier_level_1":14,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":0,"recsize":1390,"from":"VM-Trust","parent_session_id":0,"vsys_name":"foo","repeatcnt":1,"app":"incomplete","vsys":"vsys1","technology-of-app":"unknown","pkts_received":1,"receive_time":1519137271,"non-standard-dport":0,"subcategory-of-app":"unknown","users":"10.1.1.1","fwd":1,"config_ver":1,"cloud_hostname":"Aristotle","customer-id":"117270002","proto":6,"tunneled-app":"untunneled","is-saas-of-app":0,"natdport":0,"action_source":1,"dst":"00000000000000000000ffff0a01012c","natdst":"00000000000000000000ffff00000000","flags":108,"rule":"any-any","dport":1514,"elapsed":0,"sanctioned-state-of-app":0,"inbound_if":1108118339584,"device_name":"Aristotle","subtype":1,"time_received":1519137252,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":7,"natsrc":"00000000000000000000ffff00000000","seqno":23057060,"src":"00000000000000000000ffff0a010101","start":1519137247,"time_generated":1519137252,"outbound_if":1108118339584,"category-of-app":"unknown","bytes_sent":74,"srcloc":"10.0.0.0-10.255.255.255","pkts_sent":1,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":134,"vsys_id":1,"to":"VM-Trust","category":"0","sport":60127,"tunnel":0}}]},"id":"356a1975-18d5-4566-8c63-760b721644fa","from":0,"size":1,"completed":true,"state":"COMPLETED","timed_out":false},"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":1}}}}

    DELETE: {"ok":true}

Contributors
------------

- Kevin Steves - `github <https://github.com/kevinsteves>`__
- Steven Serrata - `github <https://github.com/sserrata>`__

.. |pypi| image:: https://img.shields.io/pypi/v/pancloud.svg
        :target: https://pypi.python.org/pypi/pancloud

.. |travis| image:: https://img.shields.io/travis/sserrata/pancloud.svg
        :target: https://travis-ci.org/PaloAltoNetworks/pancloud

.. |docs| image:: https://readthedocs.org/projects/pancloud/badge/?version=latest
        :target: https://pancloud.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. |updates| image:: https://pyup.io/repos/github/sserrata/pancloud/shield.svg
     :target: https://pyup.io/repos/github/sserrata/pancloud/
     :alt: Updates

.. |requests| image:: https://img.shields.io/badge/docs-requests-blue.svg
    :target: http://docs.python-requests.org/en/master
    :alt: Documentation Status

.. |pipenv| image:: https://img.shields.io/badge/docs-pipenv-green.svg
    :target: https://docs.pipenv.org
    :alt: Documentation Status
