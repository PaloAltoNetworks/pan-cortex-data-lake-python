# -*- coding: utf-8 -*-

"""Exceptions raised by PAN Cloud library.

This module provides base classes for all errors raised by the PAN Cloud
library. All other exceptions are raised and maintained by Python
standard or nonstandard libraries.

"""


class PanCloudError(Exception):
    """Base class for all exceptions raised by PAN Cloud library."""

    def __init__(self, message):
        """Override the base class message attribute.

        Args:
            message (str): Exception message

        """
        super(PanCloudError, self).__init__(message)
        self.message = message


class HTTPError(PanCloudError):
    """A pancloud HTTP error occurred."""

    def __init__(self, inst):
        """Convert exception instance to string.

        Args:
            inst (class): Exception instance

        """
        PanCloudError.__init__(
            self, "{}".format(inst)
        )


class RequiredKwargsError(PanCloudError):
    """A required keyword argument was not passed."""

    def __init__(self, kwarg):
        """Capture missing key-word argument.

        Args:
            kwarg (str): Key-word argument

        """
        PanCloudError.__init__(self, "{}".format(kwarg))


class UnexpectedKwargsError(PanCloudError):
    """An unexpected keyword argument was passed."""

    def __init__(self, kwargs):
        """Convert kwargs to CSV string.

        Args:
            kwargs (dict): Key-word arguments

        """
        PanCloudError.__init__(
            self, "{}".format(", ".join(kwargs.keys()))
        )


