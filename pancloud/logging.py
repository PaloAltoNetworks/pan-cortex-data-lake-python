# -*- coding: utf-8 -*-

"""Interact with the Application Framework Logging Service API.

The Logging Service is a Palo Alto Networks cloud service which allows
for the storage and retrieval of logging data. Any type of textual
logging data can be stored in the Logging Service. Palo Alto Networks
firewalls and software can write logging data to this service, as can
the software and services created by Palo Alto Network's various
partners.

Examples:
    Refer to the examples provided with this library.

"""

from __future__ import absolute_import
import logging
import time

from .exceptions import PanCloudError, RequiredKwargsError
from .httpclient import HTTPClient


class LoggingService(object):
    """An Application Framework Logging Service Instance."""

    def __init__(self, **kwargs):
        """

        Parameters:
            session (HTTPClient): :class:`~pancloud.httpclient.HTTPClient` object. Defaults to ``None``.
            url (str): URL to send API requests to. Later combined with ``port`` and :meth:`~request` ``path`` parameter.

        Args:
            **kwargs: Supported :class:`~pancloud.httpclient.HTTPClient` parameters.

        """
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
        for k in self.kwargs.get('headers', {}):
            if k.lower() == 'authorization':
                x = dict(self.kwargs['headers'].items())
                x[k] = '*' * 6  # starrify token
                return '{}({}, {})'.format(
                    self.__class__.__name__,
                    ', '.join('%s=%r' % (x, _) for x, _ in
                              self.kwargs.items() if x != 'headers'),
                    'headers=%r' % x
                )
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join(
                '%s=%r' % x for x in self.kwargs.items())
        )

    def delete(self, query_id=None, **kwargs):  # pragma: no cover
        """Delete a query job.

        Uses the DELETE HTTP method to delete a query job. After calling
        this endpoint, it is an error to poll for query results using
        the queryId specified here.

        Args:
            query_id (str): Specifies the ID of the query job.
            **kwargs: Supported :meth:`~pancloud.httpclient.HTTPClient.request` parameters.

        Returns:
            requests.Response: Requests Response() object.

        Examples:
            Refer to ``logging_query.py`` example.

        """
        path = "/logging-service/v1/queries/{}".format(query_id)
        r = self._httpclient.request(
            method="DELETE",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def iter_poll(self, query_id=None, sequence_no=None, params=None,
                  **kwargs):  # pragma: no cover
        """Retrieve pages iteratively in a non-greedy manner.

        Automatically increments the sequenceNo as it continues to poll
        for results until the endpoint reports JOB_FINISHED or
        JOB_FAILED, or an exception is raised by the pancloud library.

        Args:
            params (dict): Payload/request dictionary.
            query_id (str): Specifies the ID of the query job.
            sequence_no (int): Specifies the sequenceNo.
            **kwargs: Supported :meth:`~pancloud.httpclient.HTTPClient.request` parameters.

        Yields:
            requests.Response: Requests Response() object.

        Examples:
            Refer to ``logging_iter_poll.py`` example.

        """
        while True:
            r = self.poll(
                query_id, sequence_no, params, enforce_json=True,
                **kwargs
            )
            if r.json()['queryStatus'] == "FINISHED":
                if sequence_no is not None:
                    sequence_no += 1
                else:
                    sequence_no = 1
                yield r
            elif r.json()['queryStatus'] == "JOB_FINISHED":
                yield r
                break
            elif r.json()['queryStatus'] == "JOB_FAILED":
                yield r
                break
            elif r.json()['queryStatus'] == "RUNNING":
                yield r
                time.sleep(1)
            else:
                raise PanCloudError(
                    'Bad queryStatus: %s' % r.json()['queryStatus']
                )

    def poll(self, query_id=None, sequence_no=None, params=None,
             **kwargs):  # pragma: no cover
        """Poll for asynchronous query results.

        Continue to poll for results until this endpoint reports
        JOB_FINISHED or JOB_FAILED. The results of queries can be
        returned in multiple pages, each of which may contain many log
        records. Use this endpoint to poll for query result batches, as
        well as to track query result status.

        Args:
            params (dict): Payload/request dictionary.
            query_id (str): Specifies the ID of the query job.
            sequence_no (int): Specifies the sequenceNo.
            **kwargs: Supported :meth:`~pancloud.httpclient.HTTPClient.request` parameters.

        Returns:
            requests.Response: Requests Response() object.

        Examples:
            Refer to ``logging_query.py`` example.

        """
        path = "/logging-service/v1/queries/{}/{}".format(
            query_id, sequence_no
        )
        r = self._httpclient.request(
            method="GET",
            url=self.url,
            params=params,
            path=path,
            **kwargs
        )
        return r

    def query(self, data=None, **kwargs):  # pragma: no cover
        """Generate a query that retrieves log records.

        Creates a query within the Logging Service that returns 0 or
        more log records. Query results can be returned in pages,
        depending on the size of your result set. You can retrieve pages
        using :meth:`poll`, :meth:`iter_poll`, :meth:`poll_all` or :meth:`xpoll`.

        Args:
            data (dict): Payload/request dictionary.
            **kwargs: Supported :meth:`~pancloud.httpclient.HTTPClient.request` parameters.

        Returns:
            requests.Response: Requests Response() object.

        Examples:
            Refer to ``logging_query.py`` example.

        """
        path = "/logging-service/v1/queries"
        r = self._httpclient.request(
            method="POST",
            url=self.url,
            data=data,
            path=path,
            **kwargs
        )
        return r

    def xpoll(self, query_id=None, sequence_no=None, params=None,
              delete_query=True, **kwargs):  # pragma: no cover
        """Retrieve individual logs iteratively in a non-greedy manner.

        Generator function to return individual log entries from poll
        API request.

        Args:
            params (dict): Payload/request dictionary.
            query_id (str): Specifies the ID of the query job.
            sequence_no (int): Specifies the sequenceNo.
            delete_query (bool): True for delete, False otherwise.
            **kwargs: Supported :meth:`~pancloud.httpclient.HTTPClient.request` parameters.

        Yields:
            dictionary with single log entry.

        """
        def _delete(query_id, **kwargs):
            r = self.delete(query_id, **kwargs)
            try:
                r_json = r.json()
            except ValueError as e:
                raise PanCloudError('Invalid JSON: %s' % e)

            if not (200 <= r.status_code < 300):
                if 'errorCode' in r_json and 'errorMessage' in r_json:
                    raise PanCloudError('%s: %s' %
                                        (r_json['errorCode'],
                                         r_json['errorMessage']))
                else:
                    raise PanCloudError('%s %s' % (r.status_code,
                                                   r.reason))

            if r.status_code == 200:
                return
            else:
                raise PanCloudError('delete: status_code: %d' %
                                    r.status_code)

        r = self.poll(query_id, sequence_no, params, **kwargs)
        try:
            r_json = r.json()
        except ValueError as e:
            raise PanCloudError('Invalid JSON: %s' % e)

        if not (200 <= r.status_code < 300):
            if 'errorCode' in r_json and 'errorMessage' in r_json:
                raise PanCloudError('%s: %s' %
                                    (r_json['errorCode'],
                                     r_json['errorMessage']))
            else:
                raise PanCloudError('%s %s' % (r.status_code,
                                               r.reason))

        if 'queryStatus' not in r_json:
            self._debug(r_json)
            raise PanCloudError('no "queryStatus" in response')

        self._debug(r_json['queryStatus'])
        if r_json['queryStatus'] in ['FINISHED', 'JOB_FINISHED']:
            try:
                hits = r_json['result']['esResult']['hits']['hits']
            except KeyError as e:
                raise PanCloudError('no "hits" in response' % e)

            self._debug('hits: %d', len(hits))
            for x in hits:
                yield x['_source']

            if r_json['queryStatus'] == 'JOB_FINISHED':
                if delete_query:
                    _delete(query_id, **kwargs)
                return

            if sequence_no is not None:
                sequence_no += 1
            else:
                sequence_no = 1

        elif r_json['queryStatus'] == 'JOB_FAILED':
            raise PanCloudError('%s: %s: %s' %
                                (r_json['queryStatus'],
                                 r_json['errorCode'],
                                 r_json['errorMessage']))

        elif r_json['queryStatus'] == 'RUNNING':
            if 'maxWaitTime' in params:
                pass
            else:
                # XXX
                time.sleep(1)
        else:
            raise PanCloudError('Bad queryStatus: %s' % r_json['queryStatus'])

        # recursion
        for x in self.xpoll(query_id, sequence_no, params, delete_query,
                            **kwargs):
            yield x
