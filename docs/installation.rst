.. highlight:: shell

.. _installation:

============
Installation
============


Stable release
--------------

To install the Palo Alto Networks Cloud Python SDK, run this command in your terminal:

.. code-block:: console

    $ pip install pancloud

To upgrade the Palo Alto Networks Cloud Python SDK, run this command in your terminal:

.. code-block:: console

    $ pip install pancloud --upgrade

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


Using Pipenv
------------

(`The officially recommended Python packaging tool from Python.org`)

To install the Palo Alto Networks Cloud Python SDK using `pipenv`_, start by creating a virtualenv:

.. code-block:: console

    $ pipenv install

You can optionally specify which python version to use in your virtualenv using the following:

.. code-block:: console

    $ pipenv --three install

or

.. code-block:: console

    $ pipenv --two install

I highly recommend you move to python3 as python2 will be `retiring`_ soon.

.. _pipenv: https://docs.pipenv.org/
.. _retiring: https://pythonclock.org/


Now it's time to install ``pancloud``:

.. code-block:: console

    $ pipenv install pancloud

To upgrade `pancloud` using pipenv:


.. code-block:: console

    $ pipenv upgrade pancloud


From sources
------------

The sources for the Palo Alto Networks Cloud Python SDK can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/PaloAltoNetworks/pancloud

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/PaloAltoNetworks/pancloud/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/PaloAltoNetworks/pancloud
.. _tarball: https://github.com/PaloAltoNetworks/pancloud/tarball/master
