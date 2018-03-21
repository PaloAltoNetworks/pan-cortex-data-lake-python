#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for DirectorySyncService."""

import os
import sys

import pytest

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.directorysync import DirectorySyncService
from pancloud.httpclient import HTTPClient
from pancloud.exceptions import RequiredKwargsError, \
    UnexpectedKwargsError


TARPIT = os.environ.get('TARPIT', 'http://10.255.255.1')


class TestDirectorySyncService:

    def test_entry_points(self):

        DirectorySyncService(url=TARPIT).session
        DirectorySyncService(url=TARPIT).kwargs
        DirectorySyncService(url=TARPIT).url
        DirectorySyncService(url=TARPIT).attributes
        DirectorySyncService(url=TARPIT).query
        DirectorySyncService(url=TARPIT).domains
        DirectorySyncService(url=TARPIT).count


    def test_required_kwargs(self):
        with pytest.raises(RequiredKwargsError):
            DirectorySyncService()

        with pytest.raises(RequiredKwargsError):
            DirectorySyncService(session=None)

    def test_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            DirectorySyncService(url=TARPIT, foo='foo')

    def test_session(self):
        session = HTTPClient(url=TARPIT)
        DirectorySyncService(session=session)
