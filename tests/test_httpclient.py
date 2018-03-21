#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for Requests HTTPClient wrapper."""

import os
import sys

import pytest

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.httpclient import HTTPClient
from pancloud.exceptions import HTTPError, RequiredKwargsError, \
    UnexpectedKwargsError


HTTPBIN = os.environ.get('HTTPBIN_URL', 'http://httpbin.org')
TARPIT = os.environ.get('TARPIT', 'http://10.255.255.1')


class TestHTTPClient:

    def test_entry_points(self):

        HTTPClient(url=TARPIT).request

    def test_invalid_url(self):
        with pytest.raises(HTTPError):
            HTTPClient(url='asdaksjhdakjsdh').request(method='GET')
        with pytest.raises(HTTPError):
            HTTPClient(url='http://').request(method='GET')

    def test_required_kwargs(self):
        with pytest.raises(RequiredKwargsError):
            HTTPClient().request()

    def test_connection_timeout(self):
        with pytest.raises(HTTPError):
            HTTPClient(url=TARPIT).request(
                method='GET', timeout=(.1, None)
            )

    def test_read_timeout(self):
        with pytest.raises(HTTPError):
            HTTPClient(url=HTTPBIN, port=80).request(
                method='GET', timeout=(None, .0001), path='/'
            )

    def test_httpclient_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            HTTPClient(url=TARPIT, foo='foo').request(method='GET')

    def test_request_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            HTTPClient(url=TARPIT).request(method='GET', foo='foo')

    def test_enforce_json(self):
        with pytest.raises(HTTPError):
            HTTPClient(
                url=HTTPBIN,
                port=80,
                enforce_json=True,
                headers={'Accept': 'application/json'}
            ).request(method='GET', path='/')

    def test_raise_for_status(self):
        with pytest.raises(HTTPError):
            HTTPClient(
                url=HTTPBIN,
                port=80,
                raise_for_status=True
            ).request(method='GET', path='/status/400')



