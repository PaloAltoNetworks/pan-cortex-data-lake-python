#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for LoggingService."""

import os
import sys

import pytest

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.logging import LoggingService
from pancloud.httpclient import HTTPClient
from pancloud.exceptions import RequiredKwargsError, \
    UnexpectedKwargsError, HTTPError


HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org')
TARPIT = os.environ.get('TARPIT', 'http://10.255.255.1')


class TestLoggingService:

    def test_entry_points(self):

        LoggingService(url=TARPIT).session
        LoggingService(url=TARPIT).kwargs
        LoggingService(url=TARPIT).url
        LoggingService(url=TARPIT).poll
        LoggingService(url=TARPIT).query
        LoggingService(url=TARPIT).delete
        LoggingService(url=TARPIT).iter_poll
        LoggingService(url=TARPIT).xpoll

    def test_required_kwargs(self):
        with pytest.raises(RequiredKwargsError):
            LoggingService()

        with pytest.raises(RequiredKwargsError):
            LoggingService(session=None)

    def test_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            LoggingService(url=TARPIT, foo='foo')

    def test_session(self):
        session = HTTPClient(url=TARPIT)
        LoggingService(session=session)
