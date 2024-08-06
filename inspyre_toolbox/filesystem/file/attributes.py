from pathlib import Path
from typing import Union

from inspyre_toolbox.filesystem.file import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.path_man import provision_path
from inspyre_toolbox.sys_man.operating_system.checks import is_windows

MOD_LOGGER = PARENT_LOGGER.get_child('attributes')

try:
    if not is_windows():
        raise NotImplementedError('The attributes module is only available on Windows.')

    RECALL_ON_DATA_ACCESS_ATTR = 0x00400000

    __all__ = ['file_has_recall_attribute']

except NotImplementedError as e:
    MOD_LOGGER.error(f'Error: {e}')
    raise e


def file_has_recall_attribute(
        file_path: Union[str, Path],
        do_not_provision: bool = False
        ) -> bool:
    """
    Check if a file has the 'recall on data access' attribute set.

    This function checks if a file has the 'recall on data access' attribute set. This attribute is
    used by Windows to mark files that should be recalled from a storage device when they are
    accessed. OneDrive uses this attribute to mark files that are stored in the cloud and not stored
    locally. This function will return True if the file has the attribute set, and False if it does
    not. This can be useful for finding out which files must be downloaded from the cloud before they
    can have operations performed on them.

    Note:
        This function is only available on Windows.

    Parameters:
        file_path (Union[str, Path]):
            The path to the file to check.

        do_not_provision (bool):
            Whether to provision the path before checking it.

    Returns:
        bool:
            True if the file has the 'recall on data access' attribute set, False otherwise.
    """
    _name = 'file_has_recall_attribute'

    def wrapped(file_path, do_not_provision):
        # Set up the logger for this function if it doesn't already exist, otherwise get the existing
        # logger from the parent logger.
        if not MOD_LOGGER.find_child_by_name(_name):
            log = MOD_LOGGER.get_child(_name)
        else:
            log = MOD_LOGGER.find_child_by_name(_name)[0]

        from win32api import GetFileAttributes

        if not do_not_provision:
            log.debug(f'Provisioning path: {file_path}')
            file_path = provision_path(file_path)
        else:
            log.debug(f'Not provisioning path: {file_path}')

        try:
            log.debug(f'Checking file attributes for {file_path}')
            attrs = GetFileAttributes(str(file_path))
            log.debug(f'File attributes for {file_path}: {attrs}')
            return attrs & RECALL_ON_DATA_ACCESS_ATTR
        except Exception as e:
            log.error(f'Error checking file attributes for {file_path}: {e}')
            return False

    return bool(wrapped(file_path, do_not_provision))
