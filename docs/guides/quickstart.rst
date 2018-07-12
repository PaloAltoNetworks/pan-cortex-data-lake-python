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

Awesome! So how do we :meth:`~pancloud.logging.LoggingService.poll` for results?

.. code:: python

    p = ls.poll(query_id, 0, params)  # starting with sequenceNo 0

Cool. Let's take a peek at the results:

.. code:: python

    print(RESULTS: {}".format(p.text))

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
you can tell ``pancloud`` to raise a :exc:`~requests.exceptions.HTTPError` exception whenever an HTTP status code error is returned::

.. code:: python

    ls = LoggingService(
        url="https://api.us.paloaltonetoworks.com",
        credentials=Credentials(),
        raise_for_status=True
    )

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

