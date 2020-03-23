# History

## 2.0.0-alpha7 (2020-03-23)

-   Updated SDK name in HTTPClient default headers
-   Added support for specifying Developer Token provider using envar or kwarg
-   Updated `credentials.json` parent dir name

## 2.0.0-alpha6 (2020-03-04)

-   Changed `iter_job_results()` method to allow overriding `enforce_json`
-   Updated default API gateway URL
-   Minor corrections to docstrings
-   Removeed suppression of urllib3 warnings
-   Updated example scripts
-   Updated README
-   Reformatted/refactoring with black
-   Added `transactions` attribute to `ApiStats` with default value
-   Reimplemented module-level logging
-   Applied change to `HTTPClient` to avoid applying header credentials twice when no method credentials are present

## 2.0.0-alpha5 (2020-03-03)

-   Fixed `Credentials` storage adapter import

## 2.0.0-alpha4 (2020-03-03)

-   Updated MANIFEST

## 2.0.0-alpha3 (2020-02-20)

-   Renamed `pancloud` package directory to `pan_cortex_data_lake`
-   Published to PyPI under new name, `pan-cortex-data-lake`
-   Moved from RST to MD format for docs files
-   Droped support for `pipenv`
-   Updated setup.cfg and setup.py
-   Updated tests and test config files

## 2.0.0-alpha2 (2020-01-09)

-   Fixed invalid use of `HTTPClient` class `path` keyword arg in `Credentials`

## 2.0.0-alpha1 (2019-11-21)

-   Removed all legacy modules, e.g. logging, event and directorysync
-   Removed all references to legacy modules and classes
-   Removed all legacy tests
-   Added util module
-   Added query module
-   Added example query script
-   Updated httpclient module

## 1.5.1 (2019-04-26)

-   Updated Pipfile.lock.
-   Replaced recursion with loop pattern in `LoggingService` `xpoll()` method.
-   Added `decode('utf-8')` to base64 decoded JWT to ensure compatibility with `json.loads()`.
-   Addressed minor typos in docs.

## 1.5.0 (2019-02-27)

-   Added `flush()` method to `EventService` class.
-   Added `auto_refresh` support to `HTTPClient` `_apply_credentials()` method.
-   Removed `auto_retry` feature from `HTTPClient` class.
-   Refactored `HTTPClient` class `request()` method keyword argument overrides.
-   Removed unused `token_revoke_url` keyword argument.
-   Added support for API Explorer Developer Tokens to `Credentials` class.
-   Refactored `Credentials` `refresh()` method.

## 1.4.0 (2018-10-04)

-   Added default URL to `HTTPClient` class.
-   Updated docstrings for `StorageAdapter`, `TinyDBStore` and `Credentials` classes.
-   Now returning `state` as `str` instead of `UUID` in `get_authorization_url()` method.
-   Now unifying display results for -m/-s/--write. For -m you now need an output specifier (-j/-p) to print the response.
-   Added `decode_jwt_payload()` method to allow for extracting/using all JWT fields.
-   Added -s option to allow for invocation of setter methods. This allows modifying of credential store fields.
-   Added credential setters to allow for modifying credentials.
-   Updated examples.
-   Switched from using `requests` to `HTTPClient` in `Credentials` class.
-   Now checking JWT access_token `exp` to determine if refresh if needed.
-   Now generating a new `state` each time `get_authorization_url()` is called.
-   Added `__repr__` to `Credentials` class with support for masking secrets.
-   Updated -E --ack,nack,poll options usage to be accurate.
-   `JOB_FAILED` response in `xpoll()` queryStatus now includes errorCode.

# 1.3.0 (2018-08-04)

-   Added support for custom read/write credentials path.
-   `TinyDBStore` `fetch_credential()` now returns `None` instead of empty `str`.
-   Fixed bug that caused `_resolve_credential()` to be executed an inefficient number of times.
-   Now updating `HTTPClient` headers instead of overriding them which previously broke HTTP persistence.
-   Added JMESPath `isotime()` function to `summit.py` which prints epoch.
-   Added argument to `EventService` `xpoll()` method to support sleeping between polls.
-   Added `PAN_` prefix to envars to avoid name collisions.
-   Fixed bug when `R['R1_obj']['LoggingService.query']` is None and allow json=None case with special case of --end -1 which will not set a default end of now.
-   Fixed bug that nulled out credentials if an error occurred during a `fetch_tokens()` or `refresh()` operation.
-   Now enforcing strict credential resolution. Previous behavior allowed for merging credentials from different providers.
-   Added support for caching `refresh_token` to support rolling.
-   Added support for writing logs to `summit.py`.
-   Switch from using `data` param to `json` param in client/service methods.
-   Now defaulting `R1` to `None` so don't send body unless specified.
-   Now printing request headers and body at debug level 3 in `summit.py`.
-   Added enhancements to `summit.py` for specifying `startTime` and `endTime`.

# 1.2.3 (2018-06-21)

-   Reversed the `access_token` lookup order in get_credentials() method.
-   Added `_resolve_credential()` to `access_token()` property method to support token caching.
-   Now comparing passed `access_token` in `refresh()` method to value returned by property method.

# 1.2.2 (2018-06-20)

-   Added pancloud.adapters to find_packages include list to resolve issue with PyPI package.

# 1.2.1 (2018-06-20)

-   Added requirements.txt to MANIFEST.in to address build issues with PyPI package.
-   Fixed issue in README.rst that prevented PyPI from properly rendering.

# 1.2.0 (2018-06-20)

-   Updated README.rst
-   Updated RTD API Reference.
-   Added `pancloud` to requirements_dev.txt
-   Added docstrings to `Credentials` property methods.
-   Changed logging xpoll() to return entire log entry instead of just `_source` dictionary.
-   Added `Credentials` Storage Adapter feature and moved `TinyDB` code to `tinydb_adapter.py`, the default storage adapter.
-   Automatically carry `queryId` from `logging --query` response to `--id` in subsequent `--poll`, `--xpoll` and `--delete` in `summit.py`.
-   Various bug fixes and improvements to `summit.py`.
-   Added support for caching `access_token` in credentials store.
-   Added `write()` method to `LoggingService` class to support writing logs.
-   Fixed issues with `Credentials` `get_authorization_url` and `fetch_tokens` methods.
-   Added`logging_write.py` to examples.

# 1.1.0 (2018-05-08)

-   Updated logging `xpoll()` to reflect behavior of current API.
-   Added `credentials.py` module to support OAuth2 operations.
-   Added `auto\_refresh` and `auto_retry` support to `HTTPClient()`.
-   Added `PartialCredentialsError` exception to handle cases where incomplete credentials are passed to `Credentials`.
-   Removed extraneous dependencies, e.g. pyopenssl.
-   Cleaned up requirements.txt and PipLock files.
-   Added `TinyDB` package for reading/writing `credentials.json` file.
-   Now raising `PanCloudError` for `enforce_json` errors.
-   Removed logging `poll_all()` method and example script.
-   Now checking if `sequence_no` is `None` before incrementing in logging `iter_poll()` method.
-   Added event `xpoll()` method to support iterating through events.
-   Introducing `summit.py`, a command-line interface for `pancloud`.
-   Added `credentials` support to `summit.py` to enable writing `credentials.json` file and passing `Credentials` with requests.
-   Updated example scripts library to incorporate new credentials feature.

# 1.0.3 (2018-04-26)

-   Overhauled and updated RTDs
-   Updated `__init__.py` to allow package-level imports
-   Fixed issue where starrifying authorization token in `__repr__` overrode value in request header.

# 1.0.2 (2018-03-20)

-   Updated .gitignore to exclude .pytest_cache
-   Excluding certain functions/classes from tests until API Gateway is ready
-   Renamed tests modules to all lowercase
-   Bumped version to 1.0.2 from 1.0.1
-   Updated 'query' and 'poll' endpoints to reflect current working state of APIs
-   Fixed .travis.yml branch regex
-   Updated example scripts
-   Removed pyopenssl property method from HTTPClient
-   Removed test_repr() as not all tested python versions support ordered kwargs

# 1.0.1 (2018-03-19)

-   Default to empty `path`

# 1.0.0 (2018-03-16)

-   First release.
