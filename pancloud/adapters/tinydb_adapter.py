# -*- coding: utf-8 -*-

"""TinyDB storage adapter."""
from __future__ import absolute_import

import os
from threading import RLock

from tinydb import TinyDB, Query

from .. import PanCloudError
from . import StorageAdapter


class TinyDBStore(StorageAdapter):

    def __init__(self):
        self.query = Query()
        self.db = self.init_store()
        self.lock = RLock()

    def fetch_credential(self, credential=None, profile=None):
        """Fetch credential from credentials file.

        Args:
            credential (str): Credential to fetch.
            profile (str): Credentials profile. Defaults to ``'default'``.

        Returns:
            str, None: Fetched credential or ``None``.

        """
        q = self.db.search(self.query.profile == profile)
        try:
            return q[0].get(credential, '')
        except (AttributeError, ValueError, IndexError):
            return

    def init_store(self):
        path = os.path.join(
            os.path.expanduser('~'), '.config', 'pancloud',
            'credentials.json'
        )
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path), 0o700)
            except OSError as e:
                raise PanCloudError("{}".format(e))
        return TinyDB(
            path, sort_keys=True, indent=4,
            default_table='profiles'
        )

    def remove_profile(self, profile=None):
        """Remove profile from credentials file.

        Args:
            profile (str): Credentials profile to remove.

        Returns:
            int: Result of operation.

        """
        with self.db:
            return self.db.remove(self.query.profile == profile)

    def write_credentials(self, credentials=None, profile=None,
                          cache_token=None):
        """Write credentials.

        Write credentials to credentials file. Performs ``upsert``.

        Args:
            cache_token (bool): If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
            credentials (class): Read-only credentials.
            profile (str): Credentials profile. Defaults to ``'default'``.

        Returns:
            int: Result of operation.

        """
        d = {
            'profile': profile,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'refresh_token': credentials.refresh_token
        }
        if cache_token:
            d.update({'access_token': credentials.access_token})
        with self.lock:
            return self.db.upsert(
                d, self.query.profile == profile
            )
