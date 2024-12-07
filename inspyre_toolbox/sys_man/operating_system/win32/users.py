import ctypes


def is_admin():
    """
    Check if the current user is an admin.

    Returns:
        bool:
            True if the current user is an admin, False otherwise.

    Since:
        v1.6.0

    Example:
        >>> from inspyre_toolbox.proc_man.windows.users import is_admin
        >>> is_admin()
        True
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
