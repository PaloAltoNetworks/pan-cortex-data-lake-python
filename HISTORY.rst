=======
History
=======

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


