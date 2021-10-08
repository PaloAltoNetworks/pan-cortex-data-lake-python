---
sidebar_label: exceptions
title: exceptions
hide_title: true
---
import TOCInline from '@theme/TOCInline';

<TOCInline toc={toc} />;
:::info
This module provides base classes for all errors raised by the PAN Cloud
library. All other exceptions are raised and maintained by Python
standard or nonstandard libraries.
:::

## CortexError

Base class for all exceptions raised by PAN Cloud library.

### \_\_init\_\_

```python
__init__(message)
```

Override the base class message attribute.

**Arguments**:

- `message` _str_ - Exception message.

## HTTPError

A pancloud HTTP error occurred.

### \_\_init\_\_

```python
__init__(inst)
```

Convert exception instance to string.

**Arguments**:

- `inst` _class_ - Exception instance.

## PartialCredentialsError

The required credentials were not supplied.

### \_\_init\_\_

```python
__init__(inst)
```

Convert exception instance to string.

**Arguments**:

- `inst` _class_ - Exception instance.

## RequiredKwargsError

A required keyword argument was not passed.

### \_\_init\_\_

```python
__init__(kwarg)
```

Capture missing key-word argument.

**Arguments**:

- `kwarg` _str_ - Key-word argument.

## UnexpectedKwargsError

An unexpected keyword argument was passed.

### \_\_init\_\_

```python
__init__(kwargs)
```

Convert kwargs to CSV string.

**Arguments**:

- `kwargs` _dict_ - Key-word arguments.

