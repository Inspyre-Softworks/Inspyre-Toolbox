#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
"""

A package containing decorators that are a quick help in programming with Python

"""
from contextlib import contextmanager
from os import devnull
import sys

@contextmanager
def suppress_stdout():
    with open(devnull, "w") as dn:
        old_stdout = sys.stdout
        sys.stdout = dn
        try:
            yield
        finally:
            sys.stdout = old_stdout

