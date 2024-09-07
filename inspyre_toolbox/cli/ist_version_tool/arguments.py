"""
Command-line arguments for the ist-version-tool program.

This module defines a custom ArgumentParser class for parsing command-line arguments for the ist-version-tool program.

Attributes:
    PROG (str):
        The program name for the ArgumentParser.

    DESCRIPTION (str):
        The description for the ArgumentParser.

Classes:
    Arguments (class):
        A custom ArgumentParser class for the ist-version-tool program.

        This class inherits from argparse.ArgumentParser and customizes initialization to define specific command-line
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
                Parses the command-line arguments if not already done and returns the parsed namespace. If the arguments
                have already been parsed, it returns the stored namespace object. Otherwise, it parses the arguments and
                stores the result in the `__parsed` attribute.

                Note:
                    This method is a property and can be accessed as an attribute. It does not take any arguments.

    __all__ (list):
        A list of names to export when importing the module using 'from <module> import *'. It contains the 'Arguments'
        class for external access.


Example:
    To use the Arguments class in an external script, import it as follows:

    ```python
    from inspyre_toolbox.cli.ist_version_tool.arguments import Arguments
    ```

    You can then create an instance of the Arguments class to parse command-line arguments for the ist-version-tool program:

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
    """
    Custom ArgumentParser class for parsing command-line arguments for the byte converter program.

    This class inherits from argparse.ArgumentParser and customizes initialization to define specific
    command-line arguments needed for the conversion between information storage units.

    Attributes:
        __parsed (argparse.Namespace, optional): A namespace object containing the parsed arguments.
            It's initially None and gets populated after parsing command-line arguments.

    Methods:
        __init__: Initializes the custom ArgumentParser with predefined program name and description,
            and sets up the command-line arguments.
        parsed: Parses the command-line arguments if not already done and returns the parsed namespace.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the custom ArgumentParser with the program name, description, and command-line arguments.

        The method sets up the argument parser with a specific program name and description. It defines
        command-line arguments for specifying the amount of storage units to convert, the unit to convert
        from (optional, defaults to 'bytes'), and the unit to convert to.

        Args:
            *args: Variable length argument list for ArgumentParser.
            **kwargs: Arbitrary keyword arguments for ArgumentParser.
        """
        super().__init__(prog=PROG, description=DESCRIPTION, *args, **kwargs)
        self.__subparsers = {}
        self.__build_subcommands()
        self.__parsed = None  # Placeholder for parsed arguments

    def __build_subcommands(self):
        """
        Builds the subcommands for the version information tool.

        This method defines the subcommands for the version information tool, including the 'version' and 'update' commands.
        Each subcommand has its own set of arguments and help text.

        Returns:
            None
        """
        # Define the 'version' subcommand
        version_parser = self.add_subparsers(dest='command', title='subcommands', metavar='<command>')
        version_parser.add_parser('version', help='Show version information')

        # Define the 'update' subcommand
        update_parser = version_parser.add_parser('update', help='Check for updates')
        update_parser.add_argument('-c', '--check', action='store_true', help='Check for updates')
        update_parser.add_argument('-d', '--download', action='store_true', help='Download updates')

    @property
    def parsed(self):
        """
        Parses the command-line arguments if not already done and returns the parsed namespace.

        This method checks if the command-line arguments have already been parsed to avoid
        redundant parsing. If not already parsed, it parses the arguments and stores the result
        in the `__parsed` attribute.

        Returns:
            argparse.Namespace: The namespace object containing the parsed arguments.
        """
        if self.__parsed is None:
            self.__parsed = self.parse_args()
        return self.__parsed
