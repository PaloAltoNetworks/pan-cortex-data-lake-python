# -*- coding: utf-8 -*-

"""
:::info
The Query Service is a Palo Alto Networks cloud service which allows
for the storage and retrieval of data stored in the Cortex Data Lake.
Any type of textual data can be stored in the Cortex Data Lake. Palo
Alto Networks firewalls and software can write data to this service, as
can the software and services created by Palo Alto Network's various
partners.
:::

Examples:
    Refer to the [examples provided with this library](https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/tree/master/examples).

"""

from __future__ import absolute_import
import logging
import time

from .exceptions import CortexError, HTTPError
from .httpclient import HTTPClient
from . import __version__


class QueryService(object):
    """A Cortex™ Query Service instance."""

    def __init__(self, **kwargs):
        """

        Parameters:
            session (HTTPClient): [HTTPClient](httpclient.md#httpclient) object. Defaults to `None`.
            url (str): URL to send API requests to. Later combined with `port` and `endpoint` parameter.

        Args:
            **kwargs: Supported [HTTPClient](httpclient.md#httpclient) parameters.

        """
        self.kwargs = kwargs.copy()  # used for __repr__
        self.session = kwargs.pop("session", None)
        self._httpclient = self.session or HTTPClient(**kwargs)
        self._httpclient.stats.update(
            {
                "cancel_job": 0,
                "create_query": 0,
                "get_job": 0,
                "list_jobs": 0,
                "get_job_results": 0,
                "records": 0,
            }
        )
        self.stats = self._httpclient.stats
        self.url = self._httpclient.url
        self._debug = logging.getLogger(__name__).debug

    def __repr__(self):
        for k in self.kwargs.get("headers", {}):
            if k.lower() == "authorization":
                x = dict(self.kwargs["headers"].items())
                x[k] = "*" * 6  # starrify token
                return "{}({}, {})".format(
                    self.__class__.__name__,
                    ", ".join(
                        "%s=%r" % (x, _)
                        for x, _ in self.kwargs.items()
                        if x != "headers"
                    ),
                    "headers=%r" % x,
                )
        return "{}({})".format(
            self.__class__.__name__, ", ".join("%s=%r" % x for x in self.kwargs.items())
        )

    def cancel_job(self, job_id=None, **kwargs):
        """Cancel a query job.

        Args:
            job_id (str): Specifies the ID of the query job.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        Raises:


        """
        endpoint = "/query/v2/jobs/{}".format(job_id)
        r = self._httpclient.request(
            method="DELETE", url=self.url, endpoint=endpoint, **kwargs
        )
        self.stats.cancel_job += 1
        return r

    def create_query(self, job_id=None, query_params=None, **kwargs):
        """Create a search request.

        :::info
        When submission is successful, http status code of `201` (Created)
        is returned with a 'jobId' in response. Specifying a 'jobId' is
        optional.
        :::

        Args:
            job_id (str): Specifies the ID of the query job. (optional)
            query_params (dict): Query parameters.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        """
        json = kwargs.pop("json", {})
        for name, value in [("jobId", job_id), ("params", query_params)]:
            if value is not None:
                json.update({name: value})
        json.update(
            {
                "clientType": "cortex-data-lake-python",
                "clientVersion": "%s" % __version__,
            }
        )
        endpoint = "/query/v2/jobs"
        r = self._httpclient.request(
            method="POST", url=self.url, json=json, endpoint=endpoint, **kwargs
        )
        self.stats.create_query += 1
        return r

    def get_job(self, job_id=None, **kwargs):
        """Get specific job matching criteria.

        Args:
            job_id (str): Specifies the ID of the query job.
            params (dict): Payload/request dictionary.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        """
        endpoint = "/query/v2/jobs/{}".format(job_id)
        r = self._httpclient.request(
            method="GET", url=self.url, endpoint=endpoint, **kwargs
        )
        self.stats.get_job += 1
        return r

    def get_job_results(
        self,
        job_id=None,
        max_wait=None,
        offset=None,
        page_cursor=None,
        page_number=None,
        page_size=None,
        result_format=None,
        **kwargs
    ):
        """Get results for a specific job_id.

        Args:
            job_id (str): Specifies the ID of the query job.
            max_wait (int): How long to wait in ms for a job to complete. Max 2000.
            offset (int): Along with pageSize, offset can be used to page through result set.
            page_cursor (str): Token/handle that can be used to fetch more data.
            page_number (int): Return the nth page from the result set as specified by this parameter.
            page_size (int): If specified, limits the size of a batch of results to the specified value. If un-specified, backend picks a size that may provide best performance.
            result_format (str): valuesArray or valuesDictionary.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        """
        params = kwargs.pop("params", {})
        for name, value in [
            ("maxWait", max_wait),
            ("offset", offset),
            ("pageCursor", page_cursor),
            ("pageNumber", page_number),
            ("pageSize", page_size),
            ("resultFormat", result_format),
        ]:
            if value is not None:
                params.update({name: value})
        endpoint = "/query/v2/jobResults/{}".format(job_id)
        r = self._httpclient.request(
            method="GET", url=self.url, params=params, endpoint=endpoint, **kwargs
        )
        self.stats.get_job_results += 1

        rows = r.json().get("rowsInPage")
        if rows is not None:
            self.stats.records += rows

        return r

    def iter_job_results(
        self,
        job_id=None,
        max_wait=None,
        offset=None,
        page_cursor=None,
        page_number=None,
        page_size=None,
        result_format=None,
        **kwargs
    ):
        """Retrieve results iteratively in a non-greedy manner using scroll token.

        Args:
            job_id (str): Specifies the ID of the query job.
            max_wait (int): How long to wait in ms for a job to complete. Max 2000.
            offset (int): Along with pageSize, offset can be used to page through result set.
            page_cursor (str): Token/handle that can be used to fetch more data.
            page_number (int): Return the nth page from the result set as specified by this parameter.
            page_size (int): If specified, limits the size of a batch of results to the specified value. If un-specified, backend picks a size that may provide best performance.
            result_format (str): valuesArray or valuesJson.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        """
        params = kwargs.pop("params", {})
        enforce_json = kwargs.pop("enforce_json", True)
        for name, value in [
            ("maxWait", max_wait),
            ("offset", offset),
            ("pageCursor", page_cursor),
            ("pageNumber", page_number),
            ("pageSize", page_size),
            ("resultFormat", result_format),
        ]:
            if value is not None:
                params.update({name: value})

        while True:
            r = self.get_job_results(
                job_id=job_id, params=params, enforce_json=enforce_json, **kwargs
            )
            r_json = r.json()
            if r_json["state"] == "DONE":
                page_cursor = r_json["page"].get("pageCursor")
                if page_cursor is not None:
                    params["pageCursor"] = page_cursor
                    yield r
                else:
                    yield r
                    break
            elif r_json["state"] in ("RUNNING", "PENDING"):
                time.sleep(1)
                continue
            elif r_json["state"] == "FAILED":
                yield r
                break
            else:
                raise CortexError("Bad state: %s" % r_json["state"])

    def list_jobs(
        self,
        max_jobs=None,
        created_after=None,
        state=None,
        job_type=None,
        tenant_id=None,
        **kwargs
    ):
        """Get all jobs matching criteria.

        Args:
            limit (int): Max number of jobs.
            created_after (int): List jobs created after this unix epoch UTC datetime.
            state (str): Job state, e.g. 'RUNNING', 'PENDING', 'FAILED', 'DONE'.
            job_type (str): Query type hint.
            tenant_id (str): Tenant ID.
            **kwargs: Supported [HTTPClient.request()](httpclient.md#request) parameters.

        Returns:
            requests.Response: Requests [Response()](https://docs.python-requests.org/en/latest/api/#requests.Response) object.

        """
        params = kwargs.pop("params", {})
        for name, value in [
            ("maxJobs", max_jobs),
            ("createdAfter", created_after),
            ("state", state),
            ("type", job_type),
            ("tenantId", tenant_id),
        ]:
            if value is not None:
                params.update({name: value})
        endpoint = "/query/v2/jobs"
        r = self._httpclient.request(
            method="GET", url=self.url, params=params, endpoint=endpoint, **kwargs
        )
        self.stats.list_jobs += 1
        return r
