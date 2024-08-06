import winreg
from warnings import warn

from inspyre_toolbox.path_man import prepare_path


def notify_environment_of_path_changes():
    """
    Notify the environment of PATH changes.
    """
    import ctypes

    # Notify the environment of changes
    ctypes.windll.user32.SendMessageTimeoutW(
            winreg.HWND_BROADCAST,
            winreg.WM_SETTINGCHANGE,
            0,
            "Environment",
            winreg.SMTO_ABORTIFHUNG,
            5000,
            None
            )


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
    new_path = prepare_path(new_path, do_not_create=True)
    with winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER) as root:  # Get the current user
        with winreg.OpenKey(root, "Environment", 0, winreg.KEY_ALL_ACCESS) as key:  # Go to the environment key
            existing_path_value = winreg.EnumValue(key, 3)[1]  # Grab the current path value

            # Takes the current path value and appends the new program path
            new_path_value = existing_path_value + new_path + ";"

            # Update path variable with the new path value
            winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path_value)
