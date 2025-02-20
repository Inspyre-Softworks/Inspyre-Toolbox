"""Module for suppressing standard output and error streams.

This module provides two context managers:
  - suppress_stderr: Redirects stderr to the system’s null device.
  - suppress_stdout: Redirects stdout to the system’s null device.
"""

import os
import sys
from contextlib import contextmanager, redirect_stderr, redirect_stdout, suppress


@contextmanager
def _suppress_stream(stream_name, catch_exception=False):
    """Context manager to suppress a given output stream.

    This function handles both stdout and stderr by redirecting them
    to the system's null device.

    Parameters:
        stream_name (str):
            The name of the stream to suppress ("stdout" or "stderr").
        catch_exception (bool, optional):
            If True, suppresses any exceptions that occur within the context block.
            Defaults to False.

    Yields:
        None
    """
    if stream_name not in ("stdout", "stderr"):
        raise ValueError("stream_name must be either 'stdout' or 'stderr'")

    stream = getattr(sys, stream_name)
    redirect_class = redirect_stdout if stream_name == "stdout" else redirect_stderr

    with open(os.devnull, "w") as null_file, redirect_class(null_file):
        if catch_exception:
            with suppress(Exception):
                yield
        else:
            yield


@contextmanager
def suppress_stderr(catch_exception=False):
    """Context manager to suppress standard error output.

    Redirects stderr to the platform-specific null device.
    When `catch_exception` is True, exceptions within the block are suppressed.

    Parameters:
        catch_exception (bool, optional):
            If True, suppresses any exceptions that occur within the context block.
            Defaults to False.

    Yields:
        None

    Example:
        >>> with suppress_stderr():
        ...     print("This error message will not appear.", file=sys.stderr)
        >>> with suppress_stderr(catch_exception=True):
        ...     raise ValueError("This exception will not be raised.")
        >>> with suppress_stderr():
        ...     raise ValueError("This exception will not be suppressed.")
        Traceback (most recent call last):
            ...
        ValueError: This exception will not be suppressed.
    """
    yield from _suppress_stream("stderr", catch_exception)


@contextmanager
def suppress_stdout(catch_exception=False):
    """Context manager to suppress standard output.

    Redirects stdout to the platform-specific null device.
    When `catch_exception` is True, exceptions within the block are suppressed.

    Parameters:
        catch_exception (bool, optional):
            If True, suppresses any exceptions that occur within the context block.
            Defaults to False.

    Yields:
        None

    Example:
        >>> with suppress_stdout():
        ...     print("This will not be printed to stdout.")
    """
    yield from _suppress_stream("stdout", catch_exception)
