"""

This module contains different functions that help with debugging.

"""
import inspect


def who_rang() -> str:
    """
    The :func:`who_rang` function returns the name of the function that called the
    function that called it.

    Arguments:
        ``None``

    Returns:
        str: The name of the function that called the function that called it.
    """
    return inspect.stack()[2][3]
