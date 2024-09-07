from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class CustomRootException(Exception):
    """Base class for exceptions in the CustomRoot module."""
    PANEL = Panel
    PANEL_TEXT = Text

    default_message = 'An unknown error has occurred.'

    def __init__(self, message: Optional[str] = None):
        """

        Args:
            message:
        """
        super().__init__(message or self.default_message)
        self.message = message or self.default_message
        self.print_rich_panel()

    def print_rich_panel(self):
        console = Console()
        console.print(self.__rich__())

    def __rich__(self):
        return Panel(
                Text(self.message, style='bold red'),
                title=self.__class__.__name__,
                style='bold red',
                )

    # Create a __str__ method that returns the rich rendering
    def __str__(self):
        return self.message
