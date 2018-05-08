#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using nack."""

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

channel_id = 'EventFilter'

# NACK event channel
n = es.nack(channel_id)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(n.status_code, n.text)
)


