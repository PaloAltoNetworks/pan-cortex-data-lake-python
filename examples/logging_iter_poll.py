#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Logging Service using iter_poll."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import LoggingService, Credentials

url = 'https://api.us.paloaltonetworks.com'

c = Credentials()

# Create Logging Service instance
ls = LoggingService(
    url=url,
    credentials=c
)

query = {  # Prepare 'query' data
    "query": "SELECT * FROM panw.traffic LIMIT 5",
    "startTime": 0,  # 1970
    "endTime": 1609459200,  # 2021
    "maxWaitTime": 0  # no logs in initial response
}

# Generate new 'query'
q = ls.query(json=query)

print(
    "\nQUERY: {}\n".format(q.text)
)

query_id = q.json()['queryId']  # access 'queryId' from 'query' response

params = {  # Prepare 'poll' params
    "maxWaitTime": 3000
}

# Poll 'query' for results
for page in ls.iter_poll(query_id, 0, params):
    try:
        print(
            "{}: queryId: {}, sequenceNo: {}, retrieving from {},"
            " size: {}, took: {} ms\n".format(
                page.json()['queryStatus'],
                page.json()['queryId'],
                page.json()['sequenceNo'],
                page.json()['result']['esResult']['from'],
                page.json()['result']['esResult']['size'],
                page.json()['result']['esResult']['took']
            )
        )
    except TypeError:
        print(
            "{}: queryId: {}, sequenceNo: {}".format(
                page.json()['queryStatus'],
                page.json()['queryId'],
                page.json()['sequenceNo']
            )
        )

# Delete 'job'
d = ls.delete(query_id)

# Print 'delete' results
print(
    "DELETE: {}\n".format(d.text)
)
