# -*- coding: utf-8 -*-

"""Access, store and refresh credentials."""
from __future__ import absolute_import

import os
import sys
import uuid
from collections import namedtuple
from threading import Lock

import requests

from .exceptions import UnexpectedKwargsError, PanCloudError, \
    PartialCredentialsError

# Constants
TOKEN_URL = 'https://api.paloaltonetworks.com/api/oauth2/RequestToken'
REVOKE_URL = 'https://api.paloaltonetworks.com/api/oauth2/RevokeToken'
BASE_URL = 'https://identity.paloaltonetworks.com/as/authorization.oauth2'

ReadOnlyCredentials = namedtuple(
    'ReadOnlyCredentials',
    ['access_token', 'client_id', 'client_secret', 'refresh_token']
)


class Credentials(object):
    """An Application Framework credentials object."""

    def __init__(self, access_token=None, auth_base_url=None, cache_token=True,
                 client_id=None, client_secret=None, instance_id=None,
                 profile=None, redirect_uri=None, region=None,
                 refresh_token=None, scope=None, storage_adapter=None,
                 storage_params=None, token_url=None, token_revoke_url=None,
                 **kwargs):
        """Persist Session() and credentials attributes.

        Built on top of the ``Requests`` library, ``Credentials``
        is an abstraction layer for accessing, storing and refreshing
        credentials needed for interacting with the Application
        Framework.

        ``Credentials`` resolves credentials from the following locations,
        in the following order:

            1) Class instance variables
            2) Environment variables
            3) Credentials store

        Args:
            access_token (str): OAuth2 access token. Defaults to ``None``.
            auth_base_url (str): IdP base authorization URL. Default to ``None``.
            cache_token (bool): If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
            client_id (str): OAuth2 client ID. Defaults to ``None``.
            client_secret (str): OAuth2 client secret. Defaults to ``None``.
            instance_id (str): Instance ID. Defaults to ``None``.
            profile (str): Credentials profile. Defaults to ``'default'``.
            redirect_uri (str): Redirect URI. Defaults to ``None``.
            region (str): Region. Defaults to ``None``.
            refresh_token (str): OAuth2 refresh token. Defaults to ``None``.
            scope (str): OAuth2 scope. Defaults to ``None``.
            storage_params (dict) = Storage adapter parameters. Defaults to ``None``.
            token_url (str): Refresh URL. Defaults to ``None``.
            token_revoke_url (str): Revoke URL. Defaults to ``None``.
            **kwargs: Supported :class:`~requests.Session` parameters.

        """
        self.access_token_ = access_token
        self.auth_base_url = auth_base_url or BASE_URL
        self.cache_token_ = cache_token
        self.client_id_ = client_id
        self.client_secret_ = client_secret
        self.instance_id = instance_id
        self.profile = profile or 'default'
        self.redirect_uri = redirect_uri
        self.region = region
        self.refresh_token_ = refresh_token
        self.scope = scope
        self.state = uuid.uuid4()
        self.adapter = storage_adapter or \
                       'pancloud.adapters.tinydb_adapter.TinyDBStore'
        self.storage = self._init_adapter(storage_params)
        self.token_lock = Lock()
        self.token_url = token_url or TOKEN_URL
        self.token_revoke_url = token_revoke_url or REVOKE_URL
        self._credentials_found_in_instance = any(
            [self.access_token_, self.client_id_,
             self.client_secret_, self.refresh_token_])
        with requests.Session() as self.session:
            self.session.auth = kwargs.pop('auth', self.session.auth)
            self.session.cert = kwargs.pop('cert', self.session.cert)
            self.session.cookies = kwargs.pop('cookies',
                                              self.session.cookies)
            self.session.headers = kwargs.pop('headers',
                                              self.session.headers)
            self.session.params = kwargs.pop('params',
                                             self.session.params)
            self.session.proxies = kwargs.pop('proxies',
                                              self.session.proxies)
            self.session.stream = kwargs.pop('stream',
                                             self.session.stream)
            self.session.trust_env = kwargs.pop('trust_env',
                                                self.session.trust_env)
            self.session.verify = kwargs.pop('verify',
                                             self.session.verify)
            if len(kwargs) > 0:
                raise UnexpectedKwargsError(kwargs)

    @property
    def access_token(self):
        """Get access_token."""
        if self.cache_token:
            return self.access_token_ or \
                   self._resolve_credential('access_token')
        return self.access_token_

    @property
    def cache_token(self):
        """Get cache_token setting."""
        return self.cache_token_

    @property
    def client_id(self):
        """Get client_id."""
        return self.client_id_ or \
               self._resolve_credential('client_id')

    @property
    def client_secret(self):
        """Get client_secret."""
        return self.client_secret_ or \
               self._resolve_credential('client_secret')

    @property
    def refresh_token(self):
        """Get refresh_token."""
        return self.refresh_token_ or \
               self._resolve_credential('refresh_token')

    @staticmethod
    def _credentials_found_in_envars():
        """Check for credentials in envars.

        Returns:
            bool: ``True`` if at least one is found, otherwise ``False``.

        """
        return any([os.getenv('PAN_ACCESS_TOKEN'),
                    os.getenv('PAN_CLIENT_ID'),
                    os.getenv('PAN_CLIENT_SECRET'),
                    os.getenv('PAN_REFRESH_TOKEN')])

    def _init_adapter(self, storage_params=None):
        module_path = self.adapter.rsplit('.', 1)[0]
        adapter = self.adapter.split('.')[-1]
        try:
            __import__(module_path)
        except ImportError as e:
            raise PanCloudError('Module import error: %s: %s' %
                                (module_path, e))

        try:
            class_ = getattr(sys.modules[module_path], adapter)
        except AttributeError:
            raise PanCloudError('Class not found: %s' % adapter)

        return class_(storage_params=storage_params)

    def _resolve_credential(self, credential):
        """Resolve credential from envars or credentials store.

        Args:
            credential (str): Credential to resolve.

        Returns:
            str or None: Resolved credential or ``None``.

        """
        if self._credentials_found_in_instance:
            return
        elif self._credentials_found_in_envars():
            return os.getenv('PAN_' + credential.upper())
        else:
            return self.storage.fetch_credential(
                credential=credential, profile=self.profile)

    def fetch_tokens(self, client_id=None, client_secret=None, code=None,
                     redirect_uri=None):
        """Exchange authorization code for token.

        Args:
            client_id (str): OAuth2 client ID. Defaults to ``None``.
            client_secret (str): OAuth2 client secret. Defaults to ``None``.
            code (str): Authorization code. Defaults to ``None``.
            redirect_uri (str): Redirect URI. Defaults to ``None``.

        Returns:
            dict: Response from token URL.

        """
        client_id = client_id or self.client_id
        client_secret = client_secret or self.client_secret
        redirect_uri = redirect_uri or self.redirect_uri
        r = requests.post(
            self.token_url,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'authorization_code',
                'client_id': client_id,
                'client_secret': client_secret,
                'code': code,
                'redirect_uri': redirect_uri
            },
            auth=False
        )
        if not r.ok:
            raise PanCloudError(
                '%s %s: %s' % (r.status_code, r.reason, r.text)
            )
        try:
            r_json = r.json()
        except ValueError as e:
            raise PanCloudError("Invalid JSON: %s" % e)
        else:
            if r.json().get('error_description') or r.json().get('error'):
                raise PanCloudError(r.text)
            self.access_token_ = r_json.get('access_token')
            self.refresh_token_ = r_json.get('refresh_token')
            self.write_credentials()
            return r_json

    def get_authorization_url(self, client_id=None, instance_id=None,
                              redirect_uri=None, region=None, scope=None,
                              state=None):
        """Generate authorization URL.

        Args:
            client_id (str): OAuth2 client ID. Defaults to ``None``.
            instance_id (str): App Instance ID. Defaults to ``None``.
            redirect_uri (str): Redirect URI. Defaults to ``None``.
            region (str): App Region. Defaults to ``None``.
            scope (str): Permissions. Defaults to ``None``.
            state (str): UUID to detect CSRF. Defaults to ``None``.

        Returns:
            str, str: Auth URL, state

        """
        client_id = client_id or self.client_id
        instance_id = instance_id or self.instance_id
        redirect_uri = redirect_uri or self.redirect_uri
        region = region or self.region
        scope = scope or self.scope
        state = state or self.state
        return requests.Request(
            'GET',
            self.auth_base_url,
            params={
                'client_id': client_id,
                'instance_id': instance_id,
                'redirect_uri': redirect_uri,
                'region': region,
                'response_type': 'code',
                'scope': scope,
                'state': state
            }
        ).prepare().url, state

    def get_credentials(self):
        """Get read-only credentials.

        Returns:
            class: Read-only credentials.

        """
        return ReadOnlyCredentials(
            self.access_token, self.client_id, self.client_secret,
            self.refresh_token
        )

    def remove_profile(self, profile):
        """Remove profile from credentials store.

        Args:
            profile (str): Credentials profile to remove.

        Returns:
            int: Result of operation.

        """
        return self.storage.remove_profile(profile=profile)

    def refresh(self, timeout=None, access_token=None):
        """Refresh access and refresh tokens.

        Args:
            timeout (int): HTTP timeout. Defaults to ``None``.
            access_token (str): Access token to refresh. Defaults to ``None``.

        Returns:
            str: Refreshed access token.

        """
        if not self.token_lock.locked():
            with self.token_lock:
                if access_token == self.access_token or access_token is None:
                    c = self.get_credentials()
                    if c.client_id and c.client_secret and c.refresh_token:
                        r = self.session.post(
                            url=self.token_url,
                            data={
                                'client_id': c.client_id,
                                'client_secret': c.client_secret,
                                'refresh_token': c.refresh_token,
                                'grant_type': 'refresh_token'
                            },
                            timeout=timeout
                        )
                        if not r.ok:
                            raise PanCloudError(
                                '%s %s: %s' % (r.status_code, r.reason, r.text)
                            )
                        try:
                            r_json = r.json()
                        except ValueError as e:
                            raise PanCloudError("Invalid JSON: %s" % e)
                        else:
                            if r.json().get(
                                'error_description'
                            ) or r.json().get(
                                'error'
                            ):
                                raise PanCloudError(r.text)
                            self.access_token_ = r_json.get(
                                'access_token', None
                            )
                            if r_json.get('refresh_token', None):
                                self.refresh_token_ = \
                                    r_json.get('refresh_token')
                            self.write_credentials()
                        return self.access_token_
                    else:
                        raise PartialCredentialsError(
                            "Missing one or more required credentials"
                        )

    def revoke_access_token(self, timeout=None):
        """Revoke access token."""
        c = self.get_credentials()
        r = self.session.post(
            url=self.token_revoke_url,
            data={
                'client_id': c.client_id,
                'client_secret': c.client_secret,
                'token': c.access_token,
                'token_type_hint': 'access_token'
            },
            timeout=timeout
        )
        if not r.ok:
            raise PanCloudError(
                '%s %s: %s' % (r.status_code, r.reason, r.text)
            )

    def revoke_refresh_token(self, timeout=None):
        """Revoke refresh token."""
        c = self.get_credentials()
        r = self.session.post(
            url=self.token_revoke_url,
            data={
                'client_id': c.client_id,
                'client_secret': c.client_secret,
                'token': c.refresh_token,
                'token_type_hint': 'refresh_token'
            },
            timeout=timeout
        )
        if not r.ok:
            raise PanCloudError(
                '%s %s: %s' % (r.status_code, r.reason, r.text)
            )

    def write_credentials(self):
        """Write credentials.

        Write credentials to credentials store.

        Returns:
            int: Result of operation.

        """
        c = self.get_credentials()
        return self.storage.write_credentials(
            credentials=c, profile=self.profile,
            cache_token=self.cache_token_
        )
