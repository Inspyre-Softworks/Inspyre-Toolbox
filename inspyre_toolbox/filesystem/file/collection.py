"""
Since:
    1.6.0
"""
import hashlib
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Union

from box import Box
from tqdm import tqdm

from inspyre_toolbox.common.errors import InvalidParameterCombinationError, MissingRequiredParameterError
from inspyre_toolbox.common.types import File as FileType
from inspyre_toolbox.conversions.bytes import get_lowest_unit_size
from inspyre_toolbox.filesystem.errors import NeedsProcessingError
from inspyre_toolbox.filesystem.file import File
from inspyre_toolbox.filesystem.file import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.filesystem.file.helpers import get_path_list_from_list_of_file_objects
from inspyre_toolbox.humanize import Numerical
from inspyre_toolbox.log_engine import Loggable
from inspyre_toolbox.path_man import gather_files_in_dir, prepare_path, provision_path, provision_paths
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from inspyre_toolbox.syntactic_sweets.locks import flag_lock

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

    def __init__(self, paths: List[Union[str, Path]] = None, auto_process: bool = False, do_not_use_progress_bar:
    bool = False):
        """
        Initialize the FileCollection with a list of file paths.

        `FileCollection` is a class for managing a collection of files. It takes a list of file paths and creates a class
        representing a collection of files with classes for total size and number of files and a dictionary of extensions
        with classes for total size and number of files.

        Parameters:
            paths (list):
                A list of file paths.
                
            auto_process (bool):
                A flag indicating whether to automatically process the files when the collection is created. If True, the
                files will be processed automatically. If False, the files will not be processed automatically. Default is
                False.
                
            do_not_use_progress_bar (bool):
                A flag indicating whether to disable the progress bar when processing the files. If True, the progress bar
                will be disabled. If False, the progress bar will be enabled. Default is False.

        Returns:
            None
        """
        super().__init__(MOD_LOGGER)
        self.__initialized = False
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
        self.__checksums = None
        self.__use_progress_bar = True
        self._files = Box(self._files)
        self._checksums_gathered = False
        self._getting_checksums = False
        self._needs_processing = False
        self._files_gathered = False
        self._processing = False
        self.__file_objects = {}
        self.__paths = paths
        self.__file_object_hash = None

        if self.paths:
            self._files_gathered = True
            self._needs_processing = True

        self.total_size = 0
        self.total_files = 0
        self.extensions = {}
        self.__needs_reprocessing = False

        if auto_process:
            self.process_files()

        self.__initialized = True

    @property
    def checksums(self):
        if self.__checksums is None:
            self.get_all_checksums()
        return self.__checksums

    @property
    def files(self):
        if self.needs_processing and not self._processing:
            raise NeedsProcessingError("Files need to be processed before they can be accessed.")

        return self._files

    @files.setter
    @validate_type(dict)
    def files(self, value: dict):
        if not self._processing:
            raise ValueError("Files cannot be set directly. Use the process_files method to set the files.")
        self._files = value

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
    def file_names(self):
        return list(self.file_objects.keys())

    @property
    def file_objects(self):
        return self.__file_objects

    @property
    def file_objects_hash(self):
        if not self.__file_object_hash:
            self.__file_object_hash = self.get_file_object_hash()

        return self.__file_object_hash

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
    def paths(self):
        if not self.__paths and self.file_objects:
            self.__paths = get_path_list_from_list_of_file_objects(self.file_objects)

        return self.__paths

    @paths.setter
    def paths(self, new: List[Union[str, Path]]):
        self.__paths = new

    @property
    def path_strings(self):
        return [str(path) for path in self.paths]

    @property
    def total_local_size(self):
        return self.files['local']['total_size']

    @property
    def total_remote_size(self):
        return self.files['remote']['total_size']

    @property
    def use_progress_bar(self):
        return self.__use_progress_bar

    def backup_all_files(
            self,
            backup_dir: Optional[Union[str, Path]],
            archive: bool = False,
            delete_backups_on_archive: bool = False,
            delete_originals: bool = False,
            skip_archive_confirmation: bool = False,
            skip_backup_delete_confirmation: bool = False,
            skip_delete_originals_confirmation: bool = False,
            skip_all_confirmations: bool = False,
            **kwargs):
        """
        Backup all files in the collection.

        This method backs up all files in the collection to a backup directory. It includes the option to archive
        the backed-up files, delete the backups after archiving, and delete the original files after backing them up.
        Confirmation prompts are enabled by default for archiving, deletion of backups, and deletion of originals,
        but can be skipped individually or altogether.

        Parameters:
            backup_dir (Union[str, Path]):
                The backup directory. This can be a string or a Path object. If a string is provided, it will be converted
                to a Path object, expanded, resolved, and absolute.

            archive (bool):
                Whether the backup should be archived after the files are copied. Default is False.

            delete_backups_on_archive (bool):
                A flag indicating whether to delete the backup directory after archiving. Default is False.

            delete_originals (bool):
                Whether to delete the original files after backing them up. Default is False.

            skip_archive_confirmation (bool):
                Whether to skip the confirmation prompt before archiving. Default is False.

            skip_backup_delete_confirmation (bool):
                Whether to skip the confirmation prompt before deleting the backups. Default is False.

            skip_delete_originals_confirmation (bool):
                Whether to skip the confirmation prompt before deleting the original files. Default is False.

            skip_all_confirmations (bool):
                If True, all confirmation prompts will be skipped, overriding the other skip confirmation parameters.
                Default is False.

            **kwargs:
                Additional keyword arguments.

        Returns:
            Path: The path to the backup directory or archive.

        Raises:
            ValueError:
                If the backup directory cannot be created.

            FileNotFoundError:
                If a file in the collection does not exist.

            FileExistsError:
                If a file in the backup directory already exists.

            PermissionError:
                If the user does not have permission to write to the backup directory.

            OSError:
                If an error occurs while creating the backup directory or copying files.
        """

        # Convert backup_dir to Path object if it's a string
        backup_dir = Path(backup_dir).expanduser().resolve()

        # Create the backup directory if it doesn't exist
        try:
            backup_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create backup directory: {backup_dir}") from e

        backup_files = []
        dest = Path(backup_dir)
        for file_path in self.files:
            try:
                # Copy each file to the backup directory
                dest = backup_dir / file_path.name
                shutil.copy2(file_path, dest)
                backup_files.append(dest)
            except FileNotFoundError:
                raise FileNotFoundError(f"File not found: {file_path}")
            except FileExistsError:
                raise FileExistsError(f"File already exists in backup: {dest}")
            except PermissionError:
                raise PermissionError(f"No permission to copy {file_path} to {dest}")
            except OSError as e:
                raise OSError(f"Error copying {file_path} to {dest}: {e}")

        # Archive the backup directory if requested
        if archive:
            if not skip_all_confirmations and not skip_archive_confirmation:
                confirm = input("Are you sure you want to archive the backup directory? (y/n): ")
                if confirm.lower() != 'y':
                    print("Archiving skipped.")
                    return backup_dir

            archive_path = shutil.make_archive(str(backup_dir), 'zip', root_dir=str(backup_dir))

            if delete_backups_on_archive:
                if not skip_all_confirmations and not skip_backup_delete_confirmation:
                    confirm = input(
                            f"Are you sure you want to delete the backup directory {backup_dir} after archiving? (y/n): ")
                    if confirm.lower() != 'y':
                        print("Backup directory not deleted.")
                        return Path(archive_path)
                shutil.rmtree(backup_dir)

            return Path(archive_path)

        # Delete the original files if requested
        if delete_originals:
            if not skip_all_confirmations and not skip_delete_originals_confirmation:
                confirm = input("Are you sure you want to delete the original files? (y/n): ")
                if confirm.lower() != 'y':
                    print("Original files not deleted.")
                    return backup_dir

            for file_path in self.files:
                try:
                    os.remove(file_path)
                except FileNotFoundError:
                    raise FileNotFoundError(f"Original file not found: {file_path}")
                except PermissionError:
                    raise PermissionError(f"No permission to delete original file: {file_path}")
                except OSError as e:
                    raise OSError(f"Error deleting original file {file_path}: {e}")

        return backup_dir

    def bucketize_file(self, file: FileType):
        """
        Bucketize a file.

        This method "bucketizes" a file into the local or remote bucket based on whether the file has
        a recall attribute. If the file has a recall attribute, it is bucketized into the remote
        bucket. If the file does not have a recall attribute, it is bucketized into the local bucket.

        Parameters:
            file

        Returns:

        """
        try:
            remote = file.has_recall_attribute
        except NotImplementedError:
            remote = False

        bucket = self.files['remote'] if remote else self.files['local']
        bucket['files'].append(file)
        bucket['total_size'] += file.size_in_bytes

    def get_file_object_hash(self):
        # Create a new hash object
        hash_obj = hashlib.sha256()

        if self.needs_processing:
            raise NeedsProcessingError("Files need to be processed before a hash can be generated.")

        for obj in self.file_objects.values():
            # Convert each object to a hashable representation (e.g., a string)
            obj_repr = repr(obj).encode('utf-8')

            # Update the hash object with this representation
            hash_obj.update(obj_repr)

        # Return the hexadecimal digest of the combined hash
        return hash_obj.hexdigest()


    def process_files(self):
        """
        Process the files in the collection.

        This method processes the files in the collection. It calculates the total size of the collection, the total number
        of files, and the total size of each extension in the collection. It populates the `total_size`, `total_files`, and
        `extensions` attributes of the class.

        Returns:
            None
        """
        from inspyre_toolbox.filesystem.file.helpers import get_file_object

        if all(isinstance(path, File) for path in self.paths):
            self.paths = [file.path for file in self.paths]
        elif all(isinstance(path, (str, Path)) for path in self.paths):
            self.paths = provision_paths(self.paths)

        with flag_lock(self, 'processing'):


            for path_str in self.paths:
                if isinstance(path_str, Path):
                    path_str = str(path_str)
                elif isinstance(path_str, File):
                    path_str = path_str.path

                file_name = Path(path_str).name

                file = get_file_object(path_str, skip_path_provision=True)

                self.file_objects[file_name] = file

                self.bucketize_file(file)

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
        self.get_file_object_hash()

    def find_file(
            self,
            path: Optional[Union[str, Path]],
            name: Optional[str] = None,
            include_remote: bool = False
            ) -> Union[File, None]:
        """
        Find a file in the collection.

        This method finds a file in the collection by its path. It takes a file path as an argument and returns the file
        object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            path (Optional[Union[str, Path]]):
                The file path to find.

            name (Optional[str]):
                The name of the file to find. If the name is provided, the method will search for the file by name instead

            include_remote (bool):
                A flag indicating whether to include remote files in the search. If True, the method will search both
                local and remote files. If False, the method will only search local files.

        Warning:
            = If the `name` and `path` parameters are both provided values, an `In


        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.
        """
        #     log = self.create_logger()

        if path and name:
            raise InvalidParameterCombinationError("Cannot provide both path and name parameters.")
        elif not path and not name:
            raise MissingRequiredParameterError("Either path or name parameter is required.")

        if name:
            return self.find_file_by_name(name, include_remote=include_remote, case_sensitive=False)
        elif path:
            return self.find_file_by_path(path, include_remote=include_remote)

        return None

    def find_file_by_name(self, name: str, include_remote: bool = False, case_sensitive: bool = False) -> Union[
        File, None]:
        # sourcery skip: swap-nested-ifs
        """
        Find a file in the collection by name.

        This method finds a file in the collection by its name. It takes a file name as an argument and returns the file
        object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            name (str):
                The name of the file to find.

            include_remote (bool):
                A flag indicating whether to include remote files in the search. If True, the method will search both
                local and remote files. If False, the method will only search local files.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.

        """
        if not case_sensitive:
            name = name.lower()

        if found_local := self.find_local_by_name(name, case_sensitive=case_sensitive):
            return found_local

        if include_remote:
            if found_remote := self.find_remote_by_name(name, case_sensitive=case_sensitive):
                return found_remote

        return None

    def find_local_by_name(self, name: str, case_sensitive: bool = False) -> Union[File, None]:
        """
        Find a local file in the collection by name.

        This method finds a local file in the collection by its name. It takes a file name as an argument and returns the
        file object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            name (str):
                The name of the file to find.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.

        """
        for file in self.files.local.files:
            if case_sensitive:
                if file.name == name:
                    return file

            elif file.name.lower() == name:
                return file

    def find_remote_by_name(self, name: str, case_sensitive: bool = False) -> Union[File, None]:
        """
        Find a remote file in the collection by name.

        This method finds a remote file in the collection by its name. It takes a file name as an argument and returns the
        file object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            name (str):
                The name of the file to find.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.

        """
        for file in self.files.remote.files:
            if case_sensitive:
                if file.name == name:
                    return file

            elif file.name.lower() == name:
                return file

    def find_file_by_path(self, path: Union[str, Path], include_remote: bool = False) -> Union[File, None]:
        """
        Find a file in the collection by path.

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
        path = provision_path(path)

        if found_local := self.find_local_by_path(path):
            return found_local

        if include_remote:
            if found_remote := self.find_remote_by_path(path):
                return found_remote

        return None

    def find_local_by_path(self, path: Union[str, Path]) -> Union[File, None]:
        """
        Find a local file in the collection by path.

        This method finds a local file in the collection by its path. It takes a file path as an argument and returns the
        file object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            path (Union[str, Path]):
                The file path to find.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.

        """
        path = provision_path(path)

        return next(
                (file for file in self.files.local.files if file.path == path), None
                )

    def find_remote_by_path(self, path: Union[str, Path]) -> Union[File, None]:
        """
        Find a remote file in the collection by path.

        This method finds a remote file in the collection by its path. It takes a file path as an argument and returns the
        file object if the file is in the collection. If the file is not in the collection, the method will return `None`.

        Parameters:
            path (Union[str, Path]):
                The file path to find.

        Returns:
            Union[File, None]:
                The file object if the file is in the collection, `None` otherwise.

        """
        path = provision_path(path)

        return next(
                (file for file in self.files.remote.files if file.path == path), None
                )

    def get_all_checksums(self, with_progress_bar=use_progress_bar):
        if self.needs_processing:
            raise NeedsProcessingError("Files need to be processed before checksums can be accessed.")

        with flag_lock(self, 'getting_checksums'):
            self.__checksums = {}

            if with_progress_bar:
                paths = tqdm(self.file_objects.items(), desc="Calculating checksums", unit="file")
            else:
                paths = self.file_objects.items()

            for name, file in paths:
                self.__checksums[name] = file.get_checksum()

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

    def remove_file(
            self,
            path: Optional[Union[Path, str]] = None,
            name: Optional[str] = None,
            **kwargs
            ):
        """
        Remove a file from the collection.

        This method removes a file from the collection. It takes a file path as an argument and removes the file from
        the collection. It then reprocesses the files in the collection to update the total size, total number of files,
        and total size of each extension.

        Parameters:
            path (Union[Path, str]):
                The file path to remove. If the path is provided, the method will search for the file by path. If the path
                is not provided, the method will search for the file by name.

            name (str):
                The name of the file to remove. If the name is provided, the method will search for the file by name instead

            **kwargs:
                Additional keyword arguments

        Note:
            This method does not delete the file from the file system. It only removes the file from the collection,
            and only if the file is in the collection. If the file is not in the collection, this method will raise a
            `KeyError`. After removing the file, the collection will be reprocessed to update the total size, total
            number of files, and total size of each extension.

        Note:
          - If the `name` and `path` parameters are both provided values, an `InvalidParameterCombinationError`
            will be raised.

          - If neither the `name` nor the `path` parameter is provided, a `MissingRequiredParameterError` will be
            raised.


        Raises:
            KeyError:
                If the file is not in the collection.

            InvalidParameterCombinationError:
                If the `name` and `path` parameters are both provided values.

            MissingRequiredParameterError:
                If neither the `name` nor the `path` parameter is provided.

        Returns:
            None
        """
        # log = self.create_child_logger()

        if path and name:
            raise InvalidParameterCombinationError("Cannot provide both path and name parameters.")
        elif not path and not name:

            raise MissingRequiredParameterError("Either path or name parameter is required.")

        old_paths = self.paths.copy()

        if name:
            self.remove_file_by_name(name, **kwargs)
        elif path:
            self.remove_file_by_path(path, **kwargs)

        if old_paths != self.paths:
            print('Paths have changed.')
            self.__needs_reprocessing = True
            self.reprocess_files()

    def remove_file_by_name(
            self,
            name: str,
            include_remote: bool = False,
            remove_all: bool = False,
            case_sensitive: bool = False
            ):
        """
        Remove a file from the collection by name.

        This method removes a file from the collection by name. It takes a file name as an argument and removes the file
        from the collection. It then reprocesses the files in the collection to update the total size, total number of
        files, and total size of each extension.

        If you do not want to include remote files in the search, set the `include_remote` parameter to `False`. If you
        want to include remote files in the search, set the `include_remote` parameter to `True`. By default, remote files
        are not included in the search.

        Parameters:
            name (str):
                The name of the file to remove.

            include_remote (bool):
                A flag indicating whether to include remote files in the search. If True, the method will search both
                local and remote files. If False, the method will only search local files. Default is False.

            remove_all (bool):
                A flag indicating whether to remove all files with the specified name. If True, all files with the specified
                name will be removed. If False, only the first file with the specified name will be removed. Default is False.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

        Returns:
            None
        """
        if not case_sensitive:
            name = name.lower()

        self.remove_local_by_name(name, case_sensitive=case_sensitive, remove_all=remove_all)

        if include_remote:
            self.remove_remote_by_name(name, case_sensitive=case_sensitive, remove_all=remove_all)

    def remove_local_by_name(self, name: str, case_sensitive=False, remove_all: bool = False):
        """
        Remove a local file from the collection by name.

        This method removes a local file from the collection by name. It takes a file name as an argument and removes the
        file from the collection. It then reprocesses the files in the collection to update the total size, total number
        of files, and total size of each extension.

        Parameters:
            name (str):
                The name of the file to remove.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

            remove_all (bool):
                A flag indicating whether to remove all files with the specified name. If True, all files with the specified
                name will be removed. If False, only the first file with the specified name will be removed. Default is False.

        Returns:
            None
        """
        if not case_sensitive:
            name = name.lower()

        files = self.files.local.files
        paths = self.paths

        for file in files:
            if file.name == name:
                fp = file.path
                if file in files:
                    files.remove(file)
                if fp in paths:
                    paths.remove(fp)

                if name in self.file_objects:
                    del self.file_objects[name]

    def remove_remote_by_name(self, name: str, case_sensitive=False, remove_all: bool = False):
        """
        Remove a remote file from the collection by name.

        This method removes a remote file from the collection by name. It takes a file name as an argument and removes the
        file from the collection. It then reprocesses the files in the collection to update the total size, total number
        of files, and total size of each extension.

        Parameters:
            name (str):
                The name of the file to remove.

            case_sensitive (bool):
                A flag indicating whether the search should be case-sensitive. If True, the search will be case-sensitive.
                If False, the search will be case-insensitive. Default is False.

            remove_all (bool):
                A flag indicating whether to remove all files with the specified name. If True, all files with the specified
                name will be removed. If False, only the first file with the specified name will be removed. Default is False.

        Returns:
            None
        """
        if not case_sensitive:
            name = name.lower()

        if remove_all:
            files = [file for file in self.files.remote.files if file.name == name]
        else:
            files = [next((file for file in self.files.remote.files if file.name == name), None)]

        for file in files:
            self.remove_file(file.path)

    def remove_file_by_path(self, path: Union[str, Path], include_remote: bool = False):
        """
        Remove a file from the collection by path.

        This method removes a file from the collection by its path. It takes a file path as an argument and removes the
        file from the collection. It then reprocesses the files in the collection to update the total size, total number
        of files, and total size of each extension.

        Parameters:
            path (Union[str, Path]):
                The file path to remove.

            include_remote (bool):
                A flag indicating whether to include remote files in the search. If True, the method will search both
                local and remote files. If False, the method will only search local files. Default is False.

        Returns:
            None
        """
        target_path = provision_path(path)
        local_files = self.path_strings

        if str(target_path) in local_files:
            self.remove_local_by_path(target_path)

        if include_remote:
            self.remove_remote_by_path(target_path, do_not_provision=True)

    def remove_local_by_path(self, path: Union[str, Path], do_not_provision=False):
        """
        Remove a local file from the collection by path.

        This method removes a local file from the collection by its path. It takes a file path as an argument and removes
        the file from the collection. It then reprocesses the files in the collection to update the total size, total number
        of files, and total size of each extension.

        Parameters:
            path (Union[str, Path]):
                The file path to remove.

            do_not_provision (bool):
                A flag indicating whether to skip path provisioning.
                  - If True; the path will not be provisioned before removing the file.
                  - If False; the path will be provisioned before removing the file.
                  - Default is False

        Raises:
            FileNotFoundError:
                If the file is not found in the collection.

        Returns:
            None
        """
        if not do_not_provision:
            target_path = provision_path(path)

        target_path = str(target_path)
        local_files = self.files.local.files
        paths = self.paths

        for file in self.files.local.files:
            if str(file.path) == target_path:
                local_files.remove(file)
                paths.remove(file.path)
                return

    def remove_remote_by_path(self, path: Union[str, Path], do_not_provision=False):
        """
        Remove a remote file from the collection by path.

        This method removes a remote file from the collection by its path. It takes a file path as an argument and removes
        the file from the collection. It then reprocesses the files in the collection to update the total size, total number
        of files, and total size of each extension.

        Parameters:
            path (Union[str, Path]):
                The file path to remove.

        Returns:
            None
        """
        if not do_not_provision:
            target_path = provision_path(path)

        target_path = str(target_path)

        for file in self.files.remote.files:
            if file.path == target_path:
                self.remove_file(file.path)
                return

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


def create_file_collection(paths: list[Path], **kwargs) -> FileCollection:
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
    return FileCollection(paths, **kwargs)


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
    files = gather_files_in_dir(root_dir, file_types=kwargs.pop('extensions'), recursive=recursive)
    return create_file_collection(
            files,
            **kwargs
            )
