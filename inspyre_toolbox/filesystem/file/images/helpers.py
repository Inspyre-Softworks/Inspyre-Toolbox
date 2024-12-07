"""
This module provides helper functions for working with images.

Functions:
    get_supported_image_formats:
        Get the supported image formats.
"""

from pathlib import Path
from typing import Union

from platformdirs import user_pictures_path

from inspyre_toolbox.filesystem.file.collection import FileCollection, collect_files
from inspyre_toolbox.filesystem.file.images.constants import VALID_IMAGE_EXTENSIONS
from inspyre_toolbox.path_man import provision_path

DEFAULT_PICTURES_DIR = user_pictures_path()


def collect_image_files(root_dir: Union[str, Path] = DEFAULT_PICTURES_DIR, recursive: bool = True,
                        file_types=VALID_IMAGE_EXTENSIONS, **kwargs) -> FileCollection:
    return collect_files(root_dir, recursive, extensions=file_types, **kwargs)


def is_image_file(path: Union[str, Path], skip_path_provisioning=False) -> bool:
    """
    Check if a file is an image file.

    Parameters:
        path (Union[str, Path]):
            The path to the file. This can be a string or a Path object. If a string is provided, it will be converted
            to a Path object, expanded, resolved, and absolute.

        skip_path_provisioning (bool):
            Skip path provisioning if set to True. Default is False. If set to True, the path will not be
            provisioned. If this is set to True, the path must be a valid path, otherwise an exception will be raised.

    Returns:
        bool:
            True if the file is an image file, False otherwise.
    """
    if not skip_path_provisioning:
        path = provision_path(path)

    try:
        if not isinstance(path, Path):
            raise TypeError('The path must be a string or a Path object.')
    except TypeError as e:
        if skip_path_provisioning:
            print('If you\'re going to skip path provisioning, the path must be a Path object.')
        raise e from e

    return path.suffix[1:] in VALID_IMAGE_EXTENSIONS
