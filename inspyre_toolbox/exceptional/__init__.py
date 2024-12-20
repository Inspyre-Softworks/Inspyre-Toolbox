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

        Args:
            message:
        """
        super().__init__(message or self.default_message)
        self.__printed = False
        self._skip_print = None
        self.message = message or self.default_message

        self.skip_print = skip_print

        if not self.skip_print:
            self.print_rich_panel()

    @property
    def printed(self):
        return self.__printed

    @property
    def skip_print(self):
        return self._skip_print

    @skip_print.setter
    def skip_print(self, new):
        if not isinstance(new, bool):
            raise ValueError('skip_print must be a boolean.')

        if not self.printed:
            self._skip_print = new

    def print_rich_panel(self):
        console = Console()
        console.print(self.__rich__())
        self.__printed = True

    def __rich__(self):
        return Panel(
                Text(self.message, style='bold red'),
                title=self.__class__.__name__,
                style='bold red',
                )

    # Create a __str__ method that returns the rich rendering
    def __str__(self):
        return self.message
