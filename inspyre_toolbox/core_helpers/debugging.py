"""

This module contains different functions that help with debugging.

"""
import inspect

def who_rang():
    return inspect.stack()[2][3]
