import os
from pathlib import Path
from typing import List, Optional, TypeVar, Union
from warnings import warn

from pypattyrn.behavioral.null import Null

from inspyre_toolbox.syntactic_sweets.classes.decorators.freeze import freeze_property
from inspyre_toolbox.syntactic_sweets.classes.decorators import validate_type

PathLike = TypeVar("PathLike", str, bytes, Path, None)


class ISTB_Path:

    def __init__(self, path: Union[str, Path], auto_prepare=False, **kwargs):
        self.__auto_prepare = None
        self.__path = None
        self.__prepared = False

        self.path = path
        self.auto_prepare = auto_prepare

        if self.auto_prepare:
            self.prepare(**kwargs)

    @property
    def auto_prepare(self):
        return self.__auto_prepare

    @auto_prepare.setter
    @freeze_property
    @validate_type(bool)
    def auto_prepare(self, new):
        self.__auto_prepare = new

    @property
    def exists(self):
        return self.path.exists()

    @property
    def parent(self):
        return self.path.parent

    @property
    def path(self):
        return self.__path

    @path.setter
    @freeze_property
    def path(self, new):
        self.__path = new

    @property
    def prepared(self):
        return self.__prepared

    @prepared.setter
    @freeze_property
    @validate_type(bool)
    def prepared(self, new):
        self.__prepared = new

    def prepare(self, **kwargs):
        if not self.prepared:
            self.__path = prepare_path(self.path, **kwargs)
            self.prepared = True

        return self.path

    def __str__(self):
        return str(self.path)


def create_directory(
        directory: Union[str, bytes, os.PathLike],
        do_not_prepare: bool = False,
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False,
        do_not_check_if_exists: bool = False,
        ):
    """
        Create a directory.

        Parameters:
            directory (Union[str, Path]):
                The directory to create.

            do_not_prepare (bool):
                A flag indicating whether to prepare the path.

            do_not_expand (bool):
                A flag indicating whether to expand the path.

            do_not_resolve (bool):
                A flag indicating whether to resolve the path.

            do_not_convert (bool):
                A flag indicating whether to convert the path to a string.

            do_not_provision (bool):
                A flag indicating whether to provision the path.

            do_not_check_if_exists (bool):
                A flag indicating whether to check if the path exists.
        """
    if not do_not_prepare:
        directory = prepare_path(
                directory,
                do_not_convert=do_not_convert,
                do_not_expand=do_not_expand,
                do_not_resolve=do_not_resolve,
                do_not_provision=do_not_provision,
                do_not_check_if_exists=do_not_check_if_exists
                )

    if not isinstance(directory, Path):
        raise ValueError(f"Invalid directory: {directory}!")

    if not do_not_check_if_exists and directory.exists():
        return

    directory.mkdir(parents=True, exist_ok=True)


def check_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False,
        ) -> bool:
    """
    Check if a path is valid.

    This function checks if a path is valid. If the path is a string, it will be converted to a Path object. If the path
    is not expanded, it will be expanded. If the path is not resolved, it will be resolved. If the path is not converted
    to a string, it will be converted to a string. If the path is not provisioned, it will be provisioned.

    Note:
        Provisioning a path involves converting it to a Path object, expanding it, and resolving it.

    Parameters:
        path (Union[str, Path]):
            The path to check.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_provision (bool):
            A flag indicating whether to provision the path.

    Returns:
        bool:
            A flag indicating whether the path is valid.
    """
    if not do_not_provision:
        path = provision_path(
                path,
                do_not_convert=do_not_convert,
                do_not_expand=do_not_expand,
                do_not_resolve=do_not_resolve
                )

    return path.exists() if isinstance(path, Path) else False


def check_directory(
        path: Union[str, Path],
        **kwargs
        ) -> bool:
    """
    Check if a directory is valid.

    This function checks if a directory is valid. If the path is a string, it will be converted to a Path object. If the
    path is not expanded, it will be expanded. If the path is not resolved, it will be resolved. If the path is not
    converted to a string, it will be converted to a string. If the path is not provisioned, it will be provisioned.

    Note:
        Provisioning a path involves converting it to a Path object, expanding it, and resolving it.

    Parameters:
        path (Union[str, Path]):
            The directory to check.

        **kwargs:
            Additional keyword arguments.

    Returns:
        bool:
            A flag indicating whether the directory is valid.
    """
    return path.is_dir() if check_path(path, **kwargs) else False


def check_file(
        path: Union[str, Path],
        **kwargs
        ) -> bool:
    """
    Check if a file is valid.

    Parameters:

        path (Union[str, Path]):
            The file to check.

        **kwargs:
            Additional keyword arguments.

    Returns:
        bool:
            A flag indicating whether the file is valid.
    """
    return path.is_file() if check_path(path, **kwargs) else False


def prepare_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        do_not_provision: bool = False,
        do_not_check_if_exists: bool = False,
        do_not_create: bool = False,
        return_as_string: bool = False
        ):
    """
    Prepare a path.

    Parameters:
        path (Union[str, Path]):
            The path to prepare.

        do_not_create (bool):
            A flag indicating whether to create the path.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_provision (bool):
            A flag indicating whether to provision the path.

        do_not_check_if_exists (bool):
            A flag indicating whether to check if the path exists.

        return_as_string:
            A flag indicating whether to return the path as a string.

    Returns:
        Union[str, Path]:
            The prepared path.

    Raises:
        ValueError: If the path is invalid.

    Example:
        >>> prepare_path('~/path/to/file', return_as_string=True)
        '/home/taylor/path/to/file'

        >>> prepare_path('~/path/to/file', return_as_string=False)
        PosixPath('/home/taylor/path/to/file')

    """
    if not do_not_provision:
        path = provision_path(
                path,
                do_not_convert=do_not_convert,
                do_not_expand=do_not_expand,
                do_not_resolve=do_not_resolve
                )

    if path.suffix:
        do_not_create = True
        warn(f"File path detected: {path}", UserWarning)

    if not do_not_check_if_exists:

        exists = check_path(path)

        if not exists and do_not_create:
            raise ValueError(f"Invalid path: {path}")
        elif not exists:
            create_directory(path, do_not_prepare=True, do_not_provision=True, do_not_check_if_exists=True)

    return str(path) if return_as_string else path


def provision_path(
        path: Union[str, Path],
        do_not_expand: bool = False,
        do_not_resolve: bool = False,
        do_not_convert: bool = False,
        ) -> Path:
    """
    Provision a path.

    Parameters:
        path (str):
            The path to provision.

        do_not_convert (bool):
            A flag indicating whether to convert the path to a string.

        do_not_expand (bool):
            A flag indicating whether to expand the path.

        do_not_resolve (bool):
            A flag indicating whether to resolve the path.

    Returns:
        Path:
            The provisioned path.
    """
    if not isinstance(path, Path):
        if isinstance(path, str) and not do_not_convert:
            path = Path(path)
        else:
            raise ValueError(f"Invalid path: {path}!")

    if not do_not_expand:
        path = path.expanduser()

    if not do_not_resolve:
        path = path.resolve()

    return path


def provision_paths(path_list: list) -> list:
    """
    Provision a list of paths.

    This function takes a list of paths and provisions them.

    Note:
        Provisioning a path involves converting it to a Path object, expanding it, and resolving it.

    Parameters:
        path_list (list):
            The list of paths to provision.

    Returns:
        list:
            The provisioned list of paths.
    """
    return [provision_path(path) for path in path_list]


def gather_files_in_dir(
        directory: Union[str, Path],
        recursive: bool = False,
        file_types: Optional[Union[str, List[str]]] = None,
        ignore_dirs: Optional[List[str]] = None,
        ignore_case: bool = False,
        parent_logger=Null()
        ) -> List[Path]:
    """
    Gather all files in a directory.

    Parameters:
        directory (Union[str, Path]):
            The directory to gather files from.

        recursive (bool):
            Whether to gather files recursively.

        file_types (Optional[Union[str, List[str]]]):
            The file types (extensions, not including the leading '.') to gather. If None, files of all types will be
            gathered.

        ignore_dirs (Optional[List[str]]):
            A list of directory names to ignore. If any directory at any depth matches the given directory names it
            will be ignored. If `ignore_case` is True, the directory names will be converted to lowercase before
            comparison. This argument is ignored if :param:`recursive` is `False`.

        ignore_case (bool):
            Whether to ignore case when matching directory names. If True, the directory names will be converted to
            lowercase before comparison. This parameter is ignored if there are no directory names to ignore.

        parent_logger:
            The parent logger to use for the logger for this function.

    Returns:
        List[Path]:
            A list of file-paths for files in the directory.
    """
    log = parent_logger.get_child('gather_files_in_dir')
    log.debug(f'Gathering files in directory: {directory}')

    directory = prepare_path(directory)

    if not file_types:
        file_types = ['*']
    if isinstance(file_types, str):
        file_types = [file_types]

    if ignore_case and ignore_dirs:
        ignore_dirs = [dir_name.lower() for dir_name in ignore_dirs]

    files = []

    if not isinstance(directory, Path):
        raise ValueError(f"Invalid directory: {directory}!")

    for (dir_path, dir_names, file_names) in os.walk(directory):
        if ignore_case:
            dir_names[:] = [d for d in dir_names if d.lower() not in ignore_dirs]
        else:
            dir_names[:] = [d for d in dir_names if d not in ignore_dirs]

        if not recursive:
            dir_names.clear()

        for file_type in file_types:
            files.extend(
                    Path(dir_path) / file_name
                    for file_name in file_names
                    if file_type == '*' or file_name.endswith(file_type)
                    )

    log.debug(f'Gathered {len(files)} files in directory: {directory} | Recursive: {recursive}')
    return files


def get_storage_unit_abbreviation(unit):
    """
    Get the abbreviation for a storage unit.

    Parameters:
        unit (str):
            The storage unit.

    Returns:
        str:
            The abbreviation for the storage unit.
    """
    return {
            'byte':      'B',
            'kilobyte':  'KB',
            'megabyte':  'MB',
            'gigabyte':  'GB',
            'terabyte':  'TB',
            'petabyte':  'PB',
            'exabyte':   'EB',
            'zetabyte':  'ZB',
            'yottabyte': 'YB'
            }.get(unit, 'B')
