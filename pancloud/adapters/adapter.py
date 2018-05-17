# -*- coding: utf-8 -*-

"""Base adapter class."""
from __future__ import absolute_import

from abc import ABCMeta, abstractmethod
import six


@six.add_metaclass(ABCMeta)
class StorageAdapter:
    """A storage adapter abstract base class."""

    @abstractmethod
    def fetch_credential(self, credential=None, profile=None):
        """Fetch credential from store.

        Args:
            credential (str): Credential to fetch.
            profile (str): Credentials profile. Defaults to ``'default'``.

        Returns:
            str, None: Fetched credential or ``None``.

        """
        pass

    @abstractmethod
    def init_store(self):
        """Initialize credentials store."""
        pass

    @abstractmethod
    def remove_profile(self, profile=None):
        """Remove profile from store.

        Args:
            profile (str): Credentials profile to remove.

        Returns:
            int: Result of operation.

        """
        pass

    @abstractmethod
    def write_credentials(self, credentials=None, profile=None,
                          cache_token=None):
        """Write credentials.

        Write credentials to store.

        Args:
            cache_token (bool): If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
            credentials (class): Read-only credentials.
            profile (str): Credentials profile. Defaults to ``'default'``.

        Returns:
            int: Result of operation.

        """
        pass