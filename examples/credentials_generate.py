#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate credentials file."""

import getpass
import os
import sys

from builtins import input

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pancloud import Credentials


def main():
    try:
        print("\nCollecting info needed to generate credentials file...\n")
        client_id = input("CLIENT_ID: ")
        client_secret = getpass.getpass(prompt="CLIENT_SECRET: ")
        refresh_token = getpass.getpass(prompt="REFRESH_TOKEN: ")
        profile = input("PROFILE [default]: ") or None
        c = Credentials(client_id=client_id,
                        client_secret=client_secret,
                        refresh_token=refresh_token,
                        profile=profile)
        print("Writing credentials file...")
        c.write_credentials()
        print("Done!\n")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
