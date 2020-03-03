# -*- coding: utf-8 -*-

"""Exceptions raised by PAN Cloud library.

This module provides base classes for all errors raised by the PAN Cloud
library. All other exceptions are raised and maintained by Python
standard or nonstandard libraries.

"""


class CortexError(Exception):
    """Base class for all exceptions raised by PAN Cloud library."""

    def __init__(self, message):
        """Override the base class message attribute.

        Args:
            message (str): Exception message.

        """
        super(CortexError, self).__init__(message)
        self.message = message


class HTTPError(CortexError):
    """A pancloud HTTP error occurred."""

    def __init__(self, inst):
        """Convert exception instance to string.

        Args:
            inst (class): Exception instance.

        """
        CortexError.__init__(self, "{}".format(inst))


class PartialCredentialsError(CortexError):
    """The required credentials were not supplied."""

    def __init__(self, inst):
        """Convert exception instance to string.

        Args:
            inst (class): Exception instance.

        """
        CortexError.__init__(self, "{}".format(inst))


class RequiredKwargsError(CortexError):
    """A required keyword argument was not passed."""

    def __init__(self, kwarg):
        """Capture missing key-word argument.

        Args:
            kwarg (str): Key-word argument.

        """
        CortexError.__init__(self, "{}".format(kwarg))


class UnexpectedKwargsError(CortexError):
    """An unexpected keyword argument was passed."""

    def __init__(self, kwargs):
        """Convert kwargs to CSV string.

        Args:
            kwargs (dict): Key-word arguments.

        """
        CortexError.__init__(self, "{}".format(", ".join(kwargs.keys())))
