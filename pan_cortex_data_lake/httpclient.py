# -*- coding: utf-8 -*-

"""HTTP client wrapper for the **excellent** ``requests`` library."""

from __future__ import absolute_import

import logging

logger = logging.getLogger(__name__)

import requests
from requests.adapters import HTTPAdapter

# support ujson in place of standard json library
try:
    import ujson

    requests.models.complexjson = ujson
    logger.debug("Monkey patched requests with ujson")
except ImportError:
    pass

from .exceptions import (
    UnexpectedKwargsError,
    RequiredKwargsError,
    HTTPError,
    CortexError,
)
from . import __version__
from .utils import ApiStats


class HTTPClient(object):
    """HTTP client for the Cortex™ REST API"""

    def __init__(self, **kwargs):
        """Persist Session() attributes and implement connection-pooling.

        Built on top of the ``Requests`` library, ``HTTPClient`` is an
        abstraction layer for preparing and sending HTTP `requests` to the
        Application Framework REST APIs and handling `responses`. All
        ``Requests`` are prepared as ``Session`` objects, with the option
        to persist certain attributes such as ``cert``, ``headers``,
        ``proxies``, etc. ``HTTPAdapter`` is implemented to enable more
        granular performance and reliability tuning.

        Parameters:
            auto_refresh (bool): Perform token refresh following HTTP 401 response from server. Defaults to ``True``.
            auto_retry (bool): Retry last failed HTTP request following a token refresh. Defaults to ``True``.
            credentials (Credentials): :class:`~pancloud.credentials.Credentials` object. Defaults to ``None``.
            enforce_json (bool): Require properly-formatted JSON or raise :exc:`~pancloud.exceptions.PanCloudError`. Defaults to ``False``.
            force_trace (bool): If ``True``, forces trace and forces ``x-request-id`` to be returned in the response headers. Defaults to ``False``.
            port (int): TCP port to append to URL. Defaults to ``443``.
            raise_for_status (bool): If ``True``, raises :exc:`~pancloud.exceptions.HTTPError` if status_code not in 2XX. Defaults to ``False``.
            url (str): URL to send API requests to - gets combined with ``port`` and :meth:`~request` ``path`` parameter. Defaults to ``None``.

        Args:
            **kwargs: Supported :class:`~requests.Session` and :class:`~requests.adapters.HTTPAdapter` parameters.

        """
        self.kwargs = kwargs.copy()  # used for __repr__
        with requests.Session() as self.session:
            self._default_headers()  # apply default headers
            self.session.auth = kwargs.pop("auth", self.session.auth)
            self.session.cert = kwargs.pop("cert", self.session.cert)
            self.session.cookies = kwargs.pop("cookies", self.session.cookies)
            self.session.headers.update(kwargs.pop("headers", {}))
            self.session.params = kwargs.pop("params", self.session.params)
            self.session.proxies = kwargs.pop("proxies", self.session.proxies)
            self.session.stream = kwargs.pop("stream", self.session.stream)
            self.session.trust_env = kwargs.pop("trust_env", self.session.trust_env)
            self.session.verify = kwargs.pop("verify", self.session.verify)

            # HTTPAdapter key-word arguments
            _kwargs = {}
            for x in ["pool_connections", "pool_maxsize", "pool_block", "max_retries"]:
                if x in kwargs:
                    _kwargs[x] = kwargs.pop(x)
            self.adapter = HTTPAdapter(**_kwargs)
            self.session.mount("https://", self.adapter)
            self.session.mount("http://", self.adapter)

            # Non-Requests key-word arguments
            self.auto_refresh = kwargs.pop("auto_refresh", True)
            self.credentials = kwargs.pop("credentials", None)
            self.enforce_json = kwargs.pop("enforce_json", False)
            self.force_trace = kwargs.pop("force_trace", False)
            if self.force_trace is True:
                self.session.headers.update({"x-envoy-force-trace": ""})
            self.port = kwargs.pop("port", 443)
            self.raise_for_status = kwargs.pop("raise_for_status", False)
            self.url = kwargs.pop("url", "https://api.us.cdl.paloaltonetworks.com")

            if len(kwargs) > 0:  # Handle invalid kwargs
                raise UnexpectedKwargsError(kwargs)

            if self.credentials:
                logger.debug("Applying session-level credentials")
                self._apply_credentials(
                    auto_refresh=self.auto_refresh,
                    credentials=self.credentials,
                    headers=self.session.headers,
                )
            self.stats = ApiStats({"transactions": 0})

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

    @staticmethod
    def _apply_credentials(auto_refresh=True, credentials=None, headers=None):
        """Update Authorization header.

        Update request headers with latest `access_token`. Perform token
        `refresh` if token is ``None``.

        Args:
            auto_refresh (bool): Perform token refresh if access_token is ``None`` or expired. Defaults to ``True``.
            credentials (class): Read-only credentials.
            headers (class): Requests `CaseInsensitiveDict`.

        """
        token = credentials.get_credentials().access_token
        if auto_refresh is True:
            if token is None:
                token = credentials.refresh(access_token=None, timeout=10)
                logger.debug("Token refreshed due to 'None' condition")
            elif credentials.jwt_is_expired():
                token = credentials.refresh(timeout=10)
                logger.debug("Token refreshed due to 'expired' condition")
        headers.update({"Authorization": "Bearer {}".format(token)})
        logger.debug("Credentials applied to authorization header")

    def _default_headers(self):
        """Update default headers.

        The requests library default headers are set in the `utils.py`
        `default_headers()` function.

        """
        self.session.headers.update(
            {
                "Accept": "application/json",
                "User-Agent": "%s/%s" % ("cortex-data-lake-python", __version__),
            }
        )
        logger.debug("Default headers applied: %r" % self.session.headers)

    def _send_request(self, enforce_json, method, raise_for_status, url, **kwargs):
        """Send HTTP request.

        Args:
             enforce_json (bool): Require properly-formatted JSON or raise :exc:`~pancloud.exceptions.PanCloudError`. Defaults to ``False``.
             method (str): HTTP method.
             raise_for_status (bool): If ``True``, raises :exc:`~pancloud.exceptions.HTTPError` if status_code not in 2XX. Defaults to ``False``.
             url (str): Request URL.
             **kwargs (dict): Re-packed key-word arguments.

         Returns:
            requests.Response: Requests Response() object

        """
        r = self.session.request(method, url, **kwargs)
        if raise_for_status:
            r.raise_for_status()
        if enforce_json:
            if "application/json" in self.session.headers.get("Accept", ""):
                try:
                    r.json()
                except ValueError as e:
                    raise CortexError("Invalid JSON: {}".format(e))
        self.stats.transactions += 1
        return r

    def request(self, **kwargs):
        """Generate HTTP request using given parameters.

        The request method prepares HTTP requests using class or
        method-level attributes/variables. Class-level attributes may be
        overridden by method-level variables offering greater
        flexibility and efficiency.

        Parameters:
            enforce_json (bool): Require properly-formatted JSON or raise :exc:`~pancloud.exceptions.HTTPError`. Defaults to ``False``.
            path (str): URI path to append to URL. Defaults to ``empty``.
            raise_for_status (bool): If ``True``, raises :exc:`~pancloud.exceptions.HTTPError` if status_code not in 2XX. Defaults to ``False``.

        Args:
            **kwargs: Supported :class:`~requests.Session` and :class:`~requests.adapters.HTTPAdapter` parameters.

        Returns:
            requests.Response: Requests Response() object

        """
        url = kwargs.pop("url", self.url)

        # Session() overrides
        auth = kwargs.pop("auth", self.session.auth)
        cert = kwargs.pop("cert", self.session.cert)
        cookies = kwargs.pop("cookies", self.session.cookies)
        headers = kwargs.pop("headers", self.session.headers.copy())
        params = kwargs.pop("params", self.session.params)
        proxies = kwargs.pop("proxies", self.session.proxies)
        stream = kwargs.pop("stream", self.session.stream)
        verify = kwargs.pop("verify", self.session.verify)

        # Non-Requests key-word arguments
        auto_refresh = kwargs.pop("auto_refresh", self.auto_refresh)
        credentials = kwargs.pop("credentials", None)
        endpoint = kwargs.pop("endpoint", "")  # default to empty endpoint
        enforce_json = kwargs.pop("enforce_json", self.enforce_json)
        raise_for_status = kwargs.pop("raise_for_status", self.raise_for_status)
        url = "{}:{}{}".format(url, self.port, endpoint)

        if credentials:
            logger.debug("Applying method-level credentials")
            self._apply_credentials(
                auto_refresh=auto_refresh, credentials=credentials, headers=headers
            )

        k = {  # Re-pack kwargs to dictionary
            "params": params,
            "headers": headers,
            "cookies": cookies,
            "auth": auth,
            "proxies": proxies,
            "verify": verify,
            "stream": stream,
            "cert": cert,
        }

        # Request() overrides
        for x in ["allow_redirects", "data", "json", "method", "timeout"]:
            if x in kwargs:
                k[x] = kwargs.pop(x)

        # Handle invalid kwargs
        if len(kwargs) > 0:
            raise UnexpectedKwargsError(kwargs)

        try:
            method = k.pop("method")
        except KeyError:
            raise RequiredKwargsError("method")

        # Prepare and send the Request() and return Response()
        try:
            r = self._send_request(enforce_json, method, raise_for_status, url, **k)
            return r
        except requests.RequestException as e:
            raise HTTPError(e)
