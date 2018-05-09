=======
History
=======

1.1.0 (2018-05-08)
------------------

* Updated logging `xpoll()` to reflect behavior of current API.
* Added `credentials.py` module to support OAuth2 operations.
* Added `auto_refresh` and `auto_retry` support to `HTTPClient()`.
* Added `PartialCredentialsError` exception to handle cases where incomplete credentials are passed to `Credentials`.
* Removed extraneous dependencies, e.g. pyopenssl.
* Cleaned up requirements.txt and PipLock files.
* Added `TinyDB` package for reading/writing `credentials.json` file.
* Now raising `PanCloudError` for `enforce_json` errors.
* Removed logging `poll_all()` method and example script.
* Now checking if `sequence_no` is `None` before incrementing in logging `iter_poll()` method.
* Added event `xpoll()` method to support iterating through events.
* Introducing `summit.py`, a command-line interface for `pancloud`.
* Added `credentials` support to `summit.py` to enable writing `credentials.json` file and passing `Credentials` with requests.
* Updated example scripts library to incorporate new credentials feature.

1.0.3 (2018-04-26)
------------------

* Overhauled and updated RTDs
* Updated `__init__.py` to allow package-level imports
* Fixed issue where starrifying authorization token in `__repr__` overrode value in request header.

1.0.2 (2018-03-20)
------------------

* Updated .gitignore to exclude .pytest_cache
* Excluding certain functions/classes from tests until API Gateway is ready
* Renamed tests modules to all lowercase
* Bumped version to 1.0.2 from 1.0.1
* Updated 'query' and 'poll' endpoints to reflect current working state of APIs
* Fixed .travis.yml branch regex
* Updated example scripts
* Removed pyopenssl property method from HTTPClient
* Removed test_repr() as not all tested python versions support ordered kwargs

1.0.1 (2018-03-19)
------------------

* Default to empty `path`

1.0.0 (2018-03-16)
------------------

* First release.
