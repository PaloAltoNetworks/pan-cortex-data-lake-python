#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example interaction with Directory Sync Service using query."""

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

OBJ_CLASS = "users"  # users | computers | containers | groups | ous
DOMAIN = "example.com"  # use domains() method to retrieve available domains

# Retrieve attributes from directory-sync
q = ds.query(object_class=OBJ_CLASS, json={'domain': DOMAIN})

# Print results
print(
    "\nSTATUS_CODE: {}, RESULT: \n\n{}\n".format(q.status_code, q.text)
)
