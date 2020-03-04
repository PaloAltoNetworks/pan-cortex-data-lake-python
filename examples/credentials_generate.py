#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate credentials file."""

import getpass
import os
import sys

from builtins import input

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pan_cortex_data_lake import Credentials


def confirm_write(profile):
    """Prompt user to enter Y or N (case-insensitive) to continue."""
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("\nWrite credentials to PROFILE '%s' [Y/N]? " % profile).lower()
    return answer == "y"


def main():
    try:
        print("\nCollecting info needed to generate credentials file...\n")
        client_id = input("CLIENT_ID: ")
        client_secret = getpass.getpass(prompt="CLIENT_SECRET: ")
        refresh_token = getpass.getpass(prompt="REFRESH_TOKEN: ")
        profile = input("PROFILE [default]: ") or None
        c = Credentials(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            profile=profile,
        )
        if confirm_write(profile):
            print("Writing credentials file...")
            c.write_credentials()
            print("Done!\n")
        else:
            print("\nWrite credentials operation aborted.\n")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
