"""
This module provides the version of the package.
"""

from pathlib import Path

from inspyre_toolbox.ver_man.classes import PyPiVersionInfo, VersionParser as Version
from inspyre_toolbox.ver_man.helpers import read_version_file

VERSION_FILE_NAME = 'VERSION'


def get_version_file_path(version_file_name: str = VERSION_FILE_NAME) -> Path:
    """
    Gets the version-file path.

    Parameters:
        version_file_name (str, optional):
            The name of the version file. Defaults to :str:'VERSION

    Returns:
        Path:
            The version-file path.

    Since:
        v1.6.0

    Example Usage:
        >>> from inspyre_toolbox.common.about.version import get_version_file_path
        >>> file_path = get_version_file_path()
        >>> print(file_path)
        Path('path/to/version/file')
    """
    return Path(__file__).parent / version_file_name


VERSION_FILE_PATH = get_version_file_path()

VERSION = Version(read_version_file(VERSION_FILE_PATH))

VERSION_NUMBER = VERSION.parse_version()

# Clean up the namespace
del get_version_file_path
del Version
del VERSION_FILE_PATH
del read_version_file


PYPI_VERSION_INFO = PyPiVersionInfo('inspyre-toolbox')


__all__ = [
    'VERSION',
]
