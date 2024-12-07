"""
This module contains functions to check the current operating system.

Functions:
    is_windows:
        Check if the current operating system is Windows.

    is_linux:
        Check if the current operating system is Linux.

Since:
    1.6.0
"""

import os


def is_windows() -> bool:
    """
    Check if the current operating system is Windows.

    Returns:
        bool:
            True if the current operating system is Windows, False otherwise.
    """
    return os.name == 'nt'


def is_linux() -> bool:
    """
    Check if the current operating system is Linux.

    Returns:
        bool:
            True if the current operating system is Linux, False otherwise.
    """
    return os.name == 'posix'


def is_macos() -> bool:
    """
    Check if the current operating system is macOS.

    Returns:
        bool:
            True if the current operating system is macOS, False otherwise.
    """
    return os.name == 'mac'


def is_supported() -> bool:
    """
    Check if the current operating system is supported.

    Returns:
        bool:
            True if the current operating system is supported, False otherwise.
    """
    return is_windows() or is_linux() or is_macos()
