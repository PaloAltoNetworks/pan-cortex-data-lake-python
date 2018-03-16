#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using set_filters."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.event import EventService

url = 'https://apigw-qa6.us.paloaltonetworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Create Event Service instance
es = EventService(
    url=url,
    verify=False,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

data = {  # Prepare 'filter' data
    "filters": [
        {"panw.threat": "SELECT * FROM panw.threat"},
        {"panw.traffic": "SELECT * FROM panw.traffic"},
        {"panw.system": "SELECT * FROM panw.system"},
        {"panw.config": "SELECT * FROM panw.config"}
    ]
}

channel_id = 'EventFilter'

# Set new event filters
f = es.set_filters(channel_id, data)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(f.status_code, f.text)
)


