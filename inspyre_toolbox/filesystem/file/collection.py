"""
Since:
    1.6.0
"""
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Union

from box import Box

from inspyre_toolbox.conversions.bytes import get_lowest_unit_size
from inspyre_toolbox.filesystem.errors import NeedsProcessingError
from inspyre_toolbox.filesystem.file import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.humanize import Numerical
from inspyre_toolbox.log_engine import Loggable
from inspyre_toolbox.path_man import gather_files_in_dir, prepare_path, provision_path, provision_paths
from inspyre_toolbox.syntactic_sweets.locks import flag_lock
from . import File

MOD_LOGGER = PARENT_LOGGER.get_child('collection')


class NeedsReprocessingTag:

    def __init__(self, value: bool = False):
        self.__value = value if isinstance(value, bool) else None
        if self.__value is None:
            raise ValueError("Value must be a boolean.")

    def __get__(self, instance, owner):
        return self.__value

    def __set__(self, instance, value):
        if not isinstance(value, bool):
            raise ValueError("Value must be a boolean.")
        self.__value = value


@dataclass
class FileCollection(Loggable):
    """
    A class for managing a collection of files.

    Properties:
        paths (list):
            A list of file paths.

        total_size (int):
            The total size of the collection, in bytes.

        total_files (int):
            The total number of files in the collection.

        extensions (dict):
            A dictionary of extensions with classes for total size and number of files.

        needs_reprocessing (bool):
            A flag indicating whether the collection needs reprocessing.

    Methods:
        get_total_size_in_lowest_unit:
            Get the total size of the collection in the lowest unit.

        get_total_extension_size_in_lowest_unit:
            Get the total size of a specific extension in the lowest unit.

        remove_file:
            Remove a file from the collection.

        reprocess_files:
            Reprocess the files in the collection.

    Examples:
        >>> collection = FileCollection(paths=['/path/to/file1', '/path/to/file2'])
        >>> collection.total_size
        123456  # Total size of the collection, in bytes.
    """
    paths: list
    total_size: int = field(init=False, default=0)
    total_files: int = field(init=False, default=0)
    extensions: dict = field(init=False, default_factory=dict)

    def __init__(self, paths: List[Union[str, Path]] = None, auto_process: bool = False):
        """
        Initialize the FileCollection with a list of file paths.

        `FileCollection` is a class for managing a collection of files. It takes a list of file paths and creates a class
        representing a collection of files with classes for total size and number of files and a dictionary of extensions
        with classes for total size and number of files.

        Parameters:
            paths (list):
                A list of file paths.

        Returns:
            None
        """
        super().__init__(MOD_LOGGER)
        self._files = {
                'local':  {
                        'files':      [],
                        'total_size': 0,
                        },
                'remote': {
                        'files':      [],
                        'total_size': 0,
                        }
                }

        self._files = Box(self._files)
        self._needs_processing = False
        self._files_gathered = False
        self._processing = False
        self.paths = paths

        if self.paths:
            self._files_gathered = True
            self._needs_processing = True

        self.total_size = 0
        self.total_files = 0
        self.extensions = {}
        self.__needs_reprocessing = NeedsReprocessingTag()

        if auto_process:
            self.process_files()

    @property
    def files(self):
        if self.needs_processing and not self._processing:
            raise NeedsProcessingError("Files need to be processed before they can be accessed.")

        return self._files

    @property
    def files_gathered(self) -> bool:
        """
        Returns whether the files have been gathered.

        This property returns a boolean value indicating whether the files have been gathered. If the files have been
        gathered, this property will return `True`. If the files have not been gathered, it will return `False`. The
        property is read-only.

        Returns:
            bool:
                True if the files have been gathered, False otherwise.
        """
        return self._files_gathered

    @property
    def needs_processing(self):
        return self._needs_processing

    @property
    def needs_reprocessing(self) -> bool:
        """
        Returns whether the collection needs reprocessing.

        This property returns a boolean value indicating whether the collection needs reprocessing. If the collection has
        been modified since the last processing, this property will return `True`. If the collection has not been modified,
        it will return `False`. The property is read-only.

        Returns:
            bool:
                True if the collection needs reprocessing, False otherwise.
        """
        return self.__needs_reprocessing

    @needs_reprocessing.setter
    def needs_reprocessing(self, value: bool):
        """
        Sets whether the collection needs reprocessing.

        This method sets the `needs_reprocessing` attribute of the collection. If the value is `True`, the collection will
        be reprocessed the next time it is accessed. If the value is `False`, the collection will not be reprocessed. The
        method is used to indicate that the collection has been modified and needs to be reprocessed.

        Parameters:
            value (bool):
                The value to set the `needs_reprocessing` attribute to. True if the collection needs reprocessing, False
                otherwise.

        Returns:
            None
        """
        self.__needs_reprocessing = value

    @property
    def total_local_size(self):
        return self.files['local']['total_size']

    @property
    def total_remote_size(self):
        return self.files['remote']['total_size']

    def process_files(self):
        """
        Process the files in the collection.

        This method processes the files in the collection. It calculates the total size of the collection, the total number
        of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`, and
        `extensions` attributes of the class.

        Returns:
            None
        """
        self.paths = provision_paths(self.paths)

        with flag_lock(self, 'processing'):

            for path_str in self.paths:
                file = File(path_str)
                if file.has_recall_attribute:
                    bucket = self.files['remote']
                else:
                    bucket = self.files['local']

                bucket['files'].append(file)
                bucket['total_size'] += file.size_in_bytes

                if file.extension not in self.extensions:
                    self.extensions[file.extension] = {
                            'total_size':  0,
                            'total_files': 0,
                            }

                self.total_size += file.size_in_bytes
                self.total_files += 1

                self.extensions[file.extension]['total_size'] += file.size_in_bytes
                self.extensions[file.extension]['total_files'] += 1

        self._needs_processing = False

    def reprocess_files(self):
        """
        Reprocess the files in the collection.

        This method reprocesses the files in the collection. It recalculates the total size of the collection, the total
        number of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`,
        and `extensions` attributes of the class. This method is used to update the collection after files have been added
        or removed.

        Note:
            This method should be called after files have been added or removed from the collection. It will only reprocess
            the files if the `needs_reprocessing` attribute is set to `True`. After reprocessing, the `needs_reprocessing`
            attribute will be set to `False`.

        Returns:
            None

        """
        if self.needs_reprocessing:
            self.total_size = 0
            self.total_files = 0
            self.extensions = {}
            self.process_files()

    def find_file(self, path: Union[str, Path], include_remote: bool = False) -> Union[File, None]:
        """
        Find a file in the collection.

        This method finds a file in the collection by its path. It takes a file path as an argument and returns the file
        object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            path (Union[str, Path]):
                The file path to find.

            include_remote (bool):
                A flag indicating whether to include remote files in the search. If True, the method will search both
                local and remote files. If False, the method will only search local files.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.
        """
        log = self.create_logger()

        log.debug(f"Finding file: {path}")
        path = provision_path(path)

        log.debug(f'Searching {len(self.files["local"]["files"])} local files....')

        local_acc = None

        for local_acc, file in enumerate(self.files['local']['files']):
            if file.path == path:
                log.debug(f"Found file: {file.path} after {local_acc} iterations.")
                return file

        log.debug(f'File not found after searching {local_acc} files.')

        if include_remote:
            log.debug(f'Searching {len(self.files["remote"]["files"])} remote files....')
            for remote_acc, file in enumerate(self.files['remote']['files']):
                if file.path == path:
                    log.debug(f"Found file: {file.path} after {local_acc + remote_acc} iterations.")
                    return file

        return None

    def get_total_size_in_lowest_unit(self) -> tuple[Union[int, float], str]:
        """
        Get the total size of the collection in the lowest unit with a size greater than or equal to 1.

        This method calculates the total size of the collection in the lowest unit with a size greater than or equal
        to 1. It returns the size and the unit as a tuple. The unit is a string representing the unit of the size.

        Returns:
            tuple[Union[int, float], str]:
                The total size of the collection and the unit.

        """
        return get_lowest_unit_size(self.total_size)

    def get_total_extension_size_in_lowest_unit(
            self,
            extension: str,
            return_as_string: bool = False
            ) -> tuple[Union[int, float], str]:
        """
        Get the total size of a specific extension in the lowest unit with a size greater than or equal to 1.

        Parameters:
            extension (str):
                The extension to get the size of.

            return_as_string (bool):
                A flag indicating whether to return the size as a string. If True, the size will be returned as a string
                with the unit. If False, the size will be returned as a tuple with the size and the unit.

        Returns:
            tuple[Union[int, float], str]:
                The total size of the extension and the unit.

        Raises:
            ValueError:
                If the extension is not found in the collection.
        """

        if not extension.startswith('.'):
            extension = f".{extension}"

        extension = extension.lower()

        if extension not in self.extensions:
            raise ValueError(f"Invalid extension: {extension}!")

        lowest_unit_size = get_lowest_unit_size(self.extensions[extension]['total_size'])

        if return_as_string:
            return Numerical(lowest_unit_size[0], noun=lowest_unit_size[1]).count_noun()
        return lowest_unit_size

    def remove_file(self, path: Union[Path, str], **kwargs):
        """
        Remove a file from the collection.

        This method removes a file from the collection. It takes a file path as an argument and removes the file from
        the collection. It then reprocesses the files in the collection to update the total size, total number of files,
        and total size of each extension.

        Note: This method does not delete the file from the file system. It only removes the file from the
        collection, and only if the file is in the collection. If the file is not in the collection, this method will
        raise a `KeyError`. After removing the file, the collection will be reprocessed to update the total size,
        total number of files, and total size of each extension.

        Parameters:
            path (Union[Path, str]):
                The file path to remove.

            **kwargs:
                Additional keyword arguments.

        Raises:
            KeyError:
                If the file is not in the collection.

        Returns:
            None
        """
        path = provision_path(path, **kwargs)
        if path in self.paths:
            self.paths.remove(path)
            self.needs_reprocessing = True
            self.reprocess_files()
            self.needs_reprocessing = False

    def __getitem__(self, key: Union[int, str]) -> Union[str, Dict[str, int]]:
        if isinstance(key, int):
            return str(self.paths[key])
        elif isinstance(key, str):
            if not key.startswith('.'):
                key = f".{key}"
            key = key.lower()
            if key not in self.extensions:
                raise KeyError(f"Extension {key} not found in file collection.")
            return self.extensions[key]
        else:
            raise TypeError("Key must be an integer (for path index) or a string (for extension).")

    def __str__(self):
        size, unit = self.get_total_size_in_lowest_unit()
        size_str = Numerical(size, noun=unit).count_noun()
        return f"Total size: {size_str}, Total files: {self.total_files}"


def create_file_collection(paths: list[Path]) -> FileCollection:
    """
    Create a file collection.

    This function creates a file collection from a list of file paths. It takes a list of file paths as an argument and
    returns a :class:`FileCollection` object representing the collection of files.

    Parameters:
        paths (list[Path]):
            A list of file paths.

    Returns:
        FileCollection:
            A `FileCollection` object representing the collection of files.

    Since:
        v1.0.0
    """
    fc = FileCollection(paths)
    fc.process_files()
    return fc


def collect_files(root_dir: Union[str, Path], recursive=True, **kwargs):
    """
    Collect files in a directory into a :class:`FileCollection`.

    Parameters:
        root_dir (Union[str, Path]):
            The root directory from which to collect files.

        recursive (bool):
            A flag indicating whether to collect files recursively.

        **kwargs:
            Additional keyword arguments.

    Returns:
        FileCollection:
            A `FileCollection` object representing the collection of files.

    """
    root_dir = prepare_path(root_dir, do_not_create=True)
    files = gather_files_in_dir(root_dir, recursive=recursive, **kwargs)
    return create_file_collection(files)
