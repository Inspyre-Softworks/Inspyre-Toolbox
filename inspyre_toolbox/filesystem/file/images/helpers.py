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
from . import VALID_IMAGE_EXTENSIONS

DEFAULT_PICTURES_DIR = user_pictures_path()


def collect_image_files(root_dir: Union[str, Path] = DEFAULT_PICTURES_DIR, recursive: bool = True,
                        file_types=VALID_IMAGE_EXTENSIONS, **kwargs) -> FileCollection:
    return collect_files(root_dir, recursive, file_types=file_types, **kwargs)
