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

from inspyre_toolbox.ver_man.classes import PyPiVersionInfo, RELEASE_MAP, VersionParser


__all__ = [
        'RELEASE_MAP',
    'VersionParser',
    'PyPiVersionInfo',
]
