#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging Service example using query, poll, delete."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import LoggingService
from pancloud import Credentials

url = 'https://apigw-stg4.us.paloaltonetworks.com'

c = Credentials()

# Create Logging Service instance
ls = LoggingService(
    url=url,
    credentials=c
)

data = {  # Prepare 'query' data
    "query": "select * from panw.traffic limit 1",
    "startTime": 0,  # 1970
    "endTime": 1609459200,  # 2021
    "maxWaitTime": 0  # no logs in initial response
}

# Generate new 'query'
q = ls.query(data)

print(
    "\nQUERY: {}\n".format(q.text)
)

query_id = q.json()['queryId']  # access 'queryId' from 'query' response

params = {  # Prepare 'poll' params
    "maxWaitTime": 3000
}

# Poll 'query' for results
p = ls.poll(query_id, 0, params)

try:
    print(
        "{}: queryId: {}, sequenceNo: {}, retrieving from {}, size: {},"
        " took: {} ms\n\nRESULT: {}\n".format(
            p.json()['queryStatus'],
            p.json()['queryId'],
            p.json()['sequenceNo'],
            p.json()['result']['esResult']['from'],
            p.json()['result']['esResult']['size'],
            p.json()['result']['esResult']['took'],
            p.text,
        )
    )
except TypeError:
    print(
        "{}: queryId: {}, sequenceNo: {}".format(
            p.json()['queryStatus'],
            p.json()['queryId'],
            p.json()['sequenceNo'],
        )
    )

# Delete 'job'
d = ls.delete(query_id)

# Print 'delete' results
print(
    "DELETE: {}\n".format(d.text)
)

