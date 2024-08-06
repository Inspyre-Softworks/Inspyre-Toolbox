"""
The win32 module contains functions that are specific to the Windows operating system.

Functions:
    add_to_path:
        Add a program path to the system PATH environment variable on Windows systems.

    IS_ADMIN:
        A boolean value that indicates whether the current user has administrative privileges.
"""
import ctypes
import os
import winreg
from warnings import warn

from inspyre_toolbox.path_man import prepare_path
from inspyre_toolbox.sys_man.operating_system.common.path import separate_path_str as separate_path
from inspyre_toolbox.sys_man.operating_system.win32.windows_registry import RegistryManager


def is_admin() -> bool:
    """
    Checks if the current user has administrative privileges.

    Returns:
        bool:
            True if the current user has administrative privileges, False otherwise.
    """
    return ctypes.windll.shell32.IsUserAnAdmin() != 0


def update_user_path_variable(new_path: str):
    """
    The update_user_path_variable function updates the user's PATH variable with the new program path.

    Note:
        This function is for Windows systems only. It will not work on *nix systems.

        This function will not notify the environment of changes. *You must call notify_the_environment_of_changes
        after calling this function to notify the environment of changes*.

    Parameters:
        new_path (str):
            The full path to the directory you'd like to add to your PATH environment variable.

    Returns:
        None
    """
    new_path = prepare_path(new_path)
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:  # Get the current user
        with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:  # Go to the environment key
            existing_path_value = winreg.EnumValue(key, 3)[1]  # Grab the current path value

            # Takes the current path value and appends the new program path
            new_path_value = existing_path_value + new_path + ";"

            # Update path variable with the new path value
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)


def notify_the_environment_of_changes():
    """
    The notify_the_environment_of_changes function notifies the environment of changes to the PATH variable.

    Returns:
        None
    """
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_long()
    SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
    SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u"Environment", SMTO_ABORTIFHUNG, 5000,
                        ctypes.byref(result))


def add_to_path(new_path: str, do_not_notify: bool = False, profile_file=None):
    """
    The add_to_path function adds the program path to the system's PATH variable on Windows systems.
    This allows for easy access to programs from any terminal window.

    Args:
        new_path (str):
            The full path to the directory you'd like to add to your system's PATH
            environment variable.

    Returns:
        None
    """
    if profile_file:
        warn("The profile_file parameter is not used on Windows systems. Ignoring parameter.")

    update_user_path_variable(new_path)

    if not do_not_notify:
        notify_the_environment_of_changes()
        return print(f"Added {new_path} to path on Windows, changes have been notified to the environment")

    print(f"Added {new_path} to path on Windows, please restart shell for changes to take effect")


def remove_from_path(directory: str):
    """
    The remove_from_path function removes a directory from the PATH environment variable.

    Args:
        directory (str):
            The directory to remove from the PATH environment variable.

    Returns:
        None
    """
    directory = prepare_path(directory)
    path_directories = list_path_directories()

    if directory in path_directories:
        path_directories.remove(directory)
        new_path = os.pathsep.join(path_directories)

        with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:  # Get the current user PLUGIN_REGISTRY
            with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:  # Go to the environment key
                winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)

        notify_the_environment_of_changes()
        return print(f"Removed {directory} from path on Windows, changes have been notified to the environment")

    return print(f"Directory {directory} not found in PATH variable")


def list_path_directories():
    reg_man = RegistryManager('Environment')
    return separate_path(reg_man.get_value('Path'))


IS_ADMIN = is_admin()

del is_admin

__all__ = [
        'IS_ADMIN',
        'add_to_path'
        ]
