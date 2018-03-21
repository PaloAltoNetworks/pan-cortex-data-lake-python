#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using ack."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.event import EventService

url = 'https://api.us.paloaltonetoworks.com'

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

# ACK event channel
a = es.ack(channel_id)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(a.status_code, a.text)
)


