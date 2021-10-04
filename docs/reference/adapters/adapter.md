---
sidebar_label: adapter
title: adapters.adapter
hide_title: true
---
:::info
Base adapter class.
:::

## StorageAdapter

A storage adapter abstract base class.

### fetch\_credential

```python
@abstractmethod
fetch_credential(credential=None, profile=None)
```

Fetch credential from store.

**Arguments**:

- `credential` _str_ - Credential to fetch.
- `profile` _str_ - Credentials profile. Defaults to ``&#x27;default&#x27;``.

### init\_store

```python
@abstractmethod
init_store()
```

Initialize credentials store.

### remove\_profile

```python
@abstractmethod
remove_profile(profile=None)
```

Remove profile from store.

**Arguments**:

- `profile` _str_ - Credentials profile to remove.

### write\_credentials

```python
@abstractmethod
write_credentials(credentials=None, profile=None, cache_token=None)
```

Write credentials.

:::info
Write credentials to store.
:::

**Arguments**:

- `cache_token` _bool_ - If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
- `credentials` _class_ - Read-only credentials.
- `profile` _str_ - Credentials profile. Defaults to ``&#x27;default&#x27;``.

