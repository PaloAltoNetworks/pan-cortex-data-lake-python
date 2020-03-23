# -*- coding: utf-8 -*-

"""Access, store and refresh credentials."""
from __future__ import absolute_import

import os
import sys
import uuid
from collections import namedtuple
from threading import Lock

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from requests import Request
from time import time
from base64 import b64decode
from json import loads

from .httpclient import HTTPClient
from .exceptions import CortexError, PartialCredentialsError

# Constants
API_BASE_URL = "https://api.paloaltonetworks.com"
AUTH_BASE_URL = "https://identity.paloaltonetworks.com/as/authorization.oauth2"
DEVELOPER_TOKEN_PROVIDER = "https://app.apiexplorer.rocks/request_token"

ReadOnlyCredentials = namedtuple(
    "ReadOnlyCredentials",
    ["access_token", "client_id", "client_secret", "refresh_token"],
)


class Credentials(object):
    """An Application Framework credentials object."""

    def __init__(
        self,
        access_token=None,
        auth_base_url=None,
        cache_token=True,
        client_id=None,
        client_secret=None,
        developer_token=None,
        developer_token_provider=None,
        instance_id=None,
        profile=None,
        redirect_uri=None,
        region=None,
        refresh_token=None,
        scope=None,
        storage_adapter=None,
        storage_params=None,
        token_url=None,
        **kwargs
    ):
        """Persist Session() and credentials attributes.

        The ``Credentials`` class is an abstraction layer for accessing,
        storing and refreshing credentials needed for interacting with
        the Application Framework.

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
            developer_token (str): Developer Token. Defaults to ``None``.
            developer_token_provider (str): Developer Token Provider URL. Defaults to ``None``.
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
        self.auth_base_url = auth_base_url or AUTH_BASE_URL
        self.cache_token_ = cache_token
        self.client_id_ = client_id
        self.client_secret_ = client_secret
        self.developer_token_ = developer_token
        self.developer_token_provider_ = developer_token_provider
        self.instance_id = instance_id
        self.jwt_exp_ = None
        self.profile = profile or "default"
        self.redirect_uri = redirect_uri
        self.region = region
        self.refresh_token_ = refresh_token
        self.scope = scope
        self.session = kwargs.pop("session", None)
        self.state = None
        self.adapter = (
            storage_adapter
            or "pan_cortex_data_lake.adapters.tinydb_adapter.TinyDBStore"
        )
        self.storage = self._init_adapter(storage_params)
        self.token_lock = Lock()
        self.token_url = token_url or API_BASE_URL
        self._credentials_found_in_instance = any(
            [
                self.access_token_,
                self.client_id_,
                self.client_secret_,
                self.refresh_token_,
            ]
        )
        self._httpclient = self.session or HTTPClient(**kwargs)

    def __repr__(self):
        args = self.__dict__.copy()
        for k in [
            "access_token_",
            "refresh_token_",
            "client_secret_",
            "developer_token_",
        ]:
            if args[k] is not None:
                args[k] = "*" * 6
        return "{}({})".format(
            self.__class__.__name__, ", ".join("%s=%r" % x for x in args.items()),
        )

    @property
    def access_token(self):
        """Get access_token."""
        if self.cache_token:
            return self.access_token_ or self._resolve_credential("access_token")
        return self.access_token_

    @access_token.setter
    def access_token(self, access_token):
        """Set access_token."""
        self.access_token_ = access_token

    @property
    def cache_token(self):
        """Get cache_token setting."""
        return self.cache_token_

    @property
    def client_id(self):
        """Get client_id."""
        return self.client_id_ or self._resolve_credential("client_id")

    @client_id.setter
    def client_id(self, client_id):
        """Set client_id."""
        self.client_id_ = client_id

    @property
    def client_secret(self):
        """Get client_secret."""
        return self.client_secret_ or self._resolve_credential("client_secret")

    @client_secret.setter
    def client_secret(self, client_secret):
        """Set client_secret."""
        self.client_secret_ = client_secret

    @property
    def developer_token(self):
        """Get developer token."""
        return self.developer_token_ or os.getenv("PAN_DEVELOPER_TOKEN")

    @developer_token.setter
    def developer_token(self, developer_token):
        """Set developer token."""
        self.developer_token_ = developer_token

    @property
    def developer_token_provider(self):
        """Get developer token provider."""
        return (
            self.developer_token_provider_
            or os.getenv("PAN_DEVELOPER_TOKEN_PROVIDER")
            or DEVELOPER_TOKEN_PROVIDER
        )

    @developer_token_provider.setter
    def developer_token_provider(self, developer_token_provider):
        """Set developer token provider."""
        self.developer_token_provider_ = developer_token_provider

    @property
    def jwt_exp(self):
        """Get JWT exp."""
        return self.jwt_exp_ or self._decode_exp()

    @jwt_exp.setter
    def jwt_exp(self, jwt_exp):
        """Set jwt_exp."""
        self.jwt_exp_ = jwt_exp

    @property
    def refresh_token(self):
        """Get refresh_token."""
        return self.refresh_token_ or self._resolve_credential("refresh_token")

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        """Set refresh_token."""
        self.refresh_token_ = refresh_token

    @staticmethod
    def _credentials_found_in_envars():
        """Check for credentials in envars.

        Returns:
            bool: ``True`` if at least one is found, otherwise ``False``.

        """
        return any(
            [
                os.getenv("PAN_ACCESS_TOKEN"),
                os.getenv("PAN_CLIENT_ID"),
                os.getenv("PAN_CLIENT_SECRET"),
                os.getenv("PAN_REFRESH_TOKEN"),
            ]
        )

    def _init_adapter(self, storage_params=None):
        module_path = self.adapter.rsplit(".", 1)[0]
        adapter = self.adapter.split(".")[-1]
        try:
            __import__(module_path)
        except ImportError as e:
            raise CortexError("Module import error: %s: %s" % (module_path, e))

        try:
            class_ = getattr(sys.modules[module_path], adapter)
        except AttributeError:
            raise CortexError("Class not found: %s" % adapter)

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
            return os.getenv("PAN_" + credential.upper())
        else:
            return self.storage.fetch_credential(
                credential=credential, profile=self.profile
            )

    def decode_jwt_payload(self, access_token=None):
        """Extract payload field from JWT.

        Args:
            access_token (str): Access token to decode. Defaults to ``None``.

        Returns:
            dict: JSON object that contains the claims conveyed by the JWT.

        """
        c = self.get_credentials()
        jwt = access_token or c.access_token
        try:
            _, payload, _ = jwt.split(".")  # header, payload, sig
            rem = len(payload) % 4
            if rem > 0:  # add padding
                payload += "=" * (4 - rem)
            try:
                decoded_jwt = b64decode(payload).decode("utf-8")
            except TypeError as e:
                raise CortexError("Failed to base64 decode JWT: %s" % e)
            else:
                try:
                    x = loads(decoded_jwt)
                except ValueError as e:
                    raise CortexError("Invalid JSON: %s" % e)
        except (AttributeError, ValueError) as e:
            raise CortexError("Invalid JWT: %s" % e)

        return x

    def _decode_exp(self, access_token=None):
        """Extract exp field from access token.

        Args:
            access_token (str): Access token to decode. Defaults to ``None``.

        Returns:
            int: JWT expiration in epoch seconds.

        """
        c = self.get_credentials()
        jwt = access_token or c.access_token
        x = self.decode_jwt_payload(jwt)

        if "exp" in x:
            try:
                exp = int(x["exp"])
            except ValueError:
                raise CortexError("Expiration time (exp) must be an integer")
            else:
                self.jwt_exp = exp
                return exp
        else:
            raise CortexError("No exp field found in payload")

    def fetch_tokens(
        self, client_id=None, client_secret=None, code=None, redirect_uri=None, **kwargs
    ):
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
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        }
        r = self._httpclient.request(
            method="POST",
            url=self.token_url,
            json=data,
            endpoint="/api/oauth2/RequestToken",
            auth=None,
            **kwargs
        )
        if not r.ok:
            raise CortexError("%s %s: %s" % (r.status_code, r.reason, r.text))
        try:
            r_json = r.json()
        except ValueError as e:
            raise CortexError("Invalid JSON: %s" % e)
        else:
            if r.json().get("error_description") or r.json().get("error"):
                raise CortexError(r.text)
            self.access_token = r_json.get("access_token")
            self.jwt_exp = self._decode_exp(self.access_token_)
            self.refresh_token = r_json.get("refresh_token")
            self.write_credentials()
            return r_json

    def get_authorization_url(
        self,
        client_id=None,
        instance_id=None,
        redirect_uri=None,
        region=None,
        scope=None,
        state=None,
    ):
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
        state = state or str(uuid.uuid4())
        self.state = state
        return (
            Request(
                "GET",
                self.auth_base_url,
                params={
                    "client_id": client_id,
                    "instance_id": instance_id,
                    "redirect_uri": redirect_uri,
                    "region": region,
                    "response_type": "code",
                    "scope": scope,
                    "state": state,
                },
            )
            .prepare()
            .url,
            state,
        )

    def get_credentials(self):
        """Get read-only credentials.

        Returns:
            class: Read-only credentials.

        """
        return ReadOnlyCredentials(
            self.access_token, self.client_id, self.client_secret, self.refresh_token
        )

    def jwt_is_expired(self, access_token=None, leeway=0):
        """Validate JWT access token expiration.

        Args:
            access_token (str): Access token to validate. Defaults to ``None``.
            leeway (float): Time in seconds to adjust for local clock skew. Defaults to 0.

        Returns:
            bool: ``True`` if expired, otherwise ``False``.

        """
        if access_token is not None:
            exp = self._decode_exp(access_token)
        else:
            exp = self.jwt_exp
        now = time()
        if exp < (now - leeway):
            return True
        return False

    def remove_profile(self, profile):
        """Remove profile from credentials store.

        Args:
            profile (str): Credentials profile to remove.

        Returns:
            Return value of self.storage.remove_profile()

        """
        return self.storage.remove_profile(profile=profile)

    def refresh(self, access_token=None, **kwargs):
        """Refresh access and refresh tokens.

        Args:
            access_token (str): Access token to refresh. Defaults to ``None``.

        Returns:
            str: Refreshed access token.

        """
        if not self.token_lock.locked():
            with self.token_lock:
                if access_token == self.access_token or access_token is None:
                    if self.developer_token is not None:
                        parsed_provider = urlparse(self.developer_token_provider)
                        url = "{}://{}".format(
                            parsed_provider.scheme, parsed_provider.netloc
                        )
                        endpoint = parsed_provider.path
                        r = self._httpclient.request(
                            method="POST",
                            url=url,
                            endpoint=endpoint,
                            headers={
                                "Authorization": "Bearer {}".format(
                                    self.developer_token
                                )
                            },
                            timeout=30,
                            raise_for_status=True,
                        )

                    elif all([self.client_id, self.client_secret, self.refresh_token]):
                        data = {
                            "client_id": self.client_id,
                            "client_secret": self.client_secret,
                            "refresh_token": self.refresh_token,
                            "grant_type": "refresh_token",
                        }
                        r = self._httpclient.request(
                            method="POST",
                            url=self.token_url,
                            json=data,
                            endpoint="/api/oauth2/RequestToken",
                            **kwargs
                        )
                    else:
                        raise PartialCredentialsError(
                            "Missing one or more required credentials"
                        )

                    if r:
                        if not r.ok:
                            raise CortexError(
                                "%s %s: %s" % (r.status_code, r.reason, r.text)
                            )
                        try:
                            r_json = r.json()
                        except ValueError as e:
                            raise CortexError("Invalid JSON: %s" % e)
                        else:
                            if r.json().get("error_description") or r.json().get(
                                "error"
                            ):
                                raise CortexError(r.text)
                            self.access_token = r_json.get("access_token", None)
                            self.jwt_exp = self._decode_exp(self.access_token_)
                            if r_json.get("refresh_token", None):
                                self.refresh_token = r_json.get("refresh_token")
                            self.write_credentials()
                        return self.access_token_

    def revoke_access_token(self, **kwargs):
        """Revoke access token."""
        c = self.get_credentials()
        data = {
            "client_id": c.client_id,
            "client_secret": c.client_secret,
            "token": c.access_token,
            "token_type_hint": "access_token",
        }
        r = self._httpclient.request(
            method="POST",
            url=self.token_url,
            json=data,
            endpoint="/api/oauth2/RevokeToken",
            **kwargs
        )
        if not r.ok:
            raise CortexError("%s %s: %s" % (r.status_code, r.reason, r.text))
        try:
            r_json = r.json()
        except ValueError as e:
            raise CortexError("Invalid JSON: %s" % e)
        else:
            if r.json().get("error_description") or r.json().get("error"):
                raise CortexError(r.text)
            return r_json

    def revoke_refresh_token(self, **kwargs):
        """Revoke refresh token."""
        c = self.get_credentials()
        data = {
            "client_id": c.client_id,
            "client_secret": c.client_secret,
            "token": c.refresh_token,
            "token_type_hint": "refresh_token",
        }
        r = self._httpclient.request(
            method="POST",
            url=self.token_url,
            json=data,
            endpoint="/api/oauth2/RevokeToken",
            **kwargs
        )
        if not r.ok:
            raise CortexError("%s %s: %s" % (r.status_code, r.reason, r.text))
        try:
            r_json = r.json()
        except ValueError as e:
            raise CortexError("Invalid JSON: %s" % e)
        else:
            if r.json().get("error_description") or r.json().get("error"):
                raise CortexError(r.text)
            return r_json

    def write_credentials(self):
        """Write credentials.

        Write credentials to credentials store.

        Returns:
            Return value of self.storage.write_credentials()

        """
        c = self.get_credentials()
        return self.storage.write_credentials(
            credentials=c, profile=self.profile, cache_token=self.cache_token
        )
