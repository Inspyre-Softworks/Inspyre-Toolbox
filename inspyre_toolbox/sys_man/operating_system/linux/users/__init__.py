"""
This module provides functions for managing users and groups on Linux systems.

Functions:
    - is_admin():
        Checks if the current user has administrative privileges.
"""
import os


def is_admin() -> bool:
    """
    Checks if the current user has administrative privileges.

    Returns:
        bool:
            True if the current user has administrative privileges, False otherwise.
    """
    return os.getuid() == 0
