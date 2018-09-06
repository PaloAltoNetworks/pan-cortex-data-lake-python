#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using set_filters."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import EventService, Credentials

url = 'https://api.us.paloaltonetworks.com'

c = Credentials()

# Create Event Service instance
es = EventService(
    url=url,
    credentials=c
)

filters = {  # Prepare 'filter'
    "filters": [
        {"panw.traffic": "SELECT * FROM `panw.traffic`"},
        {"panw.threat": "SELECT * FROM `panw.threat`"}
    ]
}

channel_id = 'EventFilter'

# Set new event filters
f = es.set_filters(channel_id, json=filters)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: \n\n{}\n".format(f.status_code, f.text)
)
