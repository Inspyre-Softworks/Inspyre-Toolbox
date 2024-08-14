from pathlib import Path
from typing import Optional, Union

from inspyre_toolbox.console_kit.prompts.dialogs import ConfirmationPrompt
from inspyre_toolbox.decor import frozen_property
from inspyre_toolbox.filesystem import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.filesystem.file.helpers import get_file_checksum
from inspyre_toolbox.log_engine import Loggable
from inspyre_toolbox.path_man import provision_path
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from inspyre_toolbox.sys_man.operating_system.checks import is_windows

MOD_LOGGER = PARENT_LOGGER.get_child('file')


class File(Loggable):

    def __init__(
            self,
            path: Union[str, Path],
            auto_get_checksum: bool = False,
            backup_dir: Union[str, Path] = None
            ):
        """
        Initialize the File object.

        Parameters:
            path (Union[str, Path]):
                The path to the file.

            auto_get_checksum (bool):
                Whether to automatically get the checksum of the file.

            backup_dir (Path, optional):
                The directory to back up the file to. If `None`, the file will be backed up to a directory named
                'backups' in the parent directory.
        """
        # Start the logger.
        super().__init__(MOD_LOGGER)

        self.__auto_get_checksum = auto_get_checksum
        self.__extension = None
        self.__size = None
        self.__backup_dir = None

        self.__checksum = None

        self.__has_recall_attribute = None


        if is_windows():
            from inspyre_toolbox.filesystem.file.attributes import file_has_recall_attribute

            self.has_recall_attribute = file_has_recall_attribute(path, do_not_provision=True)

        self.path = path

        if self.auto_get_checksum:
            self.checksum = get_file_checksum(self.path)

        # If backup_dir is not provided, set it to a directory
        # named 'backups' in the parent directory.
        if backup_dir is not None:
            self.backup_dir = backup_dir
        else:
            self.backup_dir = self.path.parent.joinpath('backups')

    @property
    def auto_get_checksum(self) -> bool:
        """
        Get whether the file should automatically get the checksum.
        Returns:
            bool:
                Whether the file should automatically get the checksum.
        """
        return self.__auto_get_checksum

    @property
    def backup_dir(self) -> Path:
        """
        Get the backup directory for the file.

        Returns:
            Path:
                The backup directory for the file.
        """
        return self.__backup_dir

    @backup_dir.setter
    @validate_type(str, Path, preferred_type=Path, conversion_funcs={str: provision_path})
    def backup_dir(self, new: Union[str, Path]):
        """
        Set the backup directory for the file.

        Parameters:
            new (Union[str, Path]):
                The new backup directory for the file.

        Returns:
            None
        """
        self.__backup_dir = Path(new)

    @property
    def backup_path(self) -> Path:
        """
        Get the backup path for the file.

        Note:
            This is a read-only property, and depends on :attr:`path` and :attr:`backup_dir`.

        Returns:
            Path:
                The backup path for the file.
        """
        return self.backup_dir / self.path.name

    @property
    def checksum(self) -> str:
        """
        Return the file's checksum.

        Returns:
            str:
                The file's checksum.

        Raises:
            FileNotFoundError:
                If the file is not found.
        """
        return self.__checksum

    @checksum.setter
    @frozen_property('checksum', allowed_types=str, restrict_setter=True)
    def checksum(self, new: str):
        """
        Set the file's checksum. This is a frozen property, and cannot be changed once set.

        Parameters:
            new (str):
                The new checksum for the file.

        Returns:
            None
        """
        self.__checksum = new

    @property
    def exists(self) -> bool:
        """
        Check if the file exists.

        Returns:
            bool:
                True if the file exists, False otherwise.
        """
        return self.path.exists()

    @property
    def extension(self) -> str:
        """
        Get the extension of the file.

        Returns:
            str:
                The extension of the file.
        """
        return self.__extension

    @property
    def has_recall_attribute(self) -> bool:
        """
        Check if the file has the recall attribute.

        Returns:
            bool:
                True if the file has the recall attribute, False otherwise.
        """
        if not is_windows():
            raise NotImplementedError("The 'has_recall_property' attribute is only available on Windows.")

        return self.__has_recall_attribute

    @has_recall_attribute.setter
    @frozen_property('has_recall_attribute', allowed_types=bool, restrict_setter=True)
    def has_recall_attribute(self, new):
        """
        Set whether the file has the recall attribute. This is a frozen property, and cannot be changed once set.

        Parameters:
            new (bool):
                Whether the file has the recall attribute.

        Returns:
            None
        """
        self.__has_recall_attribute = new

    @property
    def is_local(self) -> bool:
        """
        Check if the file is local.

        Returns:
            bool:
                True if the file is local, False otherwise.
        """
        try:
            non_local = self.has_recall_attribute
            return not non_local
        except NotImplementedError:
            return True

    @property
    def path(self) -> Path:
        """
        Get the path of the file.

        Returns:
            Path:
                The path of the file.
        """

        return self.__path

    @path.setter
    @frozen_property('path', allowed_types=(Path, str), restrict_setter=False)
    @validate_type(str, Path, preferred_type=Path, conversion_funcs={str: provision_path})
    def path(self, new: Union[str, Path]):
        """
        Set the path of the file.

        Args:
            new:

        Returns:

        """
        self.__path = Path(new)
        self.__extension = self.__path.suffix
        self.__size = self.__path.stat().st_size

    @property
    def size_in_bytes(self) -> int:
        """
        Get the size of the file in bytes.

        Returns:
            int:
                The size of the file in bytes.
        """
        return self.__size

    def back_up(self, backup_dir=None, backup_name=None, backup_extension=None, overwrite=False):
        """
        Back up the file.

        Parameters:

            backup_dir (Path, optional):
                The directory to back up the file to. If `None`, the :attr:`backup_dir` will be used.

            backup_name (str, optional):
                The name of the backup file. If `None`, the name of the file will be used.

            backup_extension (str, optional):
                The extension of the backup file. If `None`, the extension of the file will be used.

            overwrite (bool):
                Whether to overwrite the backup file if it already exists. If `False`, a :class:`FileExistsError` will
                be raised.

        Returns:
            None

        Raises:

            FileExistsError:
                If the backup file already exists and `overwrite` is `False`.
        """
        log = self.create_logger()
        log.debug('Backing up file.')

        if backup_dir is None:
            backup_dir = self.backup_dir

        if backup_name is None:
            backup_name = self.path.stem

        if backup_extension is None:
            backup_extension = self.extension

        backup_path = backup_dir / f'{backup_name}{backup_extension}'

        if backup_path.exists() and not overwrite:
            raise FileExistsError(f'The backup file already exists: {backup_path}')

        log.debug(f'Copying file to: {backup_path}')
        self.path.replace(backup_path)

    def copy(
            self,
            destination_dir,
            new_name=None,
            new_extension=None,
            overwrite=None,
            skip_confirm_on_non_local=False,
            skip_confirm_on_overwrite=False,
            confirmation_prompt=None
            ):
        """
        Copy the file to the specified directory.

        Parameters:
            destination_dir (Path):
                The directory to copy the file to.

            new_name (str, optional):
                The new name of the file.

            new_extension (str, optional):
                The new extension of the file.

            overwrite (bool):
                Whether to overwrite the file if it already exists in the destination directory. The user will
                be prompted for confirmation, unless `skip_confirm_on_overwrite` is `True`.

            skip_confirm_on_non_local (bool):
                Whether to skip the confirmation if the file is not local.

            skip_confirm_on_overwrite (bool):
                Whether to skip the confirmation if the file already exists in the destination directory.

        Returns:
            None

        Raises:
            FileExistsError:
                If the file already exists in the destination directory and `overwrite` is `False`.
        """
        log = self.create_logger()
        log.debug(f'Copying file to: {destination_dir}')
        if self.has_recall_attribute:
            recall_prompt_text = ('The file is not local. Copying would require downloading the file. Are you sure you '
                                  'want to '
                                  f'proceed? \n\nDestination: {destination_dir}\n\nFile: {self.path}\n\nSize: {self.size_in_bytes} bytes')

            if not skip_confirm_on_non_local:
                if confirmation_prompt is None:
                    confirmation_prompt = ConfirmationPrompt(
                            title='Non-Local File',
                            text='The file is not local. Are you sure you want to proceed?',
                            no_text_stub=True,
                            no_title_stub=True
                            )

                confirmation_prompt.run()

                if not confirmation_prompt.answer:
                    denied_statement = 'User did not confirm to proceed with the download.'

                    log.debug(denied_statement)
                    log.error(denied_statement)
                    return

                log.debug('User confirmed to proceed with the download.')

        if new_name is None:
            new_name = self.path.stem

        if new_extension is None:
            new_extension = self.extension

        destination_path = provision_path(destination_dir / f'{new_name}{new_extension}')

        if destination_path.exists() and not overwrite and not skip_confirm_on_overwrite:
            raise FileExistsError(f'The file already exists in the destination directory: {destination_path}')

        log.debug(f'Copying file to: {destination_path}')
        self.path.replace(destination_path)

    def move(self, destination_dir, new_name=None, new_extension=None, overwrite=False):
        """
        Move the file to the specified directory.

        Parameters:
            destination_dir (Path):
                The directory to move the file to.
            new_name (str, optional):
                The new name of the file.
            new_extension (str, optional):
                The new extension of the file.
            overwrite (bool):
                Whether to overwrite the file if it already exists in the destination directory.

        Returns:
            None

        Raises:
            FileExistsError:
                If the file already exists in the destination directory and `overwrite` is `False`.
        """
        log = self.create_logger()
        log.debug(f'Moving file to: {destination_dir}')

        if new_name is None:
            new_name = self.path.stem

        if new_extension is None:
            new_extension = self.extension

        destination_path = provision_path(destination_dir / f'{new_name}{new_extension}')

        if destination_path.exists() and not overwrite:
            raise FileExistsError(f'The file already exists in the destination directory: {destination_path}')

        log.debug(f'Moving file to: {destination_path}')
        self.path.replace(destination_path)

    def get_checksum(
            self,
            recalculate=False,
            skip_confirm_on_non_local=False,
            confirmation_prompt=None,
            error_on_fail=False
            ) -> Optional[str]:
        """
        Get the checksum of the file.

        Parameters:
            recalculate (bool):
                Whether to recalculate the checksum.
            skip_confirm_on_non_local (bool):
                Whether to skip the confirmation if the file is not local.
            confirmation_prompt (ConfirmationPrompt, optional):
                The confirmation prompt to use if the file is non-local.
            error_on_fail (bool):
                Whether to raise an error if the user does not confirm.

        Returns:
            str:
                The checksum of the file.
        """
        log = self.create_logger()
        non_local = not self.is_local
        log.debug(f'File is non-local: {non_local}')

        if non_local and not skip_confirm_on_non_local:
            if confirmation_prompt is None:
                confirmation_prompt = ConfirmationPrompt(
                        title='Non-Local File',
                        text='The file is not local. Are you sure you want to proceed?',
                        no_text_stub=True,
                        no_title_stub=True
                        )

            confirmation_prompt.run()

            if not confirmation_prompt.answer:
                denied_statement = 'User did not confirm to proceed with the download.'

                log.debug(denied_statement)
                log.error(denied_statement)

                if error_on_fail:
                    raise PermissionError(denied_statement)
                return None

            log.debug('User confirmed to proceed with the download.')

        if recalculate or not self.checksum:
            self.checksum = get_file_checksum(self.path)

        return self.checksum


def non_local_confirmation_prompt(file: File, operation=None, text=None) -> ConfirmationPrompt:
    """
    Create a confirmation prompt for a non-local file.

    Parameters:
        file (File):
            The file to create the prompt for.

        operation (str, optional):
            The operation to perform on the file. If provided, the prompt will include the operation in the text.

        text (str, optional):
            The text to include in the prompt. If provided, the operation will be ignored.

    Returns:
        ConfirmationPrompt:
            The confirmation prompt for the non-local file.
    """
    operations = {
            'checksum': 'Calculating the checksum for',
            'copy':     'copying',
            'move':     'moving',
            'backup':   'backing-up'
            }

    title = 'Non-Local File'

    if operation is None and text is None:
        raise ValueError('Either `operation` or `text` must be specified.')

    if text is None and operation in operations:
        text = (f'The file is not local. {operations[operation.lower()]} the file would require downloading the it. '
                'Are you sure you want to proceed?\n\n'
                f'Operation: {operations[operation]}\nFile: {file.path}\nSize: {file.size_in_bytes} bytes')

    prompt = ConfirmationPrompt(title=title, text=text, no_text_stub=True, no_title_stub=True)

    return prompt
