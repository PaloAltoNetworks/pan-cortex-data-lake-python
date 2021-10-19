![Tests](https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/workflows/Tests/badge.svg) ![PyPI upload](https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/workflows/PyPI%20upload/badge.svg?branch=master) ![![PyPI version](https://badge.fury.io/py/pan-cortex-data-lake.svg)](https://badge.fury.io/py/pan-cortex-data-lake)

# Palo Alto Networks Cortex™ Data Lake SDK

Python idiomatic SDK for the Cortex™ Data Lake.

The Palo Alto Networks Cortex Data Lake Python SDK was created to assist
developers with programmatically interacting with the Palo Alto Networks
Cortex™ Data Lake API.

The primary goal is to provide full, low-level API coverage for the
following Cortex™ Data Lake services:

-   Query Service

The secondary goal is to provide coverage, in the form of helpers, for
common tasks/operations.

-   Log/event pagination
-   OAuth 2.0 and token refreshing

Resources:

-   Documentation: <https://cortex.pan.dev>
-   Free software: [ISC license](https://choosealicense.com/licenses/isc/)

---

## Features

-   HTTP client wrapper for the popular Requests library with full access to its features.
-   Language bindings for Query Service.
-   Helper methods for performing common tasks, such as log/event pagination.
-   Support for OAuth 2.0 grant code authorization flow.
-   Library of example scripts illustrating how to leverage the SDK.
-   Support for API Explorer Developer Tokens for easier access to API!

## Status

The Palo Alto Networks Cortex™ Data Lake Python SDK is considered **beta** at this time.

## Installation

From PyPI:

```bash
pip install pan-cortex-data-lake
```

From source:

```bash
pip install .
```

To run tests:

```bash
pip install .[test]
```

## Obtaining and Using OAuth 2.0 Tokens

If you're an app developer, work with your Developer Relations representative to obtain your OAuth2 credentials. API Explorer may optionally be used to generate a Developer Token, which can also be used to authenticate with the API. For details on API Explorer developer tokens, please visit <https://cortex.pan.dev/docs/learn/developer_tokens>.

# Example

```python
from pan_cortex_data_lake import Credentials, QueryService


c = Credentials()
qs = QueryService(credentials=c)
query_params = {
    "query": "SELECT * FROM `1234567890.firewall.traffic` LIMIT 1",
}
q = qs.create_query(query_params=query_params)
results = qs.get_job_results(job_id=q.json()['jobId'])
print(results.json())
```

# Contributors

<a href="https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=PaloAltoNetworks/pan-cortex-data-lake-python" />
</a>
