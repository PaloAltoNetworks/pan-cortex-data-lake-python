.. _quickstart:

Quickstart
==========

This page should give a good indication of how to get started with `pancloud`.

First off, ensure `pancloud` is installed and up-to-date.

Let's start with a basic example.

Querying Logging Service
------------------------

(example below assumes an `ACCESS_TOKEN` has been properly exported)

Start by importing `LoggingService`::

    >>> from pancloud import LoggingService

Next, let's construct a `LoggingService` instance::

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     headers={
    >>>        'Authorization': 'Bearer {}'.format(access_token),
    >>>        "Content-Type": "application/json",
    >>>        "Accept": "application/json"
    >>>    }
    >>> )

Now, let's define our `query` payload::

    >>> data = {  # Prepare 'query' data
    >>>     "query": "select * from panw.traffic limit 5",
    >>>     "startTime": 0,  # 1970
    >>>     "endTime": 1609459200,  # 2021
    >>>     "maxWaitTime": 0  # no logs in initial response
    >>> }

Next, let's perform a `query` for the last 5 traffic logs::

    >>> q = ls.query(data)

Display the `query` results::

    >>> print(QUERY: {}".format(q.text))

Awesome. So how do we `poll` for results?::

    >>> p = ls.poll(query_id, 0, params)  # starting with sequenceNo 0

Cool. Let's take a peek at the results::

    >>> print(RESULTS: {}".format(p.text))

Finally, let's clean up after ourselves by deleing the `query`::

    >>> ls.delete(query_id)

That's just a taste of what `pancloud` can do. Clone the repo and explore the library
of example scripts to get a complete view of `pancloud's` capabilities.

Handling JSON Responses
-----------------------

So you want to convert your JSON response into a python object? With `requests` under the hood, it's downright easy::

    >>> q = ls.query(data)
    >>> json_r = q.json()

What if you want to strictly enforce proper JSON encoding?

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     headers={
    >>>        'Authorization': 'Bearer {}'.format(access_token),
    >>>        "Content-Type": "application/json",
    >>>        "Accept": "application/json"
    >>>     },
    >>>     enforce_json=True
    >>> )

Now, if a response returns improperly-formatted JSON, `pancloud` will raise an `HTTPError`

HTTP Status Errors
------------------

Here, you've got options. You can choose to handle HTTP status errors by inspecting the `r.status_code` and `r.text` or
you can tell `pancloud` to raise a :exc:`~pancloud.exceptions.HTTPError` exception whenever an HTTP status error is returned::

    >>> ls = LoggingService(
    >>>     url="https://api.us.paloaltonetoworks.com",
    >>>     headers={
    >>>        'Authorization': 'Bearer {}'.format(access_token),
    >>>        "Content-Type": "application/json",
    >>>        "Accept": "application/json"
    >>>     },
    >>>     raise_for_status=True
    >>> )

Exception Handling
------------------

If the :exc:`~pancloud.HTTPClient` encounters any network-related issues,
`pancloud` will raise a :exc:`~pancloud.exceptions.HTTPError` exception.

If an unexpected argument is passed to a constructor or method, `pancloud` raises
a :exc:`~pancloud.exceptions.UnexpectedKwargsError`.

Should you forget to pass a required argument, `pancloud` raises :exc:`~pancloud.exceptions.MissingKwargsError`.

All exceptions raised by `pancloud` inherit from
:exc:`pancloud.exceptions.PanCloudError`.

That's it - Really! :)

