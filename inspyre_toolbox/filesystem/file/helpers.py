import hashlib
from typing import Union

from inspyre_toolbox.conversions.bytes import ByteConverter


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
