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

from argparse import ArgumentParser, _SubParsersAction

from inspyre_toolbox.cli.ist_version_tool.commands.registrar import CommandRegistrar
from inspyre_toolbox.common.meta import FULL_VERSION_STRING
from inspyre_toolbox.ver_man import PyPiVersionInfo

# Constants for program name and description
PROG = 'ist-version-tool'
DESCRIPTION = 'Get information about the version and update availability of the inspyre-toolbox package.'

# Exported names
__all__ = ['Arguments']


class Arguments(ArgumentParser):
    def __init__(
            self,
            *args,
            command_registrar=None,
            **kwargs,
    ):
        self.__registrar = None
        self.__command_parser = None

        if command_registrar is None:
            command_registrar = CommandRegistrar(self)

        self.registrar = command_registrar

        kwargs.setdefault('prog', PROG)
        kwargs.setdefault('description', DESCRIPTION)
        super().__init__(*args, **kwargs)

        self.add_argument('-v', '--version', action='version', version=f'Inspyre-Toolbox | {FULL_VERSION_STRING}')

        self.__parsed = None
        self.__build_command_parser()

    def __build_command_parser(self):
        if self.command_parser is None:
            self.__command_parser = self.add_subparsers(
                dest='subcommand',
                title='subcommands',
                metavar='<subcommand>',
                parser_class=ArgumentParser
            )

        self.set_defaults(func=PyPiVersionInfo('Inspyre-Toolbox').print_version_info)

    def __build_subcommands(self):
        subparsers = self.add_subparsers(
            dest='command',
            title='commands',
            metavar='<command>',
            parser_class=ArgumentParser
        )

        # version_parser = subparsers.add_parser('version', help='Show version information')
        # vp_subparsers  = version_parser.add_subparsers(dest='subcommand', title='subcommands', metavar='<subcommand>', parser_class=ArgumentParser)
        # vp_list_parser = vp_subparsers.add_parser('list', help='List all versions')
        # vp_list_parser.add_argument('--exclude-release-types', nargs='+', help='Exclude specific release types')
        # vp_list_parser.add_argument('--stable-only', action='store_true', help='Only show stable versions')
        # vp_list_parser.add_argument('--after', help='Only show versions after the specified version')
        # vp_list_parser.add_argument('--before', help='Only show versions before the specified version')

        update_parser = subparsers.add_parser('update', help='Check for updates')
        update_parser.add_argument('-c', '--check', action='store_true', help='Check for updates')
        update_parser.add_argument('-d', '--download', action='store_true', help='Download updates')

    @property
    def command_parser(self):
        return self.__command_parser

    @command_parser.setter
    def command_parser(self, new):
        if self.__command_parser is not None:
            raise ValueError('The command parser has already been set')

        if not isinstance(new, _SubParsersAction):
            raise ValueError('The command parser must be an instance of _SubParsersAction')

        self.__command_parser = new

    @property
    def registrar(self):
        return self.__registrar

    @registrar.setter
    def registrar(self, new):

        if self.__registrar is not None:
            raise ValueError('The registrar has already been set')

        if not isinstance(new, CommandRegistrar):
            raise ValueError(f'The registrar must be an instance of CommandRegistrar, not {type(new)}')

        self.__registrar = new

    @property
    def parsed(self):
        if self.__parsed is None:
            self.__parsed = self.parse_args()
        return self.__parsed
