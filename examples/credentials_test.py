#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example that tests concurrent token refresh support.

Pay special attention to the "NUM_FAILED" which indicates you may have
breached your operating system's supported max number of open files.

You should expect to see only 1 "NUM_SUCCEEDED" no matter how many
threads are specified.

"""

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

NUM_SKIPPED = 0
NUM_SUCCEEDED = 0
NUM_FAILED = 0


class Concurrency(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):

        global NUM_SKIPPED
        global NUM_SUCCEEDED
        global NUM_FAILED

        while True:
            try:
                credentials = self.queue.get()
                token = credentials.access_token
                try:
                    logging.info(
                        "{}: attempting token refresh...".format(
                            current_thread().name
                        )
                    )
                    credentials.refresh(access_token=token)
                except Exception as e:
                    logging.info(e)
                    self.queue.task_done()
                if credentials.access_token != token:
                    NUM_SUCCEEDED += 1
                    logging.info(
                        "{}: REFRESH SUCCEEDED".format(
                            current_thread().name)
                    )
                else:
                    NUM_SKIPPED += 1
                    logging.info(
                        "{}: REFRESH SKIPPED".format(
                            current_thread().name)
                    )
                self.queue.task_done()
            except OSError as e:
                NUM_FAILED += 1
                logging.error("TOO MANY THREADS DEFINED: {}".format(e))
                self.queue.task_done()


c = Credentials()

print(
    "\nACCESS_TOKEN: {}\n".format(c.get_credentials().access_token)
)

q = Queue()
n_threads = 64

for x in range(n_threads):
    worker = Concurrency(q)
    worker.daemon = True
    worker.start()

for _ in range(n_threads):
    q.put(c)

q.join()

print(
    "\nACCESS_TOKEN: {}\n".format(c.get_credentials().access_token)
)

print("NUM_SKIPPED:\t {}/{}".format(NUM_SKIPPED, n_threads))
print("NUM_SUCCEEDED:\t {}/{}".format(NUM_SUCCEEDED, n_threads))
print("NUM_FAILED:\t {}/{}\n".format(NUM_FAILED, n_threads))
