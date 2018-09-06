#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging Service example using write."""

import os
import sys
from uuid import uuid4
from time import time

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import LoggingService, Credentials


VENDOR_ID = 'vendor'
LOG_TYPE = 'log_type'

url = 'https://api.us.paloaltonetworks.com'

c = Credentials()

# Create Logging Service instance
ls = LoggingService(
    url=url,
    credentials=c
)

logs = [
    {
        'generatedTime': time(),
        'uuid': str(uuid4()),
        'user': 'acme/wcoyote',
        'action': 'drop',
        'subType': 'brute-force',
        'name': 'anvil',
        'repeatCnt': 5
    }
]

q = ls.write(vendor_id=VENDOR_ID, log_type=LOG_TYPE, json=logs)

print(
    "\nWRITE: {}\n".format(q.text)
)
