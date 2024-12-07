from argparse import ArgumentParser

from inspyre_toolbox.sys_man.operating_system.checks import is_linux

# Constants for program name and description
PROG = 'ist-add-to-path'
DESCRIPTION = 'Add a program path to the system PATH environment variable.'

LINUX = is_linux()

del is_linux


class Arguments(ArgumentParser):

    def __init__(self, *args, **kwargs):
        super().__init__(prog=PROG, description=DESCRIPTION, *args, **kwargs)

        # Define the command-line arguments for the program
        self.add_argument(
                'NEW PATH',
                type=str,
                help='The full path to the directory you want to add to the system PATH.'
                )

        if LINUX:
            self.add_argument(
                    '-f', '--file',
                    type=str,
                    help='The file to add the path to. Defaults to ~/.bashrc.',
                    required=False,
                    action='store'
                    )
        else:
            self.add_argument(
                    '-d', '--do-not-notify',
                    help='Do not notify the environment of changes.',
                    required=False,
                    action='store_true'
                    )

        self.__parsed = None

    @property
    def parsed(self):
        """
        Parse the command-line arguments and return the parsed arguments.

        Returns:
            Namespace:
                The parsed command-line arguments.

        """
        if not self.__parsed:
            self.__parsed = self.parse_args()
        return self.__parsed
