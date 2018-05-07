#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example using shared HTTPClient session."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import HTTPClient
from pancloud import LoggingService
from pancloud import EventService
from pancloud import DirectorySyncService
from pancloud import Credentials

url = 'https://apigw-stg4.us.paloaltonetworks.com'

c = Credentials()  # read from ~/.config/pancloud/credentials

session = HTTPClient(
    url=url,
    credentials=c
)

ls = LoggingService(session=session)
dss = DirectorySyncService(session=session)
es = EventService(session=session)

f = es.get_filters('EventFilter')
print("\nGET EVENT FILTERS")
print(
    "STATUS_CODE: {}, RESULT: {}".format(f.status_code, f.text)
)

a = dss.attributes()
print("\nGET ATTRIBUTES")
print(
    "STATUS_CODE: {}, RESULT: {}".format(a.status_code, a.text)
)

data = {  # Prepare 'query' data
    "query": "select * from panw.traffic limit 1",
    "startTime": 0,  # 1970
    "endTime": 1609459200,  # 2021
    "maxWaitTime": 0  # no logs in initial response
}
q = ls.query(data)
print("\nQUERY LOGS")
print(
    "STATUS_CODE: {}, RESULT: {}".format(q.status_code, q.text)
)
