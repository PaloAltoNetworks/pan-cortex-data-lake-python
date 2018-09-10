#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Directory Sync Service using domains."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import DirectorySyncService, Credentials

url = 'https://api.us.paloaltonetworks.com'

c = Credentials()

# Create Directory-Sync Service instance
ds = DirectorySyncService(
    url=url,
    credentials=c
)

# Retrieve domains
d = ds.domains()

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: \n\n{}\n".format(d.status_code, d.text)
)
