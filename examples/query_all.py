#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Query Service example SDK usage."""

import os
import sys
import time
import logging

# Necessary to reference cortex package in relative path
curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pan_cortex_data_lake import Credentials, QueryService

url = "https://api.us.cdl.paloaltonetworks.com"  # prod us

# Create Credentials instance
# export PAN_DEVELOPER_TOKEN for quick access
c = Credentials()

# Create Query Service instance
qs = QueryService(url=url, force_trace=True, credentials=c)

# SQL = 'SELECT * FROM `2020001.firewall.traffic` LIMIT 100'
SQL = "SELECT * FROM `4199400902993631660.firewall.traffic` LIMIT 1"

# Generate new 'query'
query_params = {"query": SQL}

q = qs.create_query(query_params=query_params)

print("QUERY Params: {}\n".format(query_params))

print("QUERY HTTP STATUS CODE: {}\n".format(q.status_code))

print("QUERY Response: {}\n".format(q.text))

job_id = q.json()["jobId"]  # access 'jobId' from 'query' response

# Iterate through job results (pages)
print("Iterate through job results: \n")
for p in qs.iter_job_results(job_id=job_id, result_format="valuesDictionary"):
    print("RESULTS: {}\n".format(p.text))

print("STATS: {}".format(qs.stats))
