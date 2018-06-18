#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Logging Service example using write."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import LoggingService
from pancloud import Credentials


VENDOR_ID = 'panw'
LOG_TYPE = 'threat'

url = 'https://apigw-stg4.us.paloaltonetworks.com'

c = Credentials()

# Create Logging Service instance
ls = LoggingService(
    url=url,
    credentials=c
)

data = [
    {
        'generatedTime': 0,
        'uuid': 1,
        'user': 'acme/wcoyote',
        'action': 'drop',
        'type': 'vulnerability',
        'subType': 'brute-force',
        'name': 'anvil',
        'repeatCnt': 5
    }
]

q = ls.write(vendor_id=VENDOR_ID, log_type=LOG_TYPE, data=data)

print(
    "\nWRITE: {}\n".format(q.text)
)
