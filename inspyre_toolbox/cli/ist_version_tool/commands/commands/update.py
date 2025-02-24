import subprocess

from inspyre_toolbox.cli.ist_version_tool.commands.base import Command
from inspyre_toolbox.ver_man import PyPiVersionInfo


class UpdateCommand(Command):
    """
    Command for handling package updates.

    This command registers itself with the argument parser from CommandRegistrar
    and provides options to update Inspyre-Toolbox.
    """

    def __init__(self):
        self.__command_parser = None

    @property
    def command_parser(self):
        return self.__command_parser

    def inject(self):
        """
        Injects the update command into the argument parser.

        This method adds the 'update' command and its subcommands to the parser.
        """
        parser = self.REGISTRAR.argument_parser
        self.__command_parser = parser.command_parser.add_parser('update',
                                                                 help='Update Inspyre-Toolbox to the latest version')

        self.command_parser.add_argument('-c', '--check-only', action='store_true',
                                         help='Check for updates without updating')
        self.command_parser.add_argument('-d', '--download', action='store_true', help='Download updates')
        self.command_parser.add_argument('-f', '--force', action='store_true',
                                         help='Force update even if already up to date')
        self.command_parser.set_defaults(func=self.update_package)

    def update_package(self, args):
        """
        Updates the Inspyre-Toolbox package using pip.
        """
        pypi = PyPiVersionInfo('Inspyre-Toolbox')

        if not pypi.update_available and not args.force:
            print("Inspyre-Toolbox is already up to date.")
            return

        if args.check_only:
            pypi.check_for_update()
            if not pypi.update_available:
                print(f"\nInspyre-Toolbox is already up to date.\n\n"
                      f"|| PyPi Latest\n"
                      f"||   | Stable: {pypi.latest}\n"
                      f"||   | Pre-Release: {pypi.latest_pre_release}\n"
                      f"|| Installed: {pypi.installed}\n\n")
            else:
                print(f"A new version of Inspyre-Toolbox is available: {pypi.latest}")

            return

        print("Updating Inspyre-Toolbox...")

        try:
            if args.download:
                subprocess.run(['pip', 'download', '--upgrade', 'inspyre-toolbox'], check=True)
            else:
                subprocess.run(["pip", "install", "--upgrade", "inspyre-toolbox"], check=True)

            print("Update completed successfully.")

        except subprocess.CalledProcessError:
            print("Failed to update Inspyre-Toolbox. Please check your pip installation and network connection.")


UpdateCommand.register()
