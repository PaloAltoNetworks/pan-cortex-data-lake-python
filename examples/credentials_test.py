#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example that tests thread-lock during refresh."""

import os
import sys
from threading import Thread, current_thread
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
import logging

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
ch.setFormatter(formatter)
root.addHandler(ch)

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import Credentials


class Concurrency(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            refresh, token = self.queue.get()
            try:
                logging.info(
                    "{}: attempting token refresh...".format(
                        current_thread().name
                    )
                )
                refresh(access_token=token)
            except Exception as e:
                logging.info(e)
                self.queue.task_done()
            if c.get_credentials().access_token:
                logging.info(
                    "{}: REFRESH SUCCEEDED".format(
                        current_thread().name)
                )
            else:
                logging.info(
                    "{}: REFRESH SKIPPED".format(
                        current_thread().name)
                )
            self.queue.task_done()


c = Credentials()

q = Queue()
n_threads = 8
for x in range(n_threads):
    worker = Concurrency(q)
    worker.daemon = True
    worker.start()
for _ in range(n_threads):
    q.put((c.refresh, c.get_credentials().access_token))
q.join()

credentials = c.get_credentials()

print(
    "\nACCESS_TOKEN: {}\n".format(credentials.access_token)
)
