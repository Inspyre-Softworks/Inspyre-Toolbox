from inspyre_toolbox.cli.ist_version_tool.commands.registrar import CommandRegistrar

REGISTRAR = CommandRegistrar()

REGISTRAR.inject_all()

ARG_PARSER = REGISTRAR.argument_parser
CMD_PARSER = ARG_PARSER.command_parser


def main():
    ARG_PARSER.parsed.func(ARG_PARSER.parsed)



if __name__ == '__main__':
    main()
