"""
This module is a collection of tools for managing the system. It is designed to be cross-platform, but is currently only
implemented for Windows and Linux. The tools in this module are designed to help manage the system, such as checking if
the current user has admin privileges, or checking if the current user has access to the GUI.

Subpackages:
    operating_system:
        This subpackage contains functions for managing the operating system. It is designed to be cross-platform, but is
        currently only implemented for Windows and Linux.
"""
#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
from inspyre_toolbox.log_engine import ROOT_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('sys-man')

from .operating_system.checks import is_windows

if is_windows():
    from .operating_system.win32 import *
else:
    from .operating_system.linux import *

__all__ = [
        'IS_ADMIN',
        ]
