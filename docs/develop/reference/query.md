---
sidebar_label: query
title: query
hide_title: true
---
:::info
The Query Service is a Palo Alto Networks cloud service which allows
for the storage and retrieval of data stored in the Cortex Data Lake.
Any type of textual data can be stored in the Cortex Data Lake. Palo
Alto Networks firewalls and software can write data to this service, as
can the software and services created by Palo Alto Network's various
partners.
:::

**Examples**:

  Refer to the [examples provided with this library](https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/tree/master/examples).

## QueryService

A Cortex™ Query Service instance.

### \_\_init\_\_

```python
__init__(**kwargs)
```

**Arguments**:

- `session` _HTTPClient_ - [HTTPClient](httpclient.md#httpclient) object. Defaults to `None`.
- `url` _str_ - URL to send API requests to. Later combined with `port` and `endpoint` parameter.
  

**Arguments**:

- `**kwargs` - Supported [HTTPClient](httpclient.md#httpclient) parameters.

### cancel\_job

```python
cancel_job(job_id=None, **kwargs)
```

Cancel a query job.

**Arguments**:

- `job_id` _str_ - Specifies the ID of the query job.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.
  

**Raises**:


### create\_query

```python
create_query(job_id=None, query_params=None, **kwargs)
```

Create a search request.

:::info
When submission is successful, http status code of `201` (Created)
is returned with a 'jobId' in response. Specifying a 'jobId' is
optional.
:::

**Arguments**:

- `job_id` _str_ - Specifies the ID of the query job. (optional)
- `query_params` _dict_ - Query parameters.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

### get\_job

```python
get_job(job_id=None, **kwargs)
```

Get specific job matching criteria.

**Arguments**:

- `job_id` _str_ - Specifies the ID of the query job.
- `params` _dict_ - Payload/request dictionary.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

### get\_job\_results

```python
get_job_results(job_id=None, max_wait=None, offset=None, page_cursor=None, page_number=None, page_size=None, result_format=None, **kwargs)
```

Get results for a specific job_id.

**Arguments**:

- `job_id` _str_ - Specifies the ID of the query job.
- `max_wait` _int_ - How long to wait in ms for a job to complete. Max 2000.
- `offset` _int_ - Along with pageSize, offset can be used to page through result set.
- `page_cursor` _str_ - Token/handle that can be used to fetch more data.
- `page_number` _int_ - Return the nth page from the result set as specified by this parameter.
- `page_size` _int_ - If specified, limits the size of a batch of results to the specified value. If un-specified, backend picks a size that may provide best performance.
- `result_format` _str_ - valuesArray or valuesDictionary.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

### iter\_job\_results

```python
iter_job_results(job_id=None, max_wait=None, offset=None, page_cursor=None, page_number=None, page_size=None, result_format=None, **kwargs)
```

Retrieve results iteratively in a non-greedy manner using scroll token.

**Arguments**:

- `job_id` _str_ - Specifies the ID of the query job.
- `max_wait` _int_ - How long to wait in ms for a job to complete. Max 2000.
- `offset` _int_ - Along with pageSize, offset can be used to page through result set.
- `page_cursor` _str_ - Token/handle that can be used to fetch more data.
- `page_number` _int_ - Return the nth page from the result set as specified by this parameter.
- `page_size` _int_ - If specified, limits the size of a batch of results to the specified value. If un-specified, backend picks a size that may provide best performance.
- `result_format` _str_ - valuesArray or valuesJson.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

### list\_jobs

```python
list_jobs(max_jobs=None, created_after=None, state=None, job_type=None, tenant_id=None, **kwargs)
```

Get all jobs matching criteria.

**Arguments**:

- `limit` _int_ - Max number of jobs.
- `created_after` _int_ - List jobs created after this unix epoch UTC datetime.
- `state` _str_ - Job state, e.g. 'RUNNING', 'PENDING', 'FAILED', 'DONE'.
- `job_type` _str_ - Query type hint.
- `tenant_id` _str_ - Tenant ID.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

