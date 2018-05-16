.. _quickstart:

Quickstart
==========

This page should give a good indication of how to get started with ``pancloud``.

First off, ensure ``pancloud`` is :ref:`installed <installation>` and :ref:`up-to-date <installation>`.

Let's start with a basic example.

Querying Logging Service
------------------------

(example below assumes a ``credentials.json`` file has been properly :ref:`generated <credentials>`)

Start by importing :class:`~pancloud.logging.LoggingService` and :class:`~pancloud.credentials.Credentials`::

    >>> from pancloud import LoggingService
    >>> from pancloud import Credentials

Next, let's construct a :class:`~pancloud.logging.LoggingService` instance::

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     credentials=Credentials()
    >>>    }
    >>> )

Now, let's define our :meth:`~pancloud.logging.LoggingService.query` payload::

    >>> data = {  # Prepare 'query' data
    >>>     "query": "select * from panw.traffic limit 5",
    >>>     "startTime": 0,  # 1970
    >>>     "endTime": 1609459200,  # 2021
    >>>     "maxWaitTime": 0  # no logs in initial response
    >>> }

Next, let's perform a :meth:`~pancloud.logging.LoggingService.query` for the last 5 traffic logs::

    >>> q = ls.query(data)

Display the :meth:`~pancloud.logging.LoggingService.query` results::

    >>> print(QUERY: {}".format(q.text))

Awesome. So how do we :meth:`~pancloud.logging.LoggingService.poll` for results?::

    >>> p = ls.poll(query_id, 0, params)  # starting with sequenceNo 0

Cool. Let's take a peek at the results::

    >>> print(RESULTS: {}".format(p.text))

Finally, let's use the :meth:`~pancloud.logging.LoggingService.delete` method to clean up after ourselves (`Note that queries eventually age-out on their own`)::

    >>> ls.delete(query_id)

That's just a taste of what ``pancloud`` can do. Clone the repo and explore the library
of example scripts to get a more complete view of ``pancloud's`` capabilities.

Handling JSON Responses
-----------------------

So you want to convert your JSON response into a python object? With ``requests`` under the hood, it's downright easy::

    >>> q = ls.query(data)
    >>> json_r = q.json()

What if you want to strictly enforce proper JSON encoding?

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     credentials=Credentials(),
    >>>     enforce_json=True
    >>> )

Now, if a response returns improperly-formatted JSON, ``pancloud`` will raise a :exc:`~pancloud.exceptions.HTTPError`.

HTTP Status Code Errors
-----------------------

Here, you've got options. You can choose to handle HTTP status code errors by inspecting ``r.status_code`` or
you can tell ``pancloud`` to raise a :exc:`~pancloud.exceptions.HTTPError` exception whenever an HTTP status code error is returned::

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     credentials=Credentials(),
    >>>     raise_for_status=True
    >>> )

Exception Handling
------------------

If :class:`~pancloud.logging.HTTPClient` encounters any network-related issues,
``pancloud`` will raise a :exc:`~pancloud.exceptions.HTTPError` exception.

If an unexpected argument is passed to a constructor or method, ``pancloud`` raises
a :exc:`~pancloud.exceptions.UnexpectedKwargsError`.

Should you forget to pass a required argument, ``pancloud`` raises :exc:`~pancloud.exceptions.MissingKwargsError`.

All exceptions raised by ``pancloud`` inherit from
:exc:`pancloud.exceptions.PanCloudError`.

That's it - Really! :)

