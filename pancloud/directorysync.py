# -*- coding: utf-8 -*-

"""Interact with the Application Framework Directory-Sync Service API.

To obtain rich information about users and devices for the purposes of
reporting and policy enforcement, cloud-based applications need access
to directory information. However, most directories are located
on-premise so they cannot be accessed by cloud-based applications.
The Directory Sync Service allows cloud-based applications to access
directory data by using an on-premise agent to collect it, and then
transferring the data to the cloud-based Directory Sync Service.

Examples:
    Refer to the examples provided with this library and/or the official
    Reference Application.

"""

from __future__ import absolute_import
import logging

from .exceptions import RequiredKwargsError
from .httpclient import HTTPClient


class DirectorySyncService(object):
    """An Application Framework Directory-Sync Service Instance."""

    def __init__(self, **kwargs):
        self.kwargs = kwargs.copy()  # used for __repr__
        self.session = kwargs.pop('session', None)
        if isinstance(self.session, HTTPClient):
            self.url = kwargs.pop('url', None) or self.session.url
        else:
            self.url = kwargs.pop('url', None)
        if self.url is None:
            raise RequiredKwargsError('url')
        self._httpclient = self.session or HTTPClient(**kwargs)
        self._debug = logging.getLogger(__name__).debug

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('%s=%r' % x for x in self.kwargs.items())
        )

    def attributes(self, **kwargs):
        """Retrieve the attribute configuration object.

        Retrieves a mapping that identifies the custom directory
        attributes configured for the Directory SyncService instance,
        and the mapping of the custom attributes to standard directory
        attributes.

        Args:
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to directory_attributes.py example.

        """
        path = "/directory-sync-service/v1/attributes"
        r = self._httpclient.request(
            method="GET",
            path=path,
            url=self.url,
            **kwargs
        )
        return r

    def count(self, object_class=None, **kwargs):
        """Retrieve the attribute configuration object.

        Retrieve a count of all directory entries that belong to the
        identified objectClass. The count is limited toa single domain.

        Args:
            object_class (str): Directory object class
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Coming soon.

        """
        path = "/directory-sync-service/v1/{}/count".format(
            object_class
        )
        r = self._httpclient.request(
            method="GET",
            path=path,
            url=self.url,
            **kwargs
        )
        return r

    def domains(self, **kwargs):
        """Retrieves a list of all domains available.

        Directory Sync Service can be configured to read directory
        entries from multiple domains. This API retrieves all the
        domains from which your Directory Sync Service instance is
        configured to read entries. Domains areidentified in both DNS
        and distinguished name format.

        Args:
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Coming soon.

        """
        path = "/directory-sync-service/v1/domains"
        r = self._httpclient.request(
            method="GET",
            path=path,
            url=self.url,
            **kwargs
        )
        return r

    def query(self, object_class=None, data=None, **kwargs):
        """Query data stored in directory.

        Retrieves directory data by querying a Directory Sync Service
        cloud-based instance. The directory data isstored with the
        Directory Sync Service instance using an agent that is installed
        in the customer's network.This agent retrieves directory data
        from the customer's Active Directory, and then sends it to the
        cloud-based Directory Sync Service instance.

        Args:
            object_class (str): Directory object class
            data (dict): Payload/request dictionary
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Coming soon.

        """
        path = "/directory-sync-service/v1/{}".format(object_class)
        r = self._httpclient.request(
            method="POST",
            url=self.url,
            data=data,
            path=path,
            **kwargs
        )
        return r
