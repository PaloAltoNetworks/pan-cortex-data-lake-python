# -*- coding: utf-8 -*-

"""Application Framework authentication/authorization."""

from contextlib import contextmanager

from requests_oauthlib import OAuth2Session

from .exceptions import UnexpectedKwargsError

try:
    from openssl import crypto
except ImportError:
    from OpenSSL import crypto
import tempfile

import os


class CredentialResolver(object):

    def __init__(self, **kwargs):
        pass


class Crypto(object):
    """An object for interacting with certificates."""

    def __init__(self):
        pass

    def __repr__(self):
        return '{}()'.format(self.__class__.__name__)

    @contextmanager
    def decrypt_p12(self, **kwargs):
        """Decrypt p12 certificate to temporary file in PEM format.

        The default behavior is to decrypt and extract the certificate,
        private key and CA certificates to a temporary PEM file which is
        immediately deleted after use. The temporary file is guaranteed
        across most Linux, Windows, and Mac operating systems/distros
        and will be written in the most secure manner possible for each
        OS. The location of the temp file will vary by OS beginning with
        the most obvious (i.e. "/var", "/tmp", etc.) before finally
        trying to write the file to the current working directory.
        Developers may optionally choose to persist the PEM certificate
        to the default or custom location using the "delete" and "dir"
        keywords, which default to 'True' and 'None' respectively.

        Yields:
            str: Path to temporary PEM certificate file

        """
        delete = kwargs.pop('delete', True)
        directory = kwargs.pop('dir', None)
        path = kwargs.pop('path', None)
        passphrase = kwargs.pop('passphrase', None)
        if len(kwargs) > 0:
            raise UnexpectedKwargsError(kwargs)

        with tempfile.NamedTemporaryFile(
            suffix='.pem', delete=delete, dir=directory
        ) as temp_pem_file:
            with open(temp_pem_file.name, 'wb') as pem_file:
                encrypted_p12 = open(path, 'rb').read()
                decrypted_p12 = crypto.load_pkcs12(
                    encrypted_p12, passphrase
                )
                pem_file.write(  # write private key
                    crypto.dump_privatekey(
                        crypto.FILETYPE_PEM,
                        decrypted_p12.get_privatekey()
                    )
                )
                pem_file.write(  # write certificate
                    crypto.dump_certificate(
                        crypto.FILETYPE_PEM,
                        decrypted_p12.get_certificate()
                    )
                )
                cacerts = decrypted_p12.get_ca_certificates()
                if cacerts is not None:
                    for cacert in cacerts:
                        pem_file.write(  # write CA certificate
                            crypto.dump_certificate(
                                crypto.FILETYPE_PEM,
                                cacert
                            )
                        )
                yield temp_pem_file.name


class OAuth2(OAuth2Session):
    """An Application Framework Oauth2 Instance."""

    def __init__(self, **kwargs):
        super(OAuth2, self).__init__(**kwargs)
        self.kwargs = kwargs.copy()  # used for __repr__

        # OAuth2Session key-word arguments
        self.client_id = kwargs.pop('client_id', self.client_id)
        self.client = kwargs.pop('client', None)
        self.auto_refresh_kwargs = kwargs.pop(
            'auto_refresh_kwargs', self.auto_refresh_kwargs
        )
        self.scope = kwargs.pop('scope', self.scope)
        self.redirect_uri = kwargs.pop(
            'redirect_uri', self.redirect_uri
        )
        self.token = kwargs.pop('token', self.token)
        self.state = kwargs.pop('state', self.state)
        self.token_updater = kwargs.pop(
            'token_updater', self.token_updater
        )

        # PingID key-word arguments
        _url = 'https://identitytest.paloaltonetworks.com'
        self.client_secret = kwargs.pop('client_secret', None)
        self.cert = kwargs.pop('cert', None)
        self.auth_base_url = kwargs.pop(
            'auth_base_url', '{}/as/authorization.oauth2'.format(_url)
        )
        self.token_url = kwargs.pop(
            'token_url', '{}/as/token.oauth2'.format(_url)
        )
        self.revoke_token_url = kwargs.pop(
            'revoke_token_url', '{}/as/revoke_token.oauth2'.format(_url)
        )

        # Palo Alto Networks key-word arguments
        self.instance_id = kwargs.pop('instance_id', None)

        # OAuth2 variables
        self.credentials = {}
        self.code = None

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            ', '.join('%s=%r' % x for x in self.kwargs.items())
        )

    def get_authorization_url(self):
        url, state = self.authorization_url(
            self.auth_base_url,
            state=self.state  # used to detect CSRF
        )
        return url, state

    def delete_credentials(self):
        self.credentials = None

    def fetch_credentials(self):
        credentials = self.fetch_token(
            self.token_url,
            client_id=self.client_id,
            code=self.code,
            auth=self.auth,
            verify=self.verify,
            cert=self.cert
        )
        self.credentials = credentials
        return credentials

    def refresh_credentials(self):
        credentials = self.refresh_token(
            self.token_url,
            refresh_token=self.credentials.get('refresh_token', None),
            auth=self.auth,
            verify=self.verify,
        )
        self.credentials.update(credentials)
        return credentials


