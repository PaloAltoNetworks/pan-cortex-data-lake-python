---
sidebar_label: httpclient
title: httpclient
hide_title: true
---
import TOCInline from '@theme/TOCInline';

<TOCInline toc={toc} />;
## HTTPClient

HTTP client for the Cortex™ REST API

### \_\_init\_\_

```python
__init__(**kwargs)
```

Persist `Session()` attributes and implement connection-pooling.

:::info
Built on top of the `Requests` library, `HTTPClient` is an
abstraction layer for preparing and sending HTTP `requests` to the
Application Framework REST APIs and handling `responses`. All
`Requests` are prepared as `Session` objects, with the option
to persist certain attributes such as `cert`, `headers`,
`proxies`, etc. `HTTPAdapter` is implemented to enable more
granular performance and reliability tuning.
:::

**Arguments**:

- `auto_refresh` _bool_ - Perform token refresh prior to request if `access_token` is `None` or expired. Defaults to `True`.
- `auto_retry` _bool_ - Retry last failed HTTP request following a token refresh. Defaults to `True`.
- `credentials` _Credentials_ - [Credentials](credentials.md#credentials) object. Defaults to `None`.
- `enforce_json` _bool_ - Require properly-formatted JSON or raise [CortexError](exceptions.md#cortexerror). Defaults to `False`.
- `force_trace` _bool_ - If `True`, forces trace and forces `x-request-id` to be returned in the response headers. Defaults to `False`.
- `port` _int_ - TCP port to append to URL. Defaults to `443`.
- `raise_for_status` _bool_ - If `True`, raises [HTTPError](exceptions.md#httperror) if status_code not in 2XX. Defaults to `False`.
- `url` _str_ - URL to send API requests to - gets combined with `port` and `endpoint` parameter. Defaults to `None`.
  

**Arguments**:

- `**kwargs` - Supported [Session](https://github.com/psf/requests/blob/main/requests/sessions.py#L337) and
  [HTTPAdapter](https://github.com/psf/requests/blob/main/requests/adapters.py#L85) parameters.

### request

```python
request(**kwargs)
```

Generate HTTP request using given parameters.

:::info
The request method prepares HTTP requests using class or
method-level attributes/variables. Class-level attributes may be
overridden by method-level variables offering greater
flexibility and efficiency.
:::

**Arguments**:

- `enforce_json` _bool_ - Require properly-formatted JSON or raise [HTTPError](exceptions.md#httperror). Defaults to `False`.
- `path` _str_ - URI path to append to URL. Defaults to `empty`.
- `raise_for_status` _bool_ - If `True`, raises [HTTPError](exceptions.md#httperror) if status_code not in 2XX. Defaults to `False`.
  

**Arguments**:

- `**kwargs` - Supported [Session](https://github.com/psf/requests/blob/main/requests/sessions.py#L337) and
  [HTTPAdapter](https://github.com/psf/requests/blob/main/requests/adapters.py#L85) parameters.
  

**Returns**:

- `requests.Response` - Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object

