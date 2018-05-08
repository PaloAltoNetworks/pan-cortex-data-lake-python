#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using set_filters."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import EventService
from pancloud import Credentials

url = 'https://apigw-stg4.us.paloaltonetworks.com'

c = Credentials()

# Create Event Service instance
es = EventService(
    url=url,
    credentials=c
)

data = {  # Prepare 'filter' data
    "filters": [
        {"panw.threat": "SELECT * FROM `panw.threat`"},
        {"panw.traffic": "SELECT * FROM `panw.traffic`"},
        {"panw.system": "SELECT * FROM `panw.system`"},
        {"panw.config": "SELECT * FROM `panw.config`"}
    ]
}

channel_id = 'EventFilter'

# Set new event filters
f = es.set_filters(channel_id, data)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(f.status_code, f.text)
)


