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
    >>> ls = pancloud.LoggingService(credentials=c)
    >>> query = {
    ...     "query": "SELECT * FROM panw.traffic LIMIT 1",
    ...     "startTime": 1938869090,
    ...     "endTime": 1938869150,
    ...     "maxWaitTime": 10000  
    ... }
    >>> q = ls.query(query)
    >>> q.status_code
    200
    >>> q.json()
    {u'result': {u'esQuery': {u'table': [u'panw.traffic'], u'selections': [], u'params': {}, u'query': {u'aggregations': {}, u'size': 1}}, u'esResult': {u'hits': {u'hits': [{u'_score': 2, u'_type': u'traffic', u'_id': u'117270018_lcaas:0:9379670:1', u'_source': {u'logset': u'LCaaS', u'traffic_flags': 0, u'parent_start_time': 0, u'inbound_if': u'ethernet1/1', u'dstloc': u'10.0.0.0-10.255.255.255', u'natdport': 0, u'time_generated': 1560175638, u'recsize': 1958, u'chunks_sent': 0, u'to': u'l3-untrust', u'non-standard-dport': 0, u'receive_time': 1560175660, u'elapsed': 0, u'seqno': 51422235, u'pbf_s2c': 0, u'vsys': u'vsys1', u'bytes': 196, u'subtype': u'end', u'subcategory-of-app': u'internet-utility', u'vsys_id': 1, u'actionflags': -9223372036854776000L, u'pkts_sent': 1, u'sport': 0, u'is-saas-of-app': 0, u'category': u'any', u'ui-srcloc': u'Singapore', u'bytes_received': 98, u'container': 0, u'dst': u'10.10.0.2', u'customer-id': u'117270018', u'packet_capture': 0, u'srcloc': u'SG', u'natsport': 0, u'parent_session_id': 0, u'proxy': 0, u'ui-dstloc': u'10.0.0.0-10.255.255.255', u'src': u'203.208.197.133', u'config_ver': 2304, u'sanctioned-state-of-app': 0, u'fwd': 1, u'technology-of-app': u'network-protocol', u'bytes_sent': 98, u'chunks_received': 0, u'dg_hier_level_3': 0, u'dg_hier_level_2': 0, u'dg_hier_level_1': 16, u'dg_hier_level_4': 0, u'repeatcnt': 1, u'natsrc': u'0.0.0.0', u'app': u'ping', u'characteristic-of-app': [u'tunnel-other-application', u'prone-to-misuse', u'is-saas'], u'chunks': 0, u'non_std_dport': 1, u'decrypt_mirror': 0, u'action_source': u'from-policy', u'from': u'l3-untrust', u'url_denied': 0, u'assoc_id': 0, u'log_feat_bit1': 0, u'start': 1560175625, u'cloud_hostname': u'ngfw-1', u'pbf_c2s': 0, u'sym_return': 0, u'captive_portal': 0, u'outbound_if': u'ethernet1/1', u'tunnelid_imsi': 0, u'sessionid': 407532, u'category-of-app': u'general-internet', u'tunnel': u'N/A', u'type': u'traffic', u'mptcp_on': 0, u'recon_excluded': 0, u'http2_connection': 0, u'tunnel_inspected': 0, u'risk-of-app': u'2', u'serial': u'007200000046172', u'is_fwaas': 0, u'proto': u'icmp', u'is_phishing': 0, u'is_gpaas': 0, u'nat': 0, u'tunneled-app': u'untunneled', u'natdst': u'0.0.0.0', u'time_received': 1560175638, u'users': u'203.208.197.133', u'rule_uuid': u'd6992de4-5523-4ba8-b9e9-a99fe9dbfda4', u'pkts_received': 1, u'action': u'allow', u'is_dup_log': 0, u'exported': 0, u'session_end_reason': u'aged-out', u'transaction': 0, u'packets': 2, u'flag': 0, u'rule': u'intrazone-default', u'device_name': u'ngfw-1', u'flags': 1048676, u'dport': 0}, u'_index': u'117270018_panw.all_2019060600-2019062600_000000'}], u'total': 22942, u'maxScore': 2}, u'from': 0, u'completed': True, u'took': 185, u'timed_out': False, u'state': u'COMPLETED', u'id': u'e2a685ce-0b21-41d6-a050-4e371e456817', u'size': 1}}, u'sequenceNo': 0, u'queryId': u'e2a685ce-0b21-41d6-a050-4e371e456817', u'clientParameters': {}, u'queryStatus': u'JOB_FINISHED'}
    
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
