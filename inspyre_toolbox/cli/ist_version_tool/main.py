from inspyre_toolbox.cli.ist_version_tool.arguments import Arguments
from inspyre_toolbox.cli.ist_version_tool.errors import NonExistentCommandError
from inspyre_toolbox.console_kit import clear_console
from inspyre_toolbox.ver_man.classes.pypi import load_pypi_version_info

ARG_PARSER = Arguments()

PYPI_VER_INFO = load_pypi_version_info('inspyre-toolbox')


def handle_update_command():
    raise NotImplementedError('Update command is not implemented yet.')


def handle_version_command():
    """
    Handle the version command.

    Returns:
        None
    """
    clear_console()
    PYPI_VER_INFO.print_version_info()


def handle_command(args):
    command = args.command.lower()

    if command == 'version':
        handle_version_command()

    elif command == 'update':
        handle_update_command()
    else:
        raise NonExistentCommandError(command)


def main():
    args = ARG_PARSER.parse_args()
    print(args.command)
    handle_command(args)


if __name__ == '__main__':
    main()
