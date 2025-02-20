"""
Command-line arguments for the ist-version-tool program.

This module defines a custom `ArgumentParser` class for parsing command-line arguments for the ist-version-tool program.

Attributes:
    PROG (str):
        The program name for the ArgumentParser.

    DESCRIPTION (str):
        The description for the ArgumentParser.

Classes:
    Arguments (class):
        A custom ArgumentParser class for the ist-version-tool program.

        This class inherits from `argparse.ArgumentParser` and customizes initialization to define specific command-line
        arguments needed for the version information tool. It provides a method to parse the command-line arguments and
        return the parsed namespace object.

        Properties:
            parsed (argparse.Namespace):
                Parses the command-line arguments if not already done and returns the parsed namespace. If the arguments
                have already been parsed, it returns the stored namespace object. Otherwise, it parses the arguments and
                stores the result in the `__parsed` attribute.

        Methods:
            __init__:
                Initializes the custom ArgumentParser with predefined program name and description, and sets up the
                command-line arguments.

            parsed:
                Parses the command-line arguments if not already done and returns the parsed namespace.

Example:
    To use the Arguments class in an external script, import it as follows:

    ```python
    from inspyre_toolbox.cli.ist_version_tool.arguments import Arguments
    ```

    You can then create an instance of the `Arguments` class to parse command-line arguments for the ist-version-tool program:

    ```python
    args = Arguments().parsed
    ```

    The `args` variable will contain the parsed command-line arguments as a namespace object.
"""

from argparse import ArgumentParser

# Constants for program name and description
PROG = 'ist-version-tool'
DESCRIPTION = 'Get information about the version and update availability of the inspyre-toolbox package.'

# Exported names
__all__ = ['Arguments']


class Arguments(ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('prog', PROG)
        kwargs.setdefault('description', DESCRIPTION)
        super().__init__(*args, **kwargs)
        self.__parsed = None
        self.__build_subcommands()

    def __build_subcommands(self):
        subparsers = self.add_subparsers(
            dest='command',
            title='subcommands',
            metavar='<command>',
            parser_class=ArgumentParser
        )

        subparsers.add_parser('version', help='Show version information')
        update_parser = subparsers.add_parser('update', help='Check for updates')
        update_parser.add_argument('-c', '--check', action='store_true', help='Check for updates')
        update_parser.add_argument('-d', '--download', action='store_true', help='Download updates')

    @property
    def parsed(self):
        if self.__parsed is None:
            self.__parsed = self.parse_args()
        return self.__parsed
