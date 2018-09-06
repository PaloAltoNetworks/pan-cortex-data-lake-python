#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Event Service using ack."""

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

channel_id = 'EventFilter'

# ACK event channel
a = es.ack(channel_id)

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: \n\n{}\n".format(a.status_code, a.text)
)
