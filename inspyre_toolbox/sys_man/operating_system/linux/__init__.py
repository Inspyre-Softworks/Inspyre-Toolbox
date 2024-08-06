import os
from warnings import warn

from inspyre_toolbox.path_man import check_file, prepare_path


def is_admin() -> bool:
    """
    Checks if the current user has administrative privileges.

    Returns:
        bool:
            True if the current user has administrative privileges, False otherwise.
    """
    return (os.getuid() == 0)


IS_ADMIN = is_admin()

del is_admin

PROFILE_FILE = os.getenv('HOME') + '/.bashrc'


def add_to_path(new_path: str, do_not_notify=None, profile_file: str = PROFILE_FILE):
    """
    The add_to_path function adds the program path to the system's PATH variable on Unix-like systems.
    This allows for easy access to programs from any terminal window.

    Args:
        new_path (str):
            The full path to the directory you'd like to add to your system's PATH
            environment variable.

        do_not_notify (bool):
            This parameter is not used on Unix-like systems. Ignoring parameter.

        profile_file (str):
            The file to add the path to. Defaults to ~/.bashrc.

    Returns:
        None
    """
    if do_not_notify:
        warn("The do_not_notify parameter is not used on Unix-like systems. Ignoring parameter.")

    new_path = str(prepare_path(new_path))
    profile_file = str(prepare_path(profile_file))

    if not check_file(profile_file):
        raise FileNotFoundError(f"File {profile_file} does not exist")

    with open(profile_file, "a") as bash_file:  # Open bashrc file
        bash_file.write(f'\nexport PATH="{new_path}:$PATH"\n')  # Ad
        # d program path to Path variable
    os.system(f". {os.getenv('HOME')}/.bashrc")  # Update bash source
    print(f"Added {new_path} to path on Unix-like system, please restart shell for changes to take effect")
    print('"exec $SHELL" to restart shell')


__all__ = [
        'IS_ADMIN',
        'add_to_path'
        ]
