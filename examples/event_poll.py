#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using poll."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import EventService

url = 'https://apigw-stg4.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Create Event Service instance
es = EventService(
    url=url,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

channel_id = 'EventFilter'

# Poll event channel
p = es.poll(channel_id)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(p.status_code, p.text)
)


