.. _quickstart:

Quickstart
==========

This page should give a good indication of how to get started with ``pancloud``.

First off, ensure ``pancloud`` is :ref:`installed <installation>` and :ref:`up-to-date <installation>`.

Let's start with a basic example.

.. note::

    Example below assumes a credentials.json file has been properly :ref:`generated <credentials>`

Querying Logging Service
------------------------

Begin by importing :class:`~pancloud.logging.LoggingService` and :class:`~pancloud.credentials.Credentials`:

.. code:: python

    from pancloud import LoggingService
    from pancloud import Credentials

Next, let's construct a :class:`~pancloud.logging.LoggingService` instance:

.. code:: python

    ls = LoggingService(
        url="https://api.us.paloaltonetoworks.com",
        credentials=Credentials()
    )

Now, let's define our :meth:`~pancloud.logging.LoggingService.query` JSON body:

.. code:: python

    b = {
        "query": "select * from panw.traffic limit 5",
        "startTime": 0,  # 1970
        "endTime": 1609459200,  # 2021
        "maxWaitTime": 0  # no logs in initial response
    }

Pass the JSON body to :meth:`~pancloud.logging.LoggingService.query` to query for the last 5 traffic logs:

.. code:: python

    q = ls.query(b)

Print the :meth:`~pancloud.logging.LoggingService.query` results:

.. code:: python

    print(QUERY: {}".format(q.text))

.. code-block:: json

    {"queryId":"222a45ff-4f38-4418-be7d-45b511f191db","sequenceNo":0,"queryStatus":"RUNNING","clientParameters":{},"result":{"esResult":null,"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":5},"selections":[],"params":{}}}}

Awesome! So how do we :meth:`~pancloud.logging.LoggingService.poll` for results?

.. code:: python

    p = ls.poll(query_id, 0, params)  # starting with sequenceNo 0

Cool. Let's take a peek at the results:

.. code:: python

    print(RESULTS: {}".format(p.text))

.. code-block:: json

    {"queryId":"222a45ff-4f38-4418-be7d-45b511f191db","sequenceNo":0,"queryStatus":"JOB_FINISHED","clientParameters":{},"result":{"esResult":{"took":183,"hits":{"total":73708,"maxScore":2,"hits":[{"_index":"147278001_panw.all_2018071000-2018072000_000000","_type":"traffic","_id":"147278001_lcaas:1:261405:0","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":1987,"natsport":41050,"sessionid":696398,"type":"traffic","parent_start_time":0,"packets":15,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1524,"from":"L3-Untrust","parent_session_id":0,"repeatcnt":1,"app":"ms-rdp","vsys":"vsys1","nat":1,"technology-of-app":"client-server","pkts_received":7,"chunks_sent":0,"receive_time":1531180883,"non-standard-dport":0,"subcategory-of-app":"remote-access","chunks_received":0,"users":"99.145.249.194","fwd":1,"config_ver":2049,"cloud_hostname":"ignite-ngfw","customer-id":"147278001","proto":"tcp","tunneled-app":"untunneled","is-saas-of-app":0,"natdport":3389,"action_source":"from-policy","assoc_id":0,"dst":"10.0.0.100","natdst":"10.0.1.20","chunks":0,"flags":4194369,"rule":"RDP 3389 Inbound","dport":3389,"elapsed":2,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/1","device_name":"ignite-ngfw","subtype":"end","time_received":1531180921,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-rst-from-client","natsrc":"10.0.1.11","seqno":1765767,"src":"99.145.249.194","start":1531180903,"time_generated":1531180921,"outbound_if":"ethernet1/2","category-of-app":"networking","bytes_sent":1604,"srcloc":"US","pkts_sent":8,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":3591,"vsys_id":1,"to":"L3-Trust","category":"0","sport":65416,"tunnel":0}},{"_index":"147278001_panw.all_2018071000-2018072000_000000","_type":"traffic","_id":"147278001_lcaas:1:261405:1","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":2193,"natsport":54952,"sessionid":696397,"type":"traffic","parent_start_time":0,"packets":23,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1523,"from":"L3-Untrust","parent_session_id":0,"repeatcnt":1,"app":"ms-rdp","vsys":"vsys1","nat":1,"technology-of-app":"client-server","pkts_received":8,"chunks_sent":0,"receive_time":1531180883,"non-standard-dport":0,"subcategory-of-app":"remote-access","chunks_received":0,"users":"5.39.216.193","fwd":1,"config_ver":2049,"cloud_hostname":"ignite-ngfw","customer-id":"147278001","proto":"tcp","tunneled-app":"untunneled","is-saas-of-app":0,"natdport":3389,"action_source":"from-policy","assoc_id":0,"dst":"10.0.0.100","natdst":"10.0.1.20","chunks":0,"flags":4194369,"rule":"RDP 3389 Inbound","dport":3389,"elapsed":4,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/1","device_name":"ignite-ngfw","subtype":"end","time_received":1531180922,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-rst-from-client","natsrc":"10.0.1.11","seqno":1765768,"src":"5.39.216.193","start":1531180902,"time_generated":1531180922,"outbound_if":"ethernet1/2","category-of-app":"networking","bytes_sent":2328,"srcloc":"NL","pkts_sent":15,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":4521,"vsys_id":1,"to":"L3-Trust","category":"0","sport":30231,"tunnel":0}},{"_index":"147278001_panw.all_2018071000-2018072000_000000","_type":"traffic","_id":"147278001_lcaas:1:261405:5","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":1987,"natsport":54007,"sessionid":696401,"type":"traffic","parent_start_time":0,"packets":16,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1523,"from":"L3-Untrust","parent_session_id":0,"repeatcnt":1,"app":"ms-rdp","vsys":"vsys1","nat":1,"technology-of-app":"client-server","pkts_received":7,"chunks_sent":0,"receive_time":1531180883,"non-standard-dport":0,"subcategory-of-app":"remote-access","chunks_received":0,"users":"103.92.24.220","fwd":1,"config_ver":2049,"cloud_hostname":"ignite-ngfw","customer-id":"147278001","proto":"tcp","tunneled-app":"untunneled","is-saas-of-app":0,"natdport":3389,"action_source":"from-policy","assoc_id":0,"dst":"10.0.0.100","natdst":"10.0.1.20","chunks":0,"flags":4194369,"rule":"RDP 3389 Inbound","dport":3389,"elapsed":4,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/1","device_name":"ignite-ngfw","subtype":"end","time_received":1531180929,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-rst-from-client","natsrc":"10.0.1.11","seqno":1765772,"src":"103.92.24.220","start":1531180909,"time_generated":1531180929,"outbound_if":"ethernet1/2","category-of-app":"networking","bytes_sent":1680,"srcloc":"VN","pkts_sent":9,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":3667,"vsys_id":1,"to":"L3-Trust","category":"0","sport":50905,"tunnel":0}},{"_index":"147278001_panw.all_2018071000-2018072000_000000","_type":"traffic","_id":"147278001_lcaas:1:261405:6","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":2253,"natsport":54992,"sessionid":696402,"type":"traffic","parent_start_time":0,"packets":25,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1523,"from":"L3-Untrust","parent_session_id":0,"repeatcnt":1,"app":"ms-rdp","vsys":"vsys1","nat":1,"technology-of-app":"client-server","pkts_received":9,"chunks_sent":0,"receive_time":1531180883,"non-standard-dport":0,"subcategory-of-app":"remote-access","chunks_received":0,"users":"5.39.216.193","fwd":1,"config_ver":2049,"cloud_hostname":"ignite-ngfw","customer-id":"147278001","proto":"tcp","tunneled-app":"untunneled","is-saas-of-app":0,"natdport":3389,"action_source":"from-policy","assoc_id":0,"dst":"10.0.0.100","natdst":"10.0.1.20","chunks":0,"flags":4194369,"rule":"RDP 3389 Inbound","dport":3389,"elapsed":5,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/1","device_name":"ignite-ngfw","subtype":"end","time_received":1531180930,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-rst-from-client","natsrc":"10.0.1.11","seqno":1765773,"src":"5.39.216.193","start":1531180909,"time_generated":1531180930,"outbound_if":"ethernet1/2","category-of-app":"networking","bytes_sent":2404,"srcloc":"NL","pkts_sent":16,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":4657,"vsys_id":1,"to":"L3-Trust","category":"0","sport":34914,"tunnel":0}},{"_index":"147278001_panw.all_2018071000-2018072000_000000","_type":"traffic","_id":"147278001_lcaas:1:261405:8","_score":2,"_source":{"risk-of-app":"4","logset":"ForwardToLoggingService","bytes_received":1987,"natsport":12657,"sessionid":696405,"type":"traffic","parent_start_time":0,"packets":15,"characteristic-of-app":["able-to-transfer-file","has-known-vulnerability","tunnel-other-application","prone-to-misuse","is-saas"],"dg_hier_level_4":0,"dg_hier_level_1":11,"dg_hier_level_3":0,"dg_hier_level_2":0,"action":"allow","recsize":1523,"from":"L3-Untrust","parent_session_id":0,"repeatcnt":1,"app":"ms-rdp","vsys":"vsys1","nat":1,"technology-of-app":"client-server","pkts_received":7,"chunks_sent":0,"receive_time":1531180883,"non-standard-dport":0,"subcategory-of-app":"remote-access","chunks_received":0,"users":"212.92.116.46","fwd":1,"config_ver":2049,"cloud_hostname":"ignite-ngfw","customer-id":"147278001","proto":"tcp","tunneled-app":"untunneled","is-saas-of-app":0,"natdport":3389,"action_source":"from-policy","assoc_id":0,"dst":"10.0.0.100","natdst":"10.0.1.20","chunks":0,"flags":4194369,"rule":"RDP 3389 Inbound","dport":3389,"elapsed":2,"sanctioned-state-of-app":0,"inbound_if":"ethernet1/1","device_name":"ignite-ngfw","subtype":"end","time_received":1531180932,"actionflags":-9223372036854776000,"tunnelid_imsi":0,"session_end_reason":"tcp-rst-from-client","natsrc":"10.0.1.11","seqno":1765775,"src":"212.92.116.46","start":1531180914,"time_generated":1531180932,"outbound_if":"ethernet1/2","category-of-app":"networking","bytes_sent":1616,"srcloc":"NL","pkts_sent":8,"dstloc":"10.0.0.0-10.255.255.255","serial":"","bytes":3603,"vsys_id":1,"to":"L3-Trust","category":"0","sport":51144,"tunnel":0}}]},"id":"222a45ff-4f38-4418-be7d-45b511f191db","from":0,"size":5,"completed":true,"state":"COMPLETED","timed_out":false},"esQuery":{"table":["panw.traffic"],"query":{"aggregations":{},"size":5},"selections":[],"params":{}}}}

Finally, let's use the :meth:`~pancloud.logging.LoggingService.delete` method to clean up after ourselves (`Note that queries eventually age-out on their own`):

.. code:: python

    ls.delete(query_id)

That's just a taste of what ``pancloud`` can do. Clone the repo and explore the library
of example scripts to get a more complete view of ``pancloud's`` capabilities.

Handling JSON Responses
-----------------------

So you want to convert your JSON response into a python object? With ``requests`` under the hood, it's downright easy:

.. code:: python

    q = ls.query(b)
    j = q.json()

What if you want to strictly enforce proper JSON encoding?

.. code:: python

    ls = LoggingService(
        url="https://api.us.paloaltonetoworks.com",
        credentials=Credentials(),
        enforce_json=True  # try `json.dumps()` on response text
    )

Now, if a response returns something not JSON-serializable, ``pancloud`` will raise a :exc:`~pancloud.exceptions.PanCloudError`.


HTTP Status Code Errors
-----------------------

Here, you've got options. You can choose to handle HTTP status code errors by inspecting ``r.status_code`` or
you can tell ``pancloud`` to raise a :exc:`~pancloud.exceptions.HTTPError` exception whenever an HTTP status code error is returned:

.. code:: python

    ls = LoggingService(
        url="https://api.us.paloaltonetoworks.com",
        credentials=Credentials(),
        raise_for_status=True
    )

.. note::

    Using ``raise_for_status`` breaks the auto_refresh/auto_retry feature built into :class:`~pancloud.httpclient.HTTPClient`,
    as a :exc:`~pancloud.exceptions.HTTPError` will be raised on the initial HTTP 401 response from server.

Exception Handling
------------------

If :class:`~pancloud.httpclient.HTTPClient` encounters any network-related issues,
``pancloud`` will raise a :exc:`~pancloud.exceptions.HTTPError` exception.

If an unexpected argument is passed to a constructor or method, ``pancloud`` raises
a :exc:`~pancloud.exceptions.UnexpectedKwargsError`.

Should you forget to pass a required argument, ``pancloud`` raises :exc:`~pancloud.exceptions.MissingKwargsError`.

All exceptions raised by ``pancloud`` inherit from
:exc:`pancloud.exceptions.PanCloudError`.

That's it - Really! :)

