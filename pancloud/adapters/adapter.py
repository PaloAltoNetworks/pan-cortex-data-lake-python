# -*- coding: utf-8 -*-

"""Base adapter class."""
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import six


@six.add_metaclass(ABCMeta)
class StorageAdapter:

    @abstractmethod
    def fetch_credential(self, credential=None, profile=None):
        pass

    @abstractmethod
    def init_store(self):
        pass

    @abstractmethod
    def remove_profile(self, profile=None):
        pass

    @abstractmethod
    def write_credentials(self, credentials=None, profile=None,
                          cache_token=None):
        pass
