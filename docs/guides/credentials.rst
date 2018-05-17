.. _credentials:

Credentials
===========

The Application Framework implements OAuth 2.0 for granting authorization to
access your Logging, Event and Directory-Sync instances.

``pancloud`` comes packaged with OAuth 2.0 support to ease the process of:

   - Generating authorization URL and fetching tokens
   - Refreshing tokens
   - Revoking tokens
   - Auto token refresh and auto-retry

Obtaining and Using Tokens
--------------------------

Work with your Developer Relations representative to register your
application and receive the credentials needed to obtain an ``access_token``.
You'll need a ``client_id``, ``client_secret``, and ``refresh_token``.
``API Explorer`` may optionally be used to obtain these credentials.

Once acquired, you can generate a ``credentials.json`` file using the
``summit.py`` command-line utility or the ``credentials_generate.py``
script included in the ``pancloud`` GitHub repo examples folder.

summit.py:

.. code-block:: console

    $ summit.py -C --R0 cred-init.json --write

cred-init.json example:

.. code-block:: json

    {
    "client_id":"<client_id>",
    "client_secret":"<client_secret>",
    "refresh_token":"<refresh_token>"
    }

credentials_generate.py:

.. code-block:: console

    $ ./credentials_generate.py

    Note: The script will prompt for ``client_id``, ``client_secret``
    and ``refresh_token``.


Once your ``credentials.json`` file is generated, you should be ready
to run the examples packaged with the ``pancloud`` repo or use ``pancloud``
in your own project.

Credential Resolver
-------------------
``pancloud`` also implements a built-in ``Credential Resolver`` which
handles refreshing ``access tokens`` during runtime. The credential
resolution will follow a particular lookup order of precedence, which
is outlined below:

* Passing ``Credentials`` to a service or service method.
* Passing ``Credentials`` to an HTTPClient/session object.
* Environment variables
    * REFRESH_TOKEN
    * CLIENT_ID
    * CLIENT_SECRET
* Credentials file (~/.config/pancloud/credentials.json)
    * ``refresh_token``
    * ``client_id``
    * ``client_secret``

Note: The ``Credentials`` object supports ``profiles`` which can be
used to conveniently switch between developer environments.

Auto-refresh/Auto-retry
-----------------------
By default, ``Credentials`` supports ``auto_refresh`` and ``auto_retry``
when valid credentials are present.

``pancloud`` will auto-refresh and apply the ``access_token`` to the
``"Authorization: Bearer"`` header under the following conditions:

* ``auto_refresh`` is set to ``True``.
* ``access_token`` is ``None``.
* ``pancloud`` receives an ``HTTP 401`` status code from the Application Framework API and cached token is the same as the ``access token`` to refresh.

Additionally, ``pancloud`` will ``auto_retry`` a request if an
``auto_refresh`` occurred due to an ``HTTP 401`` status code.

Access Token Caching
--------------------
By default, ``Credentials`` supports caching ``access tokens`` by writing the
most recent ``access_token`` to the credentials store. The desired effect
of caching ``access tokens`` is to limit the number of times a token
refresh is required.

For example, if your application implements concurrency,
there might be situations where a burst of activity leads to multiple clients
requesting a token refresh. By caching the ``access_token``, ``pancloud``
can instruct these clients to check the credentials store first, before
attempting to communicate with the token endpoint to perform a refresh.

In addition to improving client performance, this method of caching
``access tokens`` also helps prevent an inadvertent denial-of-service
of the token endpoint.

Custom Storage Adapters
-----------------------
The default storage adapter for ``Credentials`` is ``TinyDB``, which
stores credentials in ``~/.config/pancloud/credentials.json``. The good
news is that ``TinyDB`` is just the first of many potential credential
stores that ``pancloud`` will support.

The road map for ``pancloud`` includes adding additional storage adapters
to support storing credentials in ``Redis``, ``Memcached``, ``MongoDB``,
``AWS Key Management Service`` and ``sqlite3``, to name a few. Ultimately,
the goal is to support any possible store!

