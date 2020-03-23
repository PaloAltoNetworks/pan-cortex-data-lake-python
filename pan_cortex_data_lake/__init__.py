# -*- coding: utf-8 -*-

"""Main package for cortex."""

__author__ = "Palo Alto Networks"
__version__ = "2.0.0-a7"

from .exceptions import (  # noqa: F401
    CortexError,
    HTTPError,
    UnexpectedKwargsError,
    RequiredKwargsError,
)
from .httpclient import HTTPClient  # noqa: F401
from .credentials import Credentials  # noqa: F401
from .query import QueryService  # noqa: F401
