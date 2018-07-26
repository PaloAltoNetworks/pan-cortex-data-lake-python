.. _credentials:

Credentials
===========

The Application Framework implements OAuth 2.0 for delegating access to
your Logging, Event and Directory Sync services.

The ``pancloud`` SDK comes packaged with OAuth 2.0 support to ease the process of:

   - Generating authorization URL
   - Exchanging authorization code for tokens (authorization code grant)
   - Refreshing tokens
   - Revoking tokens
   - Token caching
   - Using a custom credentials store (storage adapters)

Obtaining and Using Tokens
--------------------------

Work with your Developer Relations representative to register your
application and receive the credentials needed to obtain an ``access_token``.
Minimally, you'll need a ``client_id``, ``client_secret``, and ``refresh_token``.
If you're working on an application without a user agent,
``API Explorer`` may optionally be used to obtain a ``refresh_token``,
i.e. perform authorization code grant.

Once acquired, you can generate a ``credentials.json`` file using the
``summit.py`` command-line utility or the ``credentials_generate.py``
script included in the ``pancloud`` GitHub repo examples folder.

summit.py:

.. code-block:: console

    $ summit.py -C --R0 cred-init.json --write

cred-init.json example:

.. code-block:: json

    {
        "client_id": "<client_id>",
        "client_secret": "<client_secret>",
        "refresh_token": "<refresh_token>"
    }

credentials_generate.py:

.. code-block:: console

    $ ./credentials_generate.py

.. note::

    The script will prompt for ``client_id``, ``client_secret``,
    ``refresh_token`` and a ``profile`` name.


Once your ``credentials.json`` file is generated, you should be ready
to run the examples packaged with the ``pancloud`` repo or use the ``pancloud``
SDK in your own project.

Credential Resolver
-------------------
The ``pancloud`` :class:`~pancloud.credentials.Credentials` class implements
a built-in resolver that looks for credentials in different places, following
a particular lookup order:

1. Credentials passed as :class:`~pancloud.credentials.Credentials` constructor key-word arguments:

.. code-block:: python

    c = Credentials(
        client_id=<client_id>,
        client_secret=<client_secret>,
        refresh_token=<refresh_token>
    )

2. Credentials stored as environment variables:

    - ``PAN_REFRESH_TOKEN``
    - ``PAN_CLIENT_ID``
    - ``PAN_CLIENT_SECRET``

3. Credentials stored in a credentials file (~/.config/pancloud/credentials.json) or custom store:

.. code-block:: python

    {
        "profiles": {
            "1": {
                "access_token": <access_token>,
                "client_id": <client_id>,
                "client_secret": <client_secret>,
                "profile": <profile>,
                "refresh_token": <refresh_token>
            }
        }
    }

The resolution performs a top-down, first match evaluation and stops when any of
the four credentials are detected. Attempting to :meth:`~pancloud.credentials.Credentials.refresh`
with an incomplete set of credentials will raise a :exc:`~pancloud.exceptions.PartialCredentialsError`.

.. note::

    The ``Credentials`` class supports ``profiles`` which can be
    used to conveniently switch between developer environments. You may also
    choose to use a different :class:`~pancloud.adapters.adapter.StorageAdapter` than
    the default (``TinyDB``) which would result in credentials being stored
    outside of ``credentials.json``.

Auto-refresh/Auto-retry
-----------------------
By default, ``Credentials`` supports ``auto_refresh`` and ``auto_retry``
when valid credentials are present (and ``raise_for_status`` is not passed).

``pancloud`` will auto-refresh and apply the ``access_token`` to the
``"Authorization: Bearer"`` header under the following conditions:

* ``auto_refresh`` is set to ``True``.
* ``access_token`` is ``None``.
* ``pancloud`` receives an ``HTTP 401`` status code from the Application Framework API and the cached token is the same as the ``access token`` to refresh.

Additionally, ``pancloud`` will ``auto_retry`` a request if an
``auto_refresh`` occurred due to an ``HTTP 401`` status code.

Access Token Caching
--------------------
By default, ``Credentials`` supports caching ``access tokens``, by writing the
most recent ``access_token`` to the credentials store. The desired effect
of caching ``access tokens`` is to limit the number of times a token
refresh is required.

For example, if your application implements concurrency,
there might be situations where a burst of activity leads to multiple clients
requesting a token refresh. By caching the ``access_token``, ``pancloud``
can instruct these clients to check the credentials store first, before
attempting to communicate with the token endpoint to perform a refresh.

.. note::

    In addition to improving client performance, this method of caching
    ``access tokens`` also helps prevent an inadvertent denial-of-service
    of the token endpoint.

Rolling Refresh Tokens and Caching
----------------------------------
If the authorization server supports rolling refresh tokens, ``Credentials``
will automatically record and cache a new ``refresh_token``, if one is
returned by the token refresh endpoint.

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

The following gists illustrate a few examples.

Memcached Storage Adapter
-------------------------

.. raw:: html

    <embed>
        <script src="https://gist.github.com/sserrata/a544d12bfa7e4d5e23f61a09adf0051e.js"></script>
    </embed>

Redis Storage Adapter
---------------------

.. raw:: html

    <embed>
        <script src="https://gist.github.com/sserrata/3ecbc2a2873025efcfcc79e280e28577.js"></script>
    </embed>

