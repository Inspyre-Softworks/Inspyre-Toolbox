import hashlib
from pathlib import Path
from typing import List, Optional, Union

from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.path_man import provision_path


def __normalize_file_types(file_types: Optional[Union[str, List[str]]]) -> List[str]:
    """Normalize file types to a list of strings."""
    if file_types is None:
        return ['*']

    return [file_types] if isinstance(file_types, str) else file_types


def __normalize_ignore_dirs(ignore_dirs: Optional[List[str]], ignore_case: bool) -> set:
    """Normalize and prepare directory names to ignore."""
    if ignore_case and ignore_dirs:
        return {dir_name.lower() for dir_name in ignore_dirs}
    return set(ignore_dirs or [])


def __filter_dirs(dir_names: List[str], ignore_dirs: set, ignore_case: bool) -> List[str]:
    """Filter out directories that should be ignored."""
    if ignore_case:
        return [d for d in dir_names if d.lower() not in ignore_dirs]
    return [d for d in dir_names if d not in ignore_dirs]


def __filter_files(dir_path: Path, file_names: List[str], file_types: List[str], get_file_object) -> List[Path]:
    """Filter and gather files based on file types."""
    return [
            get_file_object(dir_path / file_name)
            for file_name in file_names
            if any(file_name.endswith(f".{ftype}") for ftype in file_types) or '*' in file_types
            ]



def get_file_checksum(file_path, algorithm='sha256'):
    """
    Calculate the checksum of a file using the specified hashing algorithm.

    Parameters:
    file_path (str): Path to the file.
    algorithm (str): Hashing algorithm to use ('md5', 'sha1', 'sha256', etc.). Default is 'sha256'.

    Returns:
    str: The calculated checksum.

    Raises:
    ValueError: If the specified algorithm is not supported.
    FileNotFoundError: If the specified file does not exist.
    """
    # Validate the algorithm
    if algorithm not in hashlib.algorithms_available:
        raise ValueError(f"Unsupported algorithm '{algorithm}'. Available algorithms: {hashlib.algorithms_available}")

    # Initialize the hash object
    hash_func = hashlib.new(algorithm)

    # Read the file in chunks and update the hash object
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Return the hex digest of the hash
    return hash_func.hexdigest()


def get_lowest_unit_size(size: int) -> tuple[Union[int, float], str]:
    """
    Get the lowest unit size for a given size.

    Parameters:
        size (int):
            The size to convert.

    Returns:
        tuple[Union[int, float], str]:
            The converted size and the unit.

    Examples:
        >>> get_lowest_unit_size(1024)
        (1.0, 'KB')
        >>> get_lowest_unit_size(1024 * 1024)
        (1.0, 'MB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024)
        (1.0, 'GB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024)
        (1.0, 'TB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'PB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'EB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'ZB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'YB')
    """
    units = ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte', 'exabyte', 'zetabyte', 'yottabyte']
    units.reverse()
    converter = ByteConverter(size, 'byte')

    for unit in units:
        converted = converter.convert(unit.lower())

        if converted >= 1:
            return converted, unit.upper(),


def get_file_object(file_path, skip_path_provision=False):
    """
    Get a file object for the specified file path.

    Parameters:
        file_path (Union[str, Path]):
            The path to the file.

        skip_path_provision (bool):
            Skip path provisioning if set to True. Default is False.

    Returns:
        Optional[File, ImageFile]:
            A file object for the specified file path.

    Raises:
        ValueError:
            If the specified file path is not a valid file.
    """
    from inspyre_toolbox.filesystem.file import File
    from inspyre_toolbox.filesystem.file.images import ImageFile
    from inspyre_toolbox.filesystem.file.images.helpers import is_image_file

    if isinstance(file_path, Path):
        file_path = str(file_path)

    file_path = file_path if skip_path_provision else provision_path(file_path)

    return ImageFile(file_path) if is_image_file(file_path) else File(file_path)


def get_path_list_from_list_of_file_objects(file_objects):
    """
    Get a list of file paths from a list of file objects.

    Parameters:
        file_objects (List[File, ImageFile]):
            A list of file objects.

    Returns:
        List[str]:
            A list of file paths.
    """
    return [file_object.path for file_object in file_objects]
