import os
import sys

from inspyre_toolbox.sys_man.operating_system.linux.users import is_admin


def run_as_admin():
    """
    Run the current script as an admin.

    Raises:
        PermissionError:
            If the current user is not an admin.

    Since:
        v1.6.0

    Example:
        >>> from inspyre_toolbox.sys_man.operating_system.linux.system import run_as_admin
        >>> run_as_admin()
    """
    if is_admin():
        raise PermissionError('The current user is already an admin.')

    cmd = ['sudo', sys.executable] + sys.argv
    os.execvp('sudo', ['sudo'] + cmd)


__all__ = [
    'run_as_admin'
]
