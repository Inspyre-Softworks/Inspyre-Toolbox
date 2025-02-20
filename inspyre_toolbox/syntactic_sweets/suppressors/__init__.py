"""
Author:
  Taylor

Project:
  Inspyre-Toolbox

File:
    suppressors/__init__.py

Since:
    1.6.0

----

Description:
    This module provides context managers for suppressing standard output (stdout) and standard error (stderr),
    with an option to catch exceptions during suppression.

----

Functions:
    suppress_stdout(catch_exception: bool = False) -> Generator[None, None, None]:
        Context manager that suppresses stdout. Optionally catches exceptions.

    suppress_stderr(catch_exception: bool = False) -> Generator[None, None, None]:
        Context manager that suppresses stderr. Optionally catches exceptions.

----

Dependencies:
    - inspyre_toolbox.syntactic_sweets.suppressors.helpers (_suppress_stream_with_exceptions, _suppress_stream, contextmanager)

----

Example Usage:
    ```python
    with suppress_stdout():
        print("This will not be printed")

    with suppress_stderr(catch_exception=True):
        raise RuntimeError("This error will be suppressed")
    ```
"""

from typing import Generator

from inspyre_toolbox.syntactic_sweets.suppressors.helpers import _suppress_stream_with_exceptions, _suppress_stream, \
    contextmanager


@contextmanager
def suppress_stdout(catch_exception: bool = False) -> Generator[None, None, None]:
    """
    Context manager that suppresses stdout. Optionally catches exceptions.

    Parameters:
        catch_exception (bool, optional):
            Whether to catch and suppress exceptions. Defaults to False.

    Example Usage:
        >>> with suppress_stdout():
        ...    print("This will not be printed")
    """
    if catch_exception:
        yield from _suppress_stream_with_exceptions("stdout")
    else:
        yield from _suppress_stream("stdout")


@contextmanager
def suppress_stderr(catch_exception: bool = False) -> Generator[None, None, None]:
    """
    Context manager that suppresses stderr. Optionally catches exceptions.

    Parameters:
        catch_exception (bool, optional):
            Whether to catch and suppress exceptions. Defaults to False.

    Example Usage:
        >>> with suppress_stderr(catch_exception=True):
        ...     raise RuntimeError("This error will be suppressed")
    """
    if catch_exception:
        yield from _suppress_stream_with_exceptions("stderr")
    else:
        yield from _suppress_stream("stderr")


__all__ = [
    "suppress_stdout",
    "suppress_stderr"
]
