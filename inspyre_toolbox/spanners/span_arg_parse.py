# !/usr/bin/env python

# This file was originally written by jirihnidek (username on GitHub), here are some links
# regarding the original code:
#
# Author's Website:        https://jirihnidek.github.io/
# Author Gist Page:        https://gist.github.com/jirihnidek
# Source of Original Code: https://gist.github.com/jirihnidek/3f5d36636198e852280f619847d22d9e

"""Aliases for argparse positional arguments."""

import argparse


class SubparserActionAliases(argparse._SubParsersAction):
    class _AliasedPseudoAction(argparse.Action):

        def __init__(self, name, aliases, help):
            dest = name
            if aliases:
                dest += f" ({','.join(aliases)})"
            sup = super(SubparserActionAliases._AliasedPseudoAction, self)
            sup.__init__(option_strings=[], dest=dest, help=help)

    def add_parser(self, name, **kwargs):
        """
        The add_parser function adds a parser to the subparsers object.
        It adds it to the _name_parser_map dictionary, which maps command \
        name aliases to parsers. It also adds an entry in _choices_actions, which is used by argparse
        to create help text for each of these commands.

        Args:
            name:
                Specify the name of the command
            **kwargs:
                Pass a dictionary of keyword arguments to the add_parser function

        Returns:
            The parser object, which we can then use to add arguments to
        """
        if 'aliases' in kwargs:
            aliases = kwargs['aliases']
            del kwargs['aliases']
        else:
            aliases = []

        parser = super(SubparserActionAliases, self).add_parser(name, **kwargs)

        # Make the aliases work.
        for alias in aliases:
            self._name_parser_map[alias] = parser
        # Make the help text reflect them, first removing old help entry.
        if 'help' in kwargs:
            help = kwargs.pop('help')
            self._choices_actions.pop()
            pseudo_action = self._AliasedPseudoAction(name, aliases, help)
            self._choices_actions.append(pseudo_action)

        return parser
