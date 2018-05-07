#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Directory-Sync Service using attributes."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import DirectorySyncService
from pancloud import Credentials

url = 'https://apigw-stg4.us.paloaltonetworks.com'

c = Credentials()

# Create Directory-Sync Service instance
ds = DirectorySyncService(
    url=url,
    credentials=c
)

# Retrieve attributes from directory-sync
a = ds.attributes()

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(a.status_code, a.text)
)



