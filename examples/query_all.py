#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Query Service example SDK usage."""

import os
import sys
import time

# Necessary to reference cortex package in relative path
curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import QueryService, Credentials

url = "https://cortex-stg5.us.stg.cdl.pan.run"  # stg5
CERT = os.environ["PAN_CERT_PATH"]
KEY = os.environ["PAN_KEY_PATH"]

# Create Logging Service instance
qs = QueryService(url=url, cert=(CERT, KEY), verify=False, force_trace=True)

# SQL = 'SELECT * FROM `2020001.firewall.traffic` LIMIT 100'
SQL = "SELECT * FROM `587718190.firewall.traffic` LIMIT 5"

# Generate new 'query'
query_params = {"language": "bigquery", "query": SQL}

now = int(time.time())  # used for createdAfter

q = qs.create_query(query_params=query_params)

print("QUERY Params: {}\n".format(query_params))

print("QUERY HTTP STATUS CODE: {}\n".format(q.status_code))

print("QUERY Response: {}\n".format(q.text))

job_id = q.json()["jobId"]  # access 'jobId' from 'query' response

# List jobs

l = qs.list_jobs(created_after=now, tenant_id="2020001")

print("LIST HTTP STATUS CODE: {}\n".format(l.status_code))

print("LIST Response: {}\n".format(l.text))

# Get job details
j = qs.get_job(job_id=job_id)

print("JOB HTTP STATUS CODE: {}\n".format(j.status_code))

print("JOB Response: {}\n".format(j.text))

# Get job results
results = qs.get_job_results(job_id=job_id)

print("RESULTS HTTP STATUS CODE: {}\n".format(results.status_code))

print("RESULTS Response: {}\n".format(results.text))

# Iterate through job results (pages)
# Need to settle on a generic name for this method.
print("Iterate through job results: \n")
for p in qs.iter_job_results(job_id=job_id, page_size=1):
    print("RESULTS: {}\n".format(p.text))

print("STATS: {}".format(qs.stats))
