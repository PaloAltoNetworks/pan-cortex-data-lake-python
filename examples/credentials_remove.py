#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Remove credentials profile."""

import os
import sys

from builtins import input

curpath = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.path.join(curpath, os.pardir)]

from pan_cortex_data_lake import Credentials


def confirm_delete(profile):
    """Prompt user to enter Y or N (case-insensitive) to continue."""
    answer = ""
    while answer not in ["y", "n"]:
        answer = input("Delete PROFILE '%s' [Y/N]? " % profile).lower()
    return answer == "y"


def main():
    try:
        profile = input("PROFILE to remove: ") or None
        if profile is not None:
            c = Credentials(profile=profile)
            if confirm_delete(profile):
                print("Removing PROFILE '%s'..." % profile)
                op = c.remove_profile(profile)
                if len(op) > 0:
                    print("\nPROFILE '%s' successfully removed.\n" % profile)
                else:
                    print("\nPROFILE '%s' not found.\n" % profile)
            else:
                print("\nRemove PROFILE operation aborted.\n")
        else:
            print("\nMust specify a PROFILE to remove.\n")
    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
