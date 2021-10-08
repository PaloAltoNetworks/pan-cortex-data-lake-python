---
sidebar_label: tinydb_adapter
title: adapters.tinydb_adapter
hide_title: true
---
:::info
TinyDB storage adapter.
:::

## TinyDBStore

### fetch\_credential

```python
fetch_credential(credential=None, profile=None)
```

Fetch credential from credentials file.

**Arguments**:

- `credential` _str_ - Credential to fetch.
- `profile` _str_ - Credentials profile. Defaults to ``'default'``.
  

**Returns**:

  str, None: Fetched credential or ``None``.

### remove\_profile

```python
remove_profile(profile=None)
```

Remove profile from credentials file.

**Arguments**:

- `profile` _str_ - Credentials profile to remove.
  

**Returns**:

- `list` - List of affected document IDs.

### write\_credentials

```python
write_credentials(credentials=None, profile=None, cache_token=None)
```

Write credentials.

:::info
Write credentials to credentials file. Performs ``upsert``.
:::

**Arguments**:

- `cache_token` _bool_ - If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
- `credentials` _class_ - Read-only credentials.
- `profile` _str_ - Credentials profile. Defaults to ``'default'``.
  

**Returns**:

- `int` - Affected document ID.

