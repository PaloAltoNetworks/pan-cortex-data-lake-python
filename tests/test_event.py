#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for EventService."""

import os
import sys

import pytest

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.event import EventService
from pancloud.httpclient import HTTPClient
from pancloud.exceptions import RequiredKwargsError, \
    UnexpectedKwargsError


TARPIT = os.environ.get('TARPIT', 'http://10.255.255.1')


class TestEventService:

    def test_entry_points(self):

        EventService(url=TARPIT).session
        EventService(url=TARPIT).kwargs
        EventService(url=TARPIT).url
        EventService(url=TARPIT).get_filters
        EventService(url=TARPIT).set_filters
        EventService(url=TARPIT).poll
        EventService(url=TARPIT).ack
        EventService(url=TARPIT).nack

    def test_required_kwargs(self):
        with pytest.raises(RequiredKwargsError):
            EventService()

        with pytest.raises(RequiredKwargsError):
            EventService(session=None)

    def test_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            EventService(url=TARPIT, foo='foo')

    def test_session(self):
        session = HTTPClient(url=TARPIT)
        EventService(session=session)
