#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for LoggingService."""

import os
import sys

import pytest

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pan_cortex_data_lake.query import QueryService
from pan_cortex_data_lake.httpclient import HTTPClient
from pan_cortex_data_lake.exceptions import UnexpectedKwargsError


HTTPBIN = os.environ.get("HTTPBIN_URL", "http://httpbin.org")
TARPIT = os.environ.get("TARPIT", "http://10.255.255.1")


class TestQueryService:
    def test_entry_points(self):

        QueryService(url=TARPIT).session
        QueryService(url=TARPIT).kwargs
        QueryService(url=TARPIT).url
        QueryService(url=TARPIT).cancel_job
        QueryService(url=TARPIT).create_query
        QueryService(url=TARPIT).get_job
        QueryService(url=TARPIT).get_job_results
        QueryService(url=TARPIT).iter_job_results
        QueryService(url=TARPIT).list_jobs

    def test_unexpected_kwargs(self):
        with pytest.raises(UnexpectedKwargsError):
            QueryService(url=TARPIT, foo="foo")

    def test_session(self):
        session = HTTPClient(url=TARPIT)
        QueryService(session=session)
