# -*- coding: utf-8 -*-

"""HTTP client wrapper for the **excellent** ``requests`` library."""

from __future__ import absolute_import

import json
import logging

import requests
from requests.adapters import HTTPAdapter

from .exceptions import UnexpectedKwargsError, \
    RequiredKwargsError, HTTPError, PanCloudError


class HTTPClient(object):
    """HTTP client for the Application Framework REST API"""

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
            enforce_json (bool): Require properly-formatted JSON or raise :exc:`~pancloud.exceptions.PanCloudError`. Defaults to ``False``.
            port (int): TCP port to append to URL. Defaults to ``443``.
            raise_for_status (bool): If ``True``, raises :exc:`~pancloud.exceptions.HTTPError` if status_code not in 2XX. Defaults to ``False``.
            url (str): URL to send API requests to - gets combined with ``port`` and :meth:`~request` ``path`` parameter. Defaults to ``None``.

        Args:
            **kwargs: Supported :class:`~requests.Session` and :class:`~requests.adapters.HTTPAdapter` parameters.

        """
        if not logging.getLogger(__name__).isEnabledFor(logging.DEBUG):
            requests.packages.urllib3.disable_warnings()
        self.kwargs = kwargs.copy()  # used for __repr__
        with requests.Session() as self.session:
            self.session.auth = kwargs.pop('auth', self.session.auth)
            self.session.cert = kwargs.pop('cert', self.session.cert)
            self.session.cookies = kwargs.pop(
                'cookies', self.session.cookies
            )
            self.session.headers = kwargs.pop(
                'headers',
                {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )
            self.session.params = kwargs.pop(
                'params', self.session.params
            )
            self.session.proxies = kwargs.pop(
                'proxies', self.session.proxies
            )
            self.session.stream = kwargs.pop(
                'stream', self.session.stream
            )
            self.session.trust_env = kwargs.pop(
                'trust_env', self.session.trust_env
            )
            self.session.verify = kwargs.pop(
                'verify', self.session.verify
            )

            # HTTPAdapter key-word arguments
            _kwargs = {}
            for x in ['pool_connections', 'pool_maxsize', 'pool_block',
                      'max_retries']:
                if x in kwargs:
                    _kwargs[x] = kwargs.pop(x)
            self.adapter = HTTPAdapter(**_kwargs)
            self.session.mount('https://', self.adapter)
            self.session.mount('http://', self.adapter)

            # Non-Requests key-word arguments
            self.auto_refresh = kwargs.pop('auto_refresh', True)
            self.auto_retry = kwargs.pop('auto_retry', True)
            self.credentials = kwargs.pop('credentials', None)
            self.enforce_json = kwargs.pop(
                'enforce_json', False
            )
            self.port = kwargs.pop('port', 443)
            self.raise_for_status = kwargs.pop(
                'raise_for_status', False
            )
            self.url = kwargs.pop('url', None)

            if len(kwargs) > 0:  # Handle invalid kwargs
                raise UnexpectedKwargsError(kwargs)

            if self.credentials:
                self.session.headers = self._apply_credentials(
                    self.session.headers, self.credentials
                )

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

    @staticmethod
    def _apply_credentials(headers, credentials):
        """Update Authorization header.

        Update request headers with latest `access_token`. Perform token
        `refresh` if token is ``None``.

        Args:
            headers (dict): Request headers.
            credentials (class): Read-only credentials.

        Returns:
            dict: Updated request headers.

        """
        token = credentials.get_credentials().access_token
        if token is None:
            token = credentials.refresh(access_token=None, timeout=10)
        headers['Authorization'] = "Bearer {}".format(token)
        return headers

    def _send_request(self, enforce_json, method, raise_for_status,
                      url, **kwargs):
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
            if 'application/json' in self.session.headers.get(
                'Accept', ''
            ):
                try:
                    r.json()
                except ValueError as e:
                    raise PanCloudError(
                        "Invalid JSON: {}".format(e)
                    )
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
        url = kwargs.pop('url', None) or self.url

        # Session() overrides
        auth = kwargs.pop('auth', None)
        cert = kwargs.pop('cert', None)
        cookies = kwargs.pop('cookies', None)
        headers = kwargs.pop('headers', None)
        params = kwargs.pop('params', None)
        proxies = kwargs.pop('proxies', None)
        stream = kwargs.pop('stream', None)
        verify = kwargs.pop('verify', None)

        # Non-Requests key-word arguments
        auto_refresh = kwargs.pop('auto_refresh', None) or self.auto_refresh
        auto_retry = kwargs.pop('auto_retry', None) or self.auto_retry
        credentials = kwargs.pop(
            'credentials', None) or self.credentials
        enforce_json = kwargs.pop('enforce_json', self.enforce_json)
        path = kwargs.pop('path', '')  # default to empty path
        raise_for_status = kwargs.pop(
            'raise_for_status', self.raise_for_status
        )
        url = "{}:{}{}".format(url, self.port, path)

        if credentials and not headers:
            headers = self._apply_credentials(
                self.session.headers, credentials)
        elif credentials and headers:
            headers = self._apply_credentials(headers, credentials)

        k = {  # Re-pack kwargs to dictionary
            'params': params or self.session.params,
            'headers': headers or self.session.headers,
            'cookies': cookies or self.session.cookies,
            'auth': auth or self.session.auth,
            'proxies': proxies or self.session.proxies,
            'verify': verify or self.session.verify,
            'stream': stream or self.session.stream,
            'cert': cert or self.session.cert
        }

        # Request() overrides
        for x in ['allow_redirects', 'data', 'json', 'method',
                  'timeout']:
            if x in kwargs and x == 'data':
                d = kwargs.pop(x)
                if type(d) is dict:
                    k[x] = json.dumps(d)  # convert to str
                else:  # let requests handle the form-encoding
                    k[x] = d
            elif x in kwargs:
                k[x] = kwargs.pop(x)

        # Handle invalid kwargs
        if len(kwargs) > 0:
            raise UnexpectedKwargsError(kwargs)

        try:
            method = k.pop('method')
        except KeyError:
            raise RequiredKwargsError('method')

        # Prepare and send the Request() and return Response()
        try:
            r = self._send_request(
                enforce_json, method, raise_for_status, url, **k
            )
            if r.status_code == 401:
                if credentials and auto_refresh:
                    token = credentials.get_credentials().access_token
                    credentials.refresh(access_token=token, timeout=10)
                    h = self._apply_credentials(
                        k['headers'], credentials)
                    k['headers'] = h
                    if auto_retry:
                        r = self._send_request(
                            enforce_json, method, raise_for_status, url,
                            **k
                        )
            return r
        except requests.RequestException as e:
            raise HTTPError(e)

