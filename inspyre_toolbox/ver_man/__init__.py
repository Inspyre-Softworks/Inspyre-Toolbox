"""
This module contains classes and functions to instantiate and provide detailed package version information.

Classes:
    VersionParser:
        A class to parse and provide detailed version information.

    PyPiVersionInfo:
        A class to provide version information from PyPi.

Functions:
    None

Since:
    v1.6.0
"""

from inspyre_toolbox.log_engine import ROOT_LOGGER as PARENT_LOGGER
from inspyre_toolbox.ver_man.classes import VersionParser, PyPiVersionInfo, RELEASE_MAP


MOD_LOGGER = PARENT_LOGGER.get_child('ver_man')


__all__ = [
    'RELEASE_MAP'
    'VersionParser',
    'PyPiVersionInfo',
]
