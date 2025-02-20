from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class CustomRootException(Exception):
    """Base class for exceptions in the CustomRoot module."""
    PANEL = Panel
    PANEL_TEXT = Text

    default_message = 'An unknown error has occurred.'

    def __init__(self, message: Optional[str] = None, skip_print: bool = False):
        """
        Initialize the CustomRootException.

        Args:
            message (Optional[str]): The error message. Defaults to None.
            skip_print (bool): Whether to skip printing the error message. Defaults to False.
        """
        super().__init__(message or self.default_message)
        self.__message = None
        self.__printed = False
        self._skip_print = None
        self.message = message or self.default_message

        self.skip_print = skip_print

        if not self.skip_print:
            self.print_rich_panel()

    @property
    def message(self):
        """
        Get the error message.

        Returns:
            str: The error message.
        """
        additional_message = ''
        if hasattr(self, 'additional_message') and self.additional_message:
            additional_message = f'\n\n[Additional Information]:\n    {self.additional_message}\n\n'
        return f'\n\n  {self.__message}{additional_message}'

    @message.setter
    def message(self, new):
        """
        Set the error message.

        Args:
            new (str): The new error message.

        Raises:
            ValueError: If the message is already set or if the new message is not a string.
        """
        if self.__message:
            raise ValueError("Reassignment of message attribute is not allowed. Message is immutable once set.")

        if not isinstance(new, str):
            raise ValueError("message must be a string.")

        self.__message = new.strip()

    @property
    def printed(self):
        """
        Check if the error message has been printed.

        Returns:
            bool: True if the error message has been printed, False otherwise.
        """
        return self.__printed

    @property
    def skip_print(self):
        """
        Check if printing the error message is skipped.

        Returns:
            bool: True if printing the error message is skipped, False otherwise.
        """
        return self._skip_print

    @skip_print.setter
    def skip_print(self, new):
        """
        Set whether to skip printing the error message.

        Args:
            new (bool): Whether to skip printing the error message.

        Raises:
            ValueError: If the new value is not a boolean.
        """
        if not isinstance(new, bool):
            raise ValueError('skip_print must be a boolean.')

        if not self.printed:
            self._skip_print = new

    def print_rich_panel(self):
        """
        Print the error message as a rich panel.
        """
        console = Console()
        console.print(self.__rich__())
        self.__printed = True

    def __rich__(self):
        """
        Get the rich representation of the error message.

        Returns:
            Panel: The rich panel containing the error message.
        """
        return Panel(
            Text(self.message, style='bold red'),
                title=self.__class__.__name__,
                style='bold red',
                )

    def __str__(self):
        """
        Get the string representation of the error message.

        Returns:
            str: The error message.
        """
        return self.message
