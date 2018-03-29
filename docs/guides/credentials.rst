.. _credentials:

Credentials
===========

The Application Framework implements OAuth 2.0 for granting authorization to
access your Logging, Event and Directory-Sync instances.

In the near future, ``pancloud`` will come packaged with OAuth2 support to
help ease the process of:

   - Performing OAuth2 and fetching tokens
   - Refreshing tokens
   - Revoking tokens

Obtaining and Using Tokens
--------------------------

Work with your Developer Relations representative to deploy and register an
API Explorer instance, which can be used to retrieve tokens.

Once you've successfully obtained tokens, copy and export your access token
to an environment variable:

Linux/Mac:

.. code-block:: console

    $ export ACCESS_TOKEN=<access token>

Windows:

.. code-block:: console

    $ setx ACCESS_TOKEN <access token>

Once your ``ACCESS_TOKEN`` has been properly exported, you should be ready
to run the examples packaged with ``pancloud``. You may also use this
``ACCESS_TOKEN`` in your own developer projects or to facilitate your
exploration of the Application Framework APIs.

Credential Resolver
-------------------

With the upcoming OAuth 2.0 support, ``pancloud`` will also implement
a built-in ``Credential Resolver`` which will handle fetching ``ACCESS_TOKENS``
during runtime. The credential resolution will follow a particular lookup
order of precedence, which is outlined below:

* Passing credentials as parameters in a service method.
* Passing credentials as parameters when creating an HTTPClient object.
* Environment variables
    * PANCLOUD_ACCESS_TOKEN
    * PANCLOUD_REFRESH_TOKEN
    * PANCLOUD_CLIENT_ID
    * PANCLOUD_INSTANCE_ID
* Shared credential file (~/.pancloud/credentials)
    * PANCLOUD_ACCESS_TOKEN
    * PANCLOUD_REFRESH_TOKEN
    * PANCLOUD_CLIENT_ID
    * PANCLOUD_INSTANCE_ID

