# -*- coding: utf-8 -*-

"""TinyDB storage adapter."""
from __future__ import absolute_import

import os
from threading import RLock

from tinydb import TinyDB, Query

from .. import CortexError
from . import StorageAdapter


class TinyDBStore(StorageAdapter):
    def __init__(self, **kwargs):
        self._storage_params = kwargs.get("storage_params") or {}
        self.dbfile = self._storage_params.get("dbfile")
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
        q = self.db.get(self.query.profile == profile)
        if q is not None:
            return q.get(credential)

    def init_store(self):
        if self.dbfile:
            dbfile = self.dbfile
        elif os.getenv("PAN_CREDENTIALS_DBFILE"):
            dbfile = os.getenv("PAN_CREDENTIALS_DBFILE")
        else:
            dbfile = os.path.join(
                os.path.expanduser("~"),
                ".config",
                "pan_cortex_data_lake",
                "credentials.json",
            )
        if not os.path.exists(os.path.dirname(dbfile)):
            try:
                os.makedirs(os.path.dirname(dbfile), 0o700)
            except OSError as e:
                raise CortexError("{}".format(e))
        return TinyDB(dbfile, sort_keys=True, indent=4, default_table="profiles")

    def remove_profile(self, profile=None):
        """Remove profile from credentials file.

        Args:
            profile (str): Credentials profile to remove.

        Returns:
            list: List of affected document IDs.

        """
        with self.db:
            return self.db.remove(self.query.profile == profile)

    def write_credentials(self, credentials=None, profile=None, cache_token=None):
        """Write credentials.

        Write credentials to credentials file. Performs ``upsert``.

        Args:
            cache_token (bool): If ``True``, stores ``access_token`` in token store. Defaults to ``True``.
            credentials (class): Read-only credentials.
            profile (str): Credentials profile. Defaults to ``'default'``.

        Returns:
            int: Affected document ID.

        """
        d = {
            "profile": profile,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "refresh_token": credentials.refresh_token,
        }
        if cache_token:
            d.update({"access_token": credentials.access_token})
        with self.lock:
            return self.db.upsert(d, self.query.profile == profile)
