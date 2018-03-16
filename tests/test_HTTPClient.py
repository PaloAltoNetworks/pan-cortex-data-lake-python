#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Requests HTTPClient wrapper."""

from __future__ import division
import json
import os
import pickle
import collections
import contextlib
import warnings

import io
import pytest
import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import httpclient

# from .compat import StringIO, u
# from .utils import override_environ
from urllib3.util import Timeout as Urllib3Timeout
import socket

# Requests to this URL should always fail with a connection timeout (nothing
# listening on that port)
TARPIT = 'http://10.255.255.1'

try:
    from ssl import SSLContext
    del SSLContext
    HAS_MODERN_SSL = True
except ImportError:
    HAS_MODERN_SSL = False

try:
    httpclient.pyopenssl
    HAS_PYOPENSSL = True
except AttributeError:
    HAS_PYOPENSSL = False


class TestHTTPClient:

    def test_entry_points(self):
        pass


