import ctypes
import sys


def run_as_admin():
    """
    Run the current script as an admin.

    Raises:
        PermissionError:
            If the current user is not an admin.

    Since:
        v1.6.0

    Example:
        >>> from inspyre_toolbox.sys_man.operating_system import run_as_admin
        >>> run_as_admin()
    """
    params = ' '.join(f'"{arg}"' for arg in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)


__all__ = ['run_as_admin']
