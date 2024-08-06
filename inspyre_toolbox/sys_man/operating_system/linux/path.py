from pathlib import Path
from typing import Union

from inspyre_toolbox.path_man import provision_path


def add_to_path(
        path: Union[str, Path],
        persistent: bool = False
        ):
    """
    Add a path to the PATH environment variable.

    Parameters:
        path (Union[str, Path]):
            The path to add to the PATH environment variable.

        persistent (bool):
            Whether to make the change persistent.

        profile_file (Union[str, Path):
            The profile file to add the path to.

        do

    Returns:
        None
    """


def add_to_path_file(
        path: Union[str, Path],
        path_file: Union[str, Path],
        do_not_provision_filepaths: bool = False,
        prepend: bool = False

        ):
    """
    Add a path to a path file.

    Parameters:
        path (Union[str, Path]):
            The path to add to the path file.

        path_file (Union[str, Path]):
            The path file to add the path to.

        do_not_provision_filepaths (bool):
            Whether to provision the file paths.

    Returns:
        None
    """
    if not do_not_provision_filepaths:
        path_file = provision_path(path_file)
        path = provision_path(path)

    if not path_file.exists():
        create_path_file(path_file)

    with open(path_file, 'a') as file:
        if prepend:
            file.write(f'\nexport PATH={path}:$PATH\n')
        else:
            file.write(f'\nexport PATH=$PATH:{path}\n')


def add_path_file_to_profile_file(profile_file: Union[str, Path], path_file: Union[str, Path]):
    """
    Add a path file to a profile file.

    Parameters:
        profile_file (Union[str, Path]):
            The profile file to add the path file to.

        path_file (Union[str, Path]):
            The path file to add to the profile file.

    Returns:
        None
    """
    profile_file = provision_path(profile_file)
    path_file = provision_path(path_file)

    if check_profile_file_for_path_file_load(profile_file, path_file):
        return

    with open(profile_file, 'a') as file:
        file.write('# Adding path file to profile file.\n'
                   f'\nsource {path_file}\n')


def check_profile_file_for_path_file_load(
        profile_file: Union[str, Path],
        path_file: Union[str, Path],
        do_not_provision_filepaths: bool = False
        ):
    """
    Check a profile file for a path file load.

    Parameters:
        profile_file (Union[str, Path]):
            The profile file to check for the path file load.

        path_file (Union[str, Path]):
            The path file to check for in the profile file.

        do_not_provision_filepaths (bool):
            Whether to provision the file paths.

    Returns:
        bool:
            Whether the path file is loaded in the profile file
    """
    if not do_not_provision_filepaths:
        profile_file = provision_path(profile_file)
        path_file = provision_path(path_file)

    with open(profile_file, 'r') as file:
        lines = file.readlines()

    return f'source {path_file}\n' in lines


def create_path_file(path: Union[str, Path]):
    """
    Create a path file.

    Parameters:
        path (Union[str, Path]):
            The path to create the path file at.

    Returns:

    """
    path = provision_path(path)
    if not path.exists():
        path.touch(exist_ok=False)

    with open(path, 'w') as file:
        file.write('# This file is used to store paths for the PATH environment variable.\n')

    check_profile_file_for_path_file_load('~/.bashrc', path)


def remove_from_path(path: Union[str, Path], do_not_notify: bool = False):
    """
    Remove a path from the PATH environment variable.

    Parameters:
        path (Union[str, Path]):
            The path to remove from the PATH environment variable.

        do_not_notify (bool):
            Whether to notify the environment of the changes.

    Returns:
        None
    """
    pass


def remove_from_path_file(
        path: Union[str, Path],
        path_file: Union[str, Path],
        do_not_provision_filepaths: bool = False
        ):
    """
    Remove a path from a path file.

    Parameters:
        path (Union[str, Path]):
            The path to remove from the path file.

        path_file (Union[str, Path]):
            The path file to remove the path from.

        do_not_provision_filepaths (bool):
            Whether to provision the file paths.

    Returns:
        None
    """
    if not do_not_provision_filepaths:
        path_file = provision_path(path_file)
        path = provision_path(path)

    if not path_file.exists():
        raise FileNotFoundError(f"The path file {path_file} does not exist.")

    with open(path_file, 'r') as file:
        lines = file.readlines()

    with open(path_file, 'w') as file:
        for line in lines:
            if path not in line:
                file.write(line)


def list_path_directories():
    """
    List the directories in the PATH environment variable.

    Returns:
        list:
            The directories in the PATH environment variable.
    """
    pass
