# -*- coding: utf-8 -*-

"""Interact with the Application Framework Event Service API.

The Event Service allows your application to consume log data using a
subscription (pull) model. When a customer activates your application in
the Cloud Services Portal, a channel is assigned to it. This channel is
dedicated to the customer's application instance. The channel will
contain no data for any other customer,or any other application
instance. You will receive this channel's ID as a part of the process
that provisions your app for the customer in Palo Alto Network's
Application Framework.

Examples:
    Refer to the examples provided with this library and/or the official
    Reference Application.

"""

from __future__ import absolute_import
import logging

from .exceptions import RequiredKwargsError
from .httpclient import HTTPClient


class EventService(object):
    """An Application Framework Event Service Instance."""

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

    def ack(self, channel_id=None, **kwargs):
        """Send a read acknowledgment to the service.

        Causes the channel's start position to move to the channel's
        current read position.

        Args:
            channel_id (str): The channel ID
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to event_ack.py example.

        """
        path = "/event-service/v1/channels/{}/ack".format(channel_id)
        r = self._httpclient.request(
            method="POST",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def get_filters(self, channel_id=None, **kwargs):
        """Retrieve the filters currently set on the channel.

        Returns filters set using the "Set Filters" endpoint. The
        response body contains a JSON object with a singlefield:
        "filters". This field provides a JSON array of JSON objects.
        Each object identifies a log type and a filter.

        Args:
            channel_id (str): The channel ID
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to event_get_filters.py example.

        """
        path = "/event-service/v1/channels/{}/filters".format(
            channel_id
        )
        r = self._httpclient.request(
            method="GET",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def nack(self, channel_id=None, **kwargs):
        """Send a negative read-acknowledgement to the service.

        Causes the channel's read point to move to its previous position
        prior to the last poll.

        Args:
            channel_id (str): The channel ID
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to event_nack.py example.

        """
        path = "/event-service/v1/channels/{}/nack".format(channel_id)
        r = self._httpclient.request(
            method="POST",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def poll(self, channel_id=None, **kwargs):
        """Read one or more events from a channel.

        Reads events (log records) from the identified channel. Events
        are read in chronological order.

        Args:
            channel_id (str): The channel ID
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to event_poll.py example.

        """
        path = "/event-service/v1/channels/{}/poll".format(channel_id)
        r = self._httpclient.request(
            method="POST",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def set_filters(self, channel_id=None, data=None, **kwargs):
        """Set one or more filters for the channel.

        Configures one or more filters for a channel. The filters
        specified by this API override any previously-configured
        filters.

        Args:
            channel_id (str): The channel ID
            data (dict): Payload/request dictionary
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to event_set_filters.py example.

        """
        path = "/event-service/v1/channels/{}/filters".format(
            channel_id
        )
        r = self._httpclient.request(
            method="PUT",
            url=self.url,
            data=data,
            path=path,
            **kwargs
        )
        return r

