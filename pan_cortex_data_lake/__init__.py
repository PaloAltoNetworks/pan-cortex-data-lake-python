# -*- coding: utf-8 -*-

"""Main package for cortex."""

__author__ = "Palo Alto Networks"
__version__ = "2.0.0b1"
__description__ = "Python idiomatic SDK for Cortex™ Data Lake."

from .exceptions import (  # noqa: F401
    CortexError,
    HTTPError,
    UnexpectedKwargsError,
    RequiredKwargsError,
)
from .httpclient import HTTPClient  # noqa: F401
from .credentials import Credentials  # noqa: F401
from .query import QueryService  # noqa: F401
