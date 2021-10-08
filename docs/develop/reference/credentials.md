---
sidebar_label: credentials
title: credentials
hide_title: true
---
import TOCInline from '@theme/TOCInline';

<TOCInline toc={toc} />;
:::info
The Credentials object can be used to access, store and refresh credentials.
:::

## Credentials

An Application Framework credentials object.

### \_\_init\_\_

```python
__init__(access_token=None, auth_base_url=None, cache_token=True, client_id=None, client_secret=None, developer_token=None, developer_token_provider=None, instance_id=None, profile=None, redirect_uri=None, region=None, refresh_token=None, scope=None, storage_adapter=None, storage_params=None, token_url=None, **kwargs)
```

Persist `Session()` and credentials attributes.

:::info
The `Credentials` class is an abstraction layer for accessing,
storing and refreshing credentials needed for interacting with
the Application Framework.

`Credentials` resolves credentials from the following locations,
in the following order:

1. Class instance variables
2. Environment variables
3. Credentials store
:::

**Arguments**:

- `access_token` _str_ - OAuth2 access token. Defaults to `None`.
- `auth_base_url` _str_ - IdP base authorization URL. Default to `None`.
- `cache_token` _bool_ - If `True`, stores `access_token` in token store. Defaults to `True`.
- `client_id` _str_ - OAuth2 client ID. Defaults to `None`.
- `client_secret` _str_ - OAuth2 client secret. Defaults to `None`.
- `developer_token` _str_ - Developer Token. Defaults to `None`.
- `developer_token_provider` _str_ - Developer Token Provider URL. Defaults to `None`.
- `instance_id` _str_ - Instance ID. Defaults to `None`.
- `profile` _str_ - Credentials profile. Defaults to 'default'.
- `redirect_uri` _str_ - Redirect URI. Defaults to `None`.
- `region` _str_ - Region. Defaults to `None`.
- `refresh_token` _str_ - OAuth2 refresh token. Defaults to `None`.
- `scope` _str_ - OAuth2 scope. Defaults to `None`.
- `storage_adapter` _str_ - Namespace path to storage adapter module. Defaults to "pan_cortex_data_lake.adapters.tinydb_adapter.TinyDBStore".
- `storage_params` _dict_ - Storage adapter parameters. Defaults to `None`.
- `token_url` _str_ - Refresh URL. Defaults to `None`.
- `token_revoke_url` _str_ - Revoke URL. Defaults to `None`.
- `**kwargs` - Supported [Session](https://github.com/psf/requests/blob/main/requests/sessions.py#L337) parameters.
  

**Examples**:

  
  ```python
  from pan_cortex_data_lake import Credentials
  
  
  # Load credentials from envars or ~/.config/pan_cortex_data_lake/credentials.json
  c = Credentials()
  
  # Load credentials with static access_token
  access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRyYXNoIFBBTkRBIiwiaWF0IjoxNTE2MjM5MDIyfQ"
  c = Credentials(access_token=access_token)
  
  # Load full credentials
  client_id = "trash"
  client_secret = "panda"
  refresh_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRyYXNoIFBBTkRBIiwiaWF0IjoxNTE2MjM5MDIyfQ"
  c = Credentials(client_id=client_id, client_secret=client_secret, refresh_token=refresh_token)
  ```

### access\_token

```python
@property
access_token()
```

Get access_token.

### access\_token

```python
@access_token.setter
access_token(access_token)
```

Set access_token.

### cache\_token

```python
@property
cache_token()
```

Get cache_token setting.

### client\_id

```python
@property
client_id()
```

Get client_id.

### client\_id

```python
@client_id.setter
client_id(client_id)
```

Set client_id.

### client\_secret

```python
@property
client_secret()
```

Get client_secret.

### client\_secret

```python
@client_secret.setter
client_secret(client_secret)
```

Set client_secret.

### developer\_token

```python
@property
developer_token()
```

Get developer token.

### developer\_token

```python
@developer_token.setter
developer_token(developer_token)
```

Set developer token.

### developer\_token\_provider

```python
@property
developer_token_provider()
```

Get developer token provider.

### developer\_token\_provider

```python
@developer_token_provider.setter
developer_token_provider(developer_token_provider)
```

Set developer token provider.

### jwt\_exp

```python
@property
jwt_exp()
```

Get JWT exp.

### jwt\_exp

```python
@jwt_exp.setter
jwt_exp(jwt_exp)
```

Set jwt_exp.

### refresh\_token

```python
@property
refresh_token()
```

Get refresh_token.

### refresh\_token

```python
@refresh_token.setter
refresh_token(refresh_token)
```

Set refresh_token.

### decode\_jwt\_payload

```python
decode_jwt_payload(access_token=None)
```

Extract payload field from JWT.

**Arguments**:

- `access_token` _str_ - Access token to decode. Defaults to `None`.
  

**Returns**:

- `dict` - JSON object that contains the claims conveyed by the JWT.
  

**Raises**:

- `CortexError` - If unable to decode JWT payload.

### fetch\_tokens

```python
fetch_tokens(client_id=None, client_secret=None, code=None, redirect_uri=None, **kwargs)
```

Exchange authorization code for token.

**Arguments**:

- `client_id` _str_ - OAuth2 client ID. Defaults to `None`.
- `client_secret` _str_ - OAuth2 client secret. Defaults to `None`.
- `code` _str_ - Authorization code. Defaults to `None`.
- `redirect_uri` _str_ - Redirect URI. Defaults to `None`.
  

**Returns**:

- `dict` - Response from token URL.
  

**Raises**:

- `CortexError` - If non-2XX response or 'error' received from API or invalid JSON.

### get\_authorization\_url

```python
get_authorization_url(client_id=None, instance_id=None, redirect_uri=None, region=None, scope=None, state=None)
```

Generate authorization URL.

**Arguments**:

- `client_id` _str_ - OAuth2 client ID. Defaults to `None`.
- `instance_id` _str_ - App Instance ID. Defaults to `None`.
- `redirect_uri` _str_ - Redirect URI. Defaults to `None`.
- `region` _str_ - App Region. Defaults to `None`.
- `scope` _str_ - Permissions. Defaults to `None`.
- `state` _str_ - UUID to detect CSRF. Defaults to `None`.
  

**Returns**:

  str, str: Auth URL, state

### get\_credentials

```python
get_credentials()
```

Get read-only credentials.

**Returns**:

- `class` - Read-only credentials.

### jwt\_is\_expired

```python
jwt_is_expired(access_token=None, leeway=0)
```

Validate JWT access token expiration.

**Arguments**:

- `access_token` _str_ - Access token to validate. Defaults to `None`.
- `leeway` _float_ - Time in seconds to adjust for local clock skew. Defaults to 0.
  

**Returns**:

- `bool` - `True` if expired, otherwise `False`.

### remove\_profile

```python
remove_profile(profile)
```

Remove profile from credentials store.

**Arguments**:

- `profile` _str_ - Credentials profile to remove.
  

**Returns**:

  Return value of `self.storage.remove_profile()`.

### refresh

```python
refresh(access_token=None, **kwargs)
```

Refresh access and refresh tokens.

**Arguments**:

- `access_token` _str_ - Access token to refresh. Defaults to `None`.
- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `str` - Refreshed access token and refresh token (if available).
  

**Raises**:

- `CortexError` - If non-2XX response or 'error' received from API or invalid JSON.
- `PartialCredentialsError` - If one or more required credentials are missing.

### revoke\_access\_token

```python
revoke_access_token(**kwargs)
```

Revoke access token.

**Arguments**:

- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `dict` - JSON object that contains the response from API.
  

**Raises**:

- `CortexError` - If non-2XX response or 'error' received from API or invalid JSON.

### revoke\_refresh\_token

```python
revoke_refresh_token(**kwargs)
```

Revoke refresh token.

**Arguments**:

- `**kwargs` - Supported [HTTPClient.request()](httpclient.md#request) parameters.
  

**Returns**:

- `dict` - JSON object that contains the response from API.
  

**Raises**:

- `CortexError` - If non-2XX response or 'error' received from API or invalid JSON.

### write\_credentials

```python
write_credentials()
```

Write credentials.

:::info
Write credentials to credentials store.
:::

**Returns**:

  Return value of `self.storage.write_credentials()`.

