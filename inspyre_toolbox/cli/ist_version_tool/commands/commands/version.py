from inspyre_toolbox.cli.ist_version_tool.commands.base import Command
from inspyre_toolbox.cli.ist_version_tool.commands.registrar import CommandRegistrar


class VersionCommand(Command):
    """
    Command for handling version-related functionality.

    This command registers itself with the argument parser from CommandRegistrar
    and provides options to display version details.
    """

    def __init__(self):
        self.__command_parser = None

    @property
    def command_parser(self):
        return self.__command_parser

    @property
    def list_subparser(self):
        return self.__list_subparser

    @property
    def subparsers(self):
        return self.__subparsers

    def inject(self):
        """
        Injects the version command into the argument parser.

        This method adds the 'version' command and its subcommands to the parser.
        """
        registrar = CommandRegistrar()
        parser = registrar.argument_parser
        self.__command_parser = parser.command_parser.add_parser('version', help='Show version information')
        version_parser = self.command_parser
        version_parser.set_defaults(func=self.print_version)

        # Add subcommands under 'version'
        self.__subparsers = version_parser.add_subparsers(
            dest='subcommand',
            title='subcommands',
            metavar='<subcommand>',
            parser_class=parser.__class__
        )

        self.inject_subcommands()

    def inject_list(self):
        self.__list_subparser = self.subparsers.add_parser('list', help='List all versions')
        self.list_subparser.add_argument('--exclude-releases', nargs='+', help='Exclude specific release types')
        self.list_subparser.add_argument('--stable-only', action='store_true', help='Only show stable versions')
        self.list_subparser.add_argument('--after', help='Only show versions after the specified version')
        self.list_subparser.add_argument('--before', help='Only show versions before the specified version')

        self.list_subparser.set_defaults(func=self.list_versions)

    def inject_subcommands(self):
        self.inject_list()

    def list_versions(self, args):
        from inspyre_toolbox.ver_man import PyPiVersionInfo
        pypi = PyPiVersionInfo('Inspyre-Toolbox')

        versions = pypi.get_all_versions(
            exclude_pre_releases=args.stable_only,
            before_version=args.before,
            after_version=args.after,
            excluded_versions=args.exclude_releases
        )

        for version in versions:
            print(version)

    def print_version(self, args):
        from inspyre_toolbox.ver_man import VersionParser, PyPiVersionInfo
        pypi = PyPiVersionInfo('Inspyre-Toolbox')
        version = VersionParser(str(pypi.installed)).full_version_string
        print(f'Installed version: {version}')


VersionCommand.register()
