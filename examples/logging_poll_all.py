#!/usr/bin/env python

"""Example interaction with Logging Service using poll_all."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.logging import LoggingService

url = 'https://apigw-qa6.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Instantiate QueryService
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
    "q": "select * from panw.traffic limit 1000",
    "startTime": 0,  # 1970
    "endTime": 1609459200,  # 2021
    "maxWaitTime": 0  # no logs in initial response
}

# Generate new 'query'
q = ls.query(data)

print(
    "\nQUERY: {}\n".format(q.text)
)

query_id = q.json()['queryId']  # access 'jobId' from 'query' response

params = {  # Prepare 'poll' params
    "sequenceNo": 0,
    "maxWaitTime": 1
}

# Poll 'job' for all results
all_chunks = ls.poll_all(query_id, params)
print("ALL_CHUNKS: {}\n".format(all_chunks))


# Delete 'job'
d = ls.delete(query_id)

# Print 'delete' results
print(
    "DELETE: {}\n".format(d.text)
)


