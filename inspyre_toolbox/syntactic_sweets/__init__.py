"""Module for suppressing standard output and error streams.

This module provides two context managers:
  - suppress_stderr:
      Redirects stderr to the system’s null device.

  - suppress_stdout:
      Redirects stdout to the system’s null device.
"""
from inspyre_toolbox.syntactic_sweets.suppressors import suppress_stderr, suppress_stdout

__all__ = [
    "suppress_stderr",
    "suppress_stdout"
]
