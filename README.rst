===================================
Palo Alto Networks Cloud Python SDK
===================================

Python idiomatic SDK for the Palo Alto Networks Application Framework.

The Palo Alto Networks Cloud Python SDK, or `pancloud`, was created to assist developers with
programmatically interacting with the Palo Alto Networks Application Framework.

The primary goal is to provide full, low-level API coverage for the following Application Framework services:

    - Logging Service
    - Directory Sync Service
    - Event Service

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
- Language bindings for Logging Service, Event Service and Directory-Sync Service.
- Helper methods for performing common tasks, such as log/event pagination.
- Credentials support for OAuth 2.0.
- Library of example scripts illustrating how to leverage `pancloud`.

Status
------

The Palo Alto Networks Cloud Python SDK is considered **beta** at this time.

Installation
------------

From PyPI::

    $ pip install pancloud

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
application to receive the credentials needed to obtain an `access_token`.
You'll need a `client_id`, `client_secret`, and `refresh_token`.
`API Explorer <https://github.com/PaloAltoNetworks/apiexplorer>`__ may optionally be used to perform
OAuth 2.0 and fetch tokens.

For more information visit the following RTD page::

https://pancloud.readthedocs.io/en/latest/guides/credentials.html

Example
-------

The following example assumes valid credentials are present::

    $ ./logging_query.py

    QUERY: {"queryId":"59801207-9a75-49c1-9f87-a2aa23f55774","sequenceNo":0,"queryStatus":"RUNNING","clientParameters":{},"result":{"esResult":null,"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":1},"selections":[],"params":{}}}}

    JOB_FINISHED: queryId: 59801207-9a75-49c1-9f87-a2aa23f55774, sequenceNo: 0, retrieving from 0, size: 1, took: 117 ms

    RESULT: {"queryId":"59801207-9a75-49c1-9f87-a2aa23f55774","sequenceNo":0,"queryStatus":"JOB_FINISHED","clientParameters":{},"result":{"esResult":{"took":117,"hits":{"total":1878954,"maxScore":2,"hits":[{"_index":"117270009_panw.all_2018042400-2018062300_000000","_type":"traffic","_id":"117270009_lcaas:0:149314:0","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":14882,"natsport":53295,"sessionid":806912,"type":"traffic","parent_start_time":0,"packets":30,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1622,"from":"L3-Trust","parent_session_id":0,"repeatcnt":1,"app":"web-browsing","vsys":"vsys1","nat":1,"technology-of-app":"browser-based","pkts_received":17,"chunks_sent":0,"receive_time":1524893357,"non-standard-dport":443,"subcategory-of-app":"internet-utility","chunks_received":0,"users":"panwdomain\\user1","srcuser":"panwdomain\\user1","proxy":1,"fwd":1,"config_ver":2049,"cloud_hostname":"sample-cft-fw","customer-id":"117270009","proto":"tcp","non_std_dport":1,"tunneled-app":"tunneled-app","is-saas-of-app":0,"natdport":443,"action_source":"from-policy","assoc_id":0,"dst":"66.135.212.201","natdst":"66.135.212.201","chunks":0,"flags":22020208,"rule":"Allow Outbound Browsing","dport":443,"elapsed":0,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/2","device_name":"sample-cft-fw","subtype":"end","time_received":1524893357,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-fin","natsrc":"10.0.0.100","seqno":1633879,"src":"10.0.1.101","start":1524893341,"time_generated":1524893357,"outbound_if":"ethernet1/1","category-of-app":"general-internet","bytes_sent":2152,"srcloc":"10.0.0.0-10.255.255.255","pkts_sent":13,"dstloc":"US","serial":"","bytes":17034,"vsys_id":1,"to":"L3-Untrust","category":"10006","sport":33562,"tunnel":0}}]},"id":"59801207-9a75-49c1-9f87-a2aa23f55774","from":0,"size":1,"completed":true,"state":"COMPLETED","timed_out":false},"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":1},"selections":[],"params":{}}}}

    DELETE: {"success":true}

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
