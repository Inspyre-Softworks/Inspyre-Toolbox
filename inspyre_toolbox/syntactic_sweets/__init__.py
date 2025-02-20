#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
"""

A package containing decorators that are a quick help in programming with Python

"""
import os
import sys
from contextlib import contextmanager, redirect_stderr
from os import devnull

SUPPRESSED = False


@contextmanager
def suppress_stderr():
    """
    A context manager that redirects stderr to /dev/null, suppressing error output.
    """
    # Use os.devnull to get the platform-specific null device
    with open(os.devnull, "w") as devnull:
        # Option 1: Use contextlib.redirect_stderr to automatically handle flushing and closing.
        with redirect_stderr(devnull):
            yield


@contextmanager
def suppress_stdout():
    """
    The suppress_stdout function is a context manager that redirects stdout to
    /dev/null.

    This is useful for suppressing output from functions and methods,
    especially when called in loops.  For example:

        with suppress_stdout():
            for i in range(10):
                print(i) # this will not print anything

    Args:
        ``None``
    """
    global SUPPRESSED

    if SUPPRESSED:
        with open(devnull, "w") as dn:
            old_stdout = sys.stdout
            sys.stdout = dn
            try:
                yield
            finally:
                sys.stdout = old_stdout
    else:
        yield
