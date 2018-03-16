# -*- coding: utf-8 -*-

"""Interact with the Application Framework Logging Service API.

The Logging Service is a Palo Alto Networks cloud service which allows
for the storage and retrieval of logging data. Any type of textual
logging data can be stored in the Logging Service. Palo Alto Networks
firewalls and software can write logging data to this service, as can
the software and services created by Palo Alto Network's various
partners.

Examples:
    Refer to the examples provided with this library and/or the official
    Reference Application.

"""

from __future__ import absolute_import
import logging
import time

from .exceptions import PanCloudError, RequiredKwargsError
from .httpclient import HTTPClient


class LoggingService(object):
    """An Application Framework Logging Service Instance."""

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

    def delete(self, query_id=None, **kwargs):
        """Delete a query job.

        Uses the DELETE HTTP method to delete a query job. After calling
        this endpoint, it is an error to poll for query results using
        the queryId specified here.

        Args:
            query_id (str): Specifies the ID of the query job
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        """
        path = "/logging-service/v1/queries/{}".format(query_id)
        r = self._httpclient.request(
            method="DELETE",
            url=self.url,
            path=path,
            **kwargs
        )
        return r

    def iter_poll(self, query_id=None, params=None, **kwargs):
        """Retrieve pages iteratively in a non-greedy manner.

        Automatically increments the pageNumber as it continues to poll
        for results until the endpoint reports JOB_FINISHED or
        JOB_FAILED, or an exception is raised by the pancloud library.

        Args:
            params (dict): Payload/request dictionary
            query_id (str): Specifies the ID of the query job
            **kwargs: Supported Request() and Session() kwargs

        Yields:
            requests.Response: requests Response() object

        """
        while True:
            r = self.poll(query_id, params, **kwargs)
            if r.json()['status'] == "FINISHED":
                params['pageNumber'] += 1
                yield r
            elif r.json()['status'] == "JOB_FINISHED":
                yield r
                break
            elif r.json()['status'] == "JOB_FAILED":
                yield r
                break
            else:  # query status ostensibly == 'RUNNING'
                yield r
                time.sleep(1)  # wait before trying again

    def poll(self, query_id=None, params=None, **kwargs):
        """Poll for asynchronous query results.

        Continue to poll for results until this endpoint reports
        JOB_FINISHED or JOB_FAILED. The results of queries can be
        returned in multiple pages, each of which may contain many log
        records. Use this endpoint to poll for query result batches, as
        well as to track query result status.

        Args:
            params (dict): Payload/request dictionary
            query_id (str): Specifies the ID of the query job
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        """
        path = "/logging-service/v1/queries/{}".format(query_id)
        r = self._httpclient.request(
            method="GET",
            url=self.url,
            params=params,
            path=path,
            **kwargs
        )
        return r

    def poll_all(self, query_id=None, params=None, **kwargs):
        """Retrieve pages iteratively in a greedy manner.

        Automatically increments the pageNumber as it continues to poll
        for results until the endpoint reports JOB_FINISHED or
        JOB_FAILED, or an exception is raised by the pancloud library.

        WARNING: Be mindful of memory consumption as all results will be
        stored in memory until they are destroyed or garbage collection
        occurs.

        Args:
            params (dict): Payload/request dictionary
            query_id (str): Specifies the ID of the query job
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            list of requests.Response: requests Response() objects

        """
        pages = []
        while True:
            r = self.poll(query_id, params, **kwargs)
            if r.json()['status'] == "FINISHED":
                params['pageNumber'] += 1
                pages.append(r)
            elif r.json()['status'] == "JOB_FINISHED":
                pages.append(r)
                break
            elif r.json()['status'] == "JOB_FAILED":
                pages.append(r)
                break
            else:  # query status ostensibly == 'RUNNING'
                pages.append(r)
                time.sleep(1)  # wait before trying again
        return pages

    def query(self, data=None, **kwargs):
        """Generate a query that retrieves log records.

        Creates a query within the Logging Service that returns 0 or
        more log records. Query results can be returned in pages,
        depending on the size of your result set. You can retrieve pages
        using poll, iter_poll, or poll_all.

        Args:
            data (dict): Payload/request dictionary
            **kwargs: Supported Request() and Session() kwargs

        Returns:
            requests.Response: requests Response() object

        Examples:
            Refer to logging_query.py example.

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

    def xpoll(self, query_id=None, params=None, delete_query=True,
              **kwargs):
        """Retrieve individual logs iteratively in a non-greedy manner.

        Generator function to return individual log entries from poll
        API request.

        Args:
            params (dict): Payload/request dictionary
            query_id (str): Specifies the ID of the query job
            delete_query (bool): True for delete, False otherwise.
            **kwargs: Supported Request() and Session() kwargs

        Yields:
            requests.Response: requests Response() object

        Examples:
            Refer to logging_xpoll.py example.

        """
        def _delete(query_id, **kwargs):
            r = self.delete(query_id, **kwargs)
            try:
                r_json = r.json()
            except ValueError as e:
                raise PanCloudError('Invalid JSON: %s' % e)

            if not (200 <= r.status_code < 300):
                if 'message' in r_json:
                    # XXX delete error response object borked
                    raise PanCloudError(r_json['message'])
                else:
                    raise PanCloudError('%s %s' % (r.status_code,
                                                   r.reason))

            if 'ok' in r_json:
                if r_json['ok'] is True:
                    return
                else:
                    raise PanCloudError('delete: ok: %s' % r_json['ok'])
            else:
                raise PanCloudError('no "ok" in response')

        r = self.poll(query_id, params, **kwargs)
        try:
            r_json = r.json()
        except ValueError as e:
            raise PanCloudError('Invalid JSON: %s' % e)

        if not (200 <= r.status_code < 300):
            if 'message' in r_json:
                raise PanCloudError(r_json['message'])
            else:
                raise PanCloudError('%s %s' % (r.status_code,
                                               r.reason))

        if 'status' not in r_json:
            self._debug(r_json)
            raise PanCloudError('no "status" in response')

        self._debug(r_json['status'])
        if r_json['status'] in ['FINISHED', 'JOB_FINISHED']:
            try:
                hits = r_json['result']['esResult']['hits']['hits']
            except KeyError as e:
                raise PanCloudError('no "hits" in response' % e)

            self._debug('hits: %d', len(hits))
            for x in hits:
                yield x['_source']

            if r_json['status'] == 'JOB_FINISHED':
                if delete_query:
                    _delete(params['queryId'], **kwargs)
                return

            if 'pageNumber' in params:
                params['pageNumber'] += 1
            else:
                params['pageNumber'] = 1

        elif r_json['status'] == 'JOB_FAILED':
            # XXX "message"?
            raise PanCloudError('%s' % r_json['status'])

        elif r_json['status'] == 'RUNNING':
            if 'maxWaitTime' in params:
                pass
            else:
                # XXX
                time.sleep(1)
        else:
            raise PanCloudError('Bad status: %s' % r_json['status'])

        # recursion
        for x in self.xjob(query_id, params, delete_query, **kwargs):
            yield x


