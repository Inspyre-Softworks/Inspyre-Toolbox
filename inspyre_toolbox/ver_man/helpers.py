from pathlib import Path
from typing import Optional
from inspyre_toolbox.path_man import provision_path
from inspyre_toolbox.ver_man.classes import VersionParser as Version


def get_version_from_file(file_path: Path, do_not_raise_errors=False) -> Optional[Version]:
    """
    Gets the version from a file.

    Parameters:
        file_path (Path):
            The file path from which to get the version.

        do_not_raise_errors (bool, optional):
            If True, does not raise an error if the file is not found. Defaults to False.

    Returns:
        Optional[Version]:
            The version.

    Raises:
        FileNotFoundError:
            If the file is not found and :param:`do_not_raise_errors` is :bool:`False`.

        Exception:
            If an error occurs while reading the file and :param:`do_not_raise_errors` is :bool:`False`.

    Since:
        v1.6.0

    Example Usage:
        >>> from inspyre_toolbox.ver_man.helpers import get_version_from_file
        >>> from pathlib import Path
        >>> file_path = Path('path/to/version/file')
        >>> version = get_version_from_file(file_path)
        >>> print(version)
        1.6.0
    """
    if not file_path.exists():
        if do_not_raise_errors:
            return None
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            return Version(f.read().strip())
    except Exception as e:

        # If the error should not be raised, return None
        if do_not_raise_errors:
            return None

        # Otherwise, raise the error with the original traceback.
        raise e from e  # Raise the exception with the original traceback


def get_version_string_from_file(file_path: Path) -> str:
    """
    Gets the version string from a file.

    Parameters:
        file_path (Path):
            The file path from which to get the version string.

    Returns:
    Since:
        v1.6.0
    """

    return str(get_version_from_file(file_path))


def read_version_file(file_path, do_not_provision=False):
    if not do_not_provision:
        file_path = provision_path(file_path)

    with open(file_path, 'r') as f:
        return f.read().strip()
