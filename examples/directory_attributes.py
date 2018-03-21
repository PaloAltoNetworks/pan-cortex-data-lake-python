#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Directory-Sync Service using attributes."""

import os
import sys

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud.directorysync import DirectorySyncService

url = 'https://api.us.paloaltonetoworks.com'

# `export ACCESS_TOKEN=<access token>`
access_token = os.environ['ACCESS_TOKEN']

# Create Directory-Sync Service instance
ds = DirectorySyncService(
    url=url,
    headers={
        'Authorization': 'Bearer {}'.format(access_token),
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

# Retrieve attributes from directory-sync
a = ds.attributes()

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: {}\n".format(a.status_code, a.text)
)



