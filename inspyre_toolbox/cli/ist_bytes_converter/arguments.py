"""
This module provides a command-line interface for converting between different information storage units.
It includes a custom ArgumentParser class that parses the user input, allowing for conversion operations
between various storage units, with 'bytes' as the default unit to convert from.

Usage:
    python ist_bytes_converter.py <amount> [<from_unit>] <to_unit>

Example:
    python ist_bytes_converter.py 1024 bytes KB
    This will convert 1024 bytes to kilobytes.
"""

from argparse import ArgumentParser

# Constants for program name and description
PROG = 'ist-bytes-converter'
DESCRIPTION = 'Convert between information storage units.'

# Exported names
__all__ = ['Arguments']


class Arguments(ArgumentParser):
    """
    Custom ArgumentParser class for parsing command-line arguments for the byte converter program.

    This class inherits from argparse.ArgumentParser and customizes initialization to define specific
    command-line arguments needed for the conversion between information storage units.

    Attributes:
        __parsed (argparse.Namespace, optional): A namespace object containing the parsed arguments.
            It's initially None and gets populated after parsing command-line arguments.
    
    Methods:
        __init__: Initializes the custom ArgumentParser with predefined program name and description,
            and sets up the command-line arguments.
        parsed: Parses the command-line arguments if not already done and returns the parsed namespace.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the custom ArgumentParser with the program name, description, and command-line arguments.

        The method sets up the argument parser with a specific program name and description. It defines
        command-line arguments for specifying the amount of storage units to convert, the unit to convert
        from (optional, defaults to 'bytes'), and the unit to convert to.

        Args:
            *args: Variable length argument list for ArgumentParser.
            **kwargs: Arbitrary keyword arguments for ArgumentParser.
        """
        super().__init__(prog=PROG, description=DESCRIPTION, *args, **kwargs)
        
        # Define the command-line arguments for the program
        self.add_argument('amount', type=float, help='The amount of storage units to convert.')
        self.add_argument('from_unit', type=str, nargs='?', default='bytes',
                          help='The storage unit to convert from. Optional, defaults to "bytes".')
        self.add_argument('to_unit', type=str, help='The storage unit to convert to.')
        
        self.__parsed = None  # Placeholder for parsed arguments
    
    @property
    def parsed(self):
        """
        Parses the command-line arguments if not already done and returns the parsed namespace.

        This method checks if the command-line arguments have already been parsed to avoid
        redundant parsing. If not already parsed, it parses the arguments and stores the result
        in the `__parsed` attribute.

        Returns:
            argparse.Namespace: The namespace object containing the parsed arguments.
        """
        if self.__parsed is None:
            self.__parsed = self.parse_args()
        return self.__parsed
