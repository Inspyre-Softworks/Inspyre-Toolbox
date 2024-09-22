"""
This module contains functions that help determine the environment the program is running in.

Functions:
    has_gui_access -> bool:
        Check if the current user has access to the GUI.

Constants:
    GUI_ACCESS -> bool:
        True if the user has access to the GUI, False otherwise.

Exports:
    GUI_ACCESS -> bool:
        True if the user has access to the GUI, False otherwise.
"""
import ctypes
from ctypes import wintypes

from inspyre_toolbox.sys_man.operating_system.win32 import MOD_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('environment')


def has_gui_access():
    """
    Check if the current user has access to the GUI. This is so you can see if a GUI prompt can be displayed.

    Returns:
        bool:
            True if the user has access to the GUI, False otherwise.

    """
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    # Try to open the input desktop
    h_desktop = user32.OpenInputDesktop(0, False, wintypes.DWORD(0x0100))  # 0x0100 is GENERIC_READ
    if h_desktop:
        user32.CloseDesktop(h_desktop)
        return True
    else:
        return False


GUI_ACCESS = has_gui_access()

__all__ = [
        'GUI_ACCESS'
        ]
