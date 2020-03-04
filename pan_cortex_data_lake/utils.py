# -*- coding: utf-8 -*-

"""PAN Cloud Python SDK utilities."""

from __future__ import absolute_import

import logging  # noqa: F401


class ApiStats(dict):
    """Object for storing, updating and retrieving API stats."""

    def __init__(self, *args, **kwargs):
        super(ApiStats, self).__init__(*args, **kwargs)
        self.transactions = 0
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(ApiStats, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ApiStats, self).__delitem__(key)
        del self.__dict__[key]
