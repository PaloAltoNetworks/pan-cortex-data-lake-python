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

url = 'https://apigw-stg4.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

session = HTTPClient(
    url=url,
    max_retries=5,
    pool_maxsize=30,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

ls = LoggingService(session=session)
dss = DirectorySyncService(session=session)
es = EventService(session=session)


filters = {  # Prepare 'filter' data
    "filters": [
        {"panw.threat": "SELECT * FROM panw.threat"},
        {"panw.traffic": "SELECT * FROM panw.traffic"},
        {"panw.system": "SELECT * FROM panw.system"},
        {"panw.config": "SELECT * FROM panw.config"}
    ]
}

channel_id = 'EventFilter'

f = es.set_filters(channel_id, filters)
print("\nSET EVENT FILTERS")
print(
    "STATUS_CODE: {}, RESULT: {}".format(f.status_code, f.text)
)

f = es.get_filters(channel_id)
print("\nGET EVENT FILTERS")
print(
    "STATUS_CODE: {}, RESULT: {}\n".format(f.status_code, f.text)
)
