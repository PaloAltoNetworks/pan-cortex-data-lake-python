#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Logging Service using iter_poll."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.logging import LoggingService

url = 'https://apigw-qa6.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Create Logging Service instance
ls = LoggingService(
    url=url,
    verify=False,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

data = {  # Prepare 'query' data
    "q": "select * from panw.traffic limit 1",
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
    "pageNumber": 0,  # initial sequenceNo
    "maxWaitTime": 3000
}

# Poll 'query' for results
for page in ls.iter_poll(query_id, params):
    try:
        print(
            "{}: queryId: {}, pageNumber: {}, retrieving from {},"
            " size: {}, took: {} ms\n".format(
                page.json()['status'],
                page.json()['queryId'],
                page.json()['pageNumber'],
                page.json()['result']['esResult']['from'],
                page.json()['result']['esResult']['size'],
                page.json()['result']['esResult']['took']
            )
        )
    except TypeError:
        print(
            "{}: jobID: {}, sequenceNo: {}".format(
                page.json()['status'],
                page.json()['queryId'],
                page.json()['pageNumber']
            )
        )

# Delete 'job'
d = ls.delete(query_id)

# Print 'delete' results
print(
    "DELETE: {}\n".format(d.text)
)


