import os

from inspyre_toolbox.sys_man.operating_system.linux import MOD_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('environment')

DISPLAY = 'DISPLAY' in os.environ


def has_gui_access():
    """
    Check if the current user has access to the GUI. This is so you can see if a GUI prompt can be displayed.

    Returns:
        bool:
            True if the user has access to the GUI, False otherwise.

    """
    # Check if the $DISPLAY environment variable is set
    if not DISPLAY:
        return False

    # Try to connect to the X server
    try:
        from Xlib import display as x_display

        display = x_display.Display()
        display.close()
        return True
    except Exception:
        return False


GUI_ACCESS = has_gui_access()

__all__ = [
        'GUI_ACCESS'
        ]
