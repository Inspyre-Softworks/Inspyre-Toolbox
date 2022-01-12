#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
import argparse
from inspyre_toolbox.spanners.span_arg_parse import SubparserActionAliases

if __name__ == '__main__':
    # An example parser with subcommands.
    
    parser = argparse.ArgumentParser()
    parser.register('action', 'parsers', SubparserActionAliases)
    parser.add_argument(
            "--library", metavar="libfile",
            type=str, help="library database filename")
    
    subparsers = parser.add_subparsers(title="commands", metavar="COMMAND")
    
    p_import = subparsers.add_parser(
            "import", help="add files to library",
            aliases=('imp', 'im'))
    
    p_import.add_argument(
            "filename", metavar="file", type=str,
            nargs="+", help="the files to import")
    
    p_remove = subparsers.add_parser(
            "remove", aliases=('rm',),
            help="remove items")

    args = parser.parse_args()
    
    print(args)
