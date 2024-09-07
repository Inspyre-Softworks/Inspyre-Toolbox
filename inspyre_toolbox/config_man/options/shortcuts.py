"""
This module provides shortcuts to the different option classes.

Classes:
    Option:
        The base class for all options.

    OptionLedger:
        A class to represent an option ledger.

    OptionLedgerEntry:
        A class to represent an entry in an option ledger

    OptionManager:
        A class to manage various options, acting like a dictionary with type enforcement

    YesNoOption:
        A class to represent a yes/no option.

    StringInputOption:
        A class to represent a string input option with a description.

Since:
    1.6.0
"""

from inspyre_toolbox.config_man.options import Option
from inspyre_toolbox.config_man.options.classes.string_input import StringInputOption
from inspyre_toolbox.config_man.options.classes.yes_no import YesNoOption
from inspyre_toolbox.config_man.options.ledger import OptionLedger, OptionLedgerEntry
from inspyre_toolbox.config_man.options.manager import OptionManager

__all__ = [
        'Option',
        'OptionLedger',
        'OptionLedgerEntry',
        'OptionManager',
        'YesNoOption',
        'StringInputOption'
        ]
