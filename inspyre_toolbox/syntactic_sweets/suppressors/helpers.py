"""
Author:
  Taylor

Project:
  Inspyre-Toolbox

Since:
  1.6.0

File:
  helpers.py

----

Description:
    This module provides utility functions for suppressing standard output (stdout) and standard error (stderr)
    streams in a controlled manner using context managers. It includes a function to suppress a specified stream
    and another that suppresses a stream while handling exceptions gracefully.

----

Functions:
    _suppress_stream(stream_name: str) -> Generator[None, None, None]:
        Context manager that suppresses the specified output stream ('stdout' or 'stderr').

    _suppress_stream_with_exceptions(stream_name: str) -> Generator[None, None, None]:
        Context manager that suppresses the specified output stream and safely ignores any exceptions raised.

----

Dependencies:
    - os
    - contextlib:
        * contextmanager,
        * redirect_stdout,
        * redirect_stderr,
        * suppress

----

Example Usage:
    >>> with _suppress_stream("stdout"):
    ...    print("This will not be printed")

    >>> with _suppress_stream_with_exceptions("stderr"):
    ...    raise RuntimeError("This error will be suppressed")
"""
import os
from contextlib import contextmanager, redirect_stderr, redirect_stdout, suppress
from typing import Generator


@contextmanager
def _suppress_stream(stream_name: str) -> Generator[None, None, None]:
    """
    Context manager that suppresses the specified output stream ('stdout' or 'stderr').

    Parameters:
        stream_name (str):
            The name of the stream to suppress ('stdout' or 'stderr').

    Returns:
        Generator[None, None, None]:
            A generator that suppresses the specified stream.

    Raises:
        ValueError:
            If the stream name is not 'stdout' or 'stderr'.

    Example Usage:
        >>> with _suppress_stream("stdout"):
        ...     print("This will not be printed")
    """
    if stream_name not in ("stdout", "stderr"):
        raise ValueError("stream_name must be either 'stdout' or 'stderr'")

    redirect_cls = redirect_stdout if stream_name == "stdout" else redirect_stderr
    with open(os.devnull, "w") as null_file, redirect_cls(null_file):
        yield


@contextmanager
def _suppress_stream_with_exceptions(stream_name: str) -> Generator[None, None, None]:
    """
    Context manager that suppresses the specified output stream and safely ignores any exceptions raised.

    Parameters:
        stream_name (str):
            The name of the stream to suppress ('stdout' or 'stderr').

    Returns:
        Generator[None, None, None]:
            A generator that suppresses the specified stream and safely ignores any exceptions.

    Example Usage:
        >>> with _suppress_stream_with_exceptions("stderr"):
        ...    raise RuntimeError("This error will be suppressed")
    """
    with suppress(Exception):
        yield from _suppress_stream(stream_name)
