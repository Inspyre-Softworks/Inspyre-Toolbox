from inspyre_toolbox.cli.ist_version_tool.arguments import Arguments
from inspyre_toolbox.cli.ist_version_tool.errors import NonExistentCommandError
from inspyre_toolbox.console_kit import clear_console
from inspyre_toolbox.ver_man.classes.pypi import load_pypi_version_info

ARG_PARSER = Arguments()

PYPI_VER_INFO = load_pypi_version_info('inspyre-toolbox')


def handle_print_version_info():
    """
    Handle the print version info command.

    Returns:
        None
    """
    handle_version_command()


def handle_update_command():
    PYPI_VER_INFO.update()


def handle_version_command():
    """
    Handle the version command.

    Returns:
        None
    """
    clear_console()
    PYPI_VER_INFO.print_version_info()


def handle_command(args):
    if not args.command:
        return handle_print_version_info()

    command = args.command.lower()

    if command == 'version':
        handle_version_command()

    elif command == 'update':
        handle_update_command()
    else:
        raise NonExistentCommandError(command)


def main():
    args = ARG_PARSER.parse_args()

    handle_command(args)


if __name__ == '__main__':
    main()
