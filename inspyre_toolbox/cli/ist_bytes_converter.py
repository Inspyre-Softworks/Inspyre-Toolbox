from argparse import ArgumentParser
from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.humanize import Numerical

"""
This script provides a command-line interface to convert between different units of digital information storage.
It uses the inspyre_toolbox library to perform the conversion and to humanize the numerical output.
The user can specify the amount and units for conversion, and the script will output the result in the desired unit.
"""

PROG = 'ist-bytes-converter'  # Name of the program for command-line interface
DESCRIPTION = 'Convert between information storage units.'  # Description of the program


class Arguments(ArgumentParser):
    """
    Custom ArgumentParser class for parsing command-line arguments for the byte converter program.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the custom ArgumentParser with program name and description
        """
        super().__init__(prog=PROG, description=DESCRIPTION)
        
        # Define the command-line arguments for the program
        self.add_argument('amount', type=float, help='The amount of storage units to convert.')
        self.add_argument('from_unit', type=str, nargs='?', default='bytes', help='The storage unit to convert from. Defaults to "bytes".')
        self.add_argument('to_unit', type=str, help='The storage unit to convert to.')
        
        self.__parsed = None  # Placeholder for parsed arguments
    
    @property
    def parsed(self):
        """
        Parses the command-line arguments and returns the parsed namespace object.

        Returns:
            argparse.Namespace:
                The namespace object containing the parsed arguments.
        """
        # Parse the arguments if they have not already been parsed
        if not self.__parsed:
            self.__parsed = super().parse_args()
        return self.__parsed

def clean_unit_str(unit_str):
    """
    Cleans and standardizes the unit string by removing plural 's' and converting to lowercase.

    Parameters:
        unit_str (str):
            The unit string to clean.

    Returns:
        str:
            The cleaned and standardized unit string
    """
    # Remove plural 's' and convert to lowercase for unit consistency
    return unit_str.rstrip('s').lower()

def main(cli_args=None):
    """
    Main function that handles the conversion between different units of digital information storage.

    Parameters:
        cli_args (argparse.Namespace, optional):
            Parsed command-line arguments. If `None`, the function will parse the arguments itself.
    
    Returns:
        None
    """
    # Main function to handle conversion
    args = Arguments().parsed if cli_args is None else cli_args  # Parse command-line arguments

    from_unit = clean_unit_str(args.from_unit)  # Clean and standardize the 'from' unit
    to_unit = clean_unit_str(args.to_unit)  # Clean and standardize the 'to' unit

    converter = ByteConverter(args.amount, from_unit)  # Initialize the ByteConverter with the specified amount and 'from' unit
    result = converter.convert(to_unit)  # Perform the conversion to the 'to' unit
    from_str = Numerical(args.amount, from_unit).count_noun()  # Humanize the 'from' amount and unit
    to_str = Numerical(result, to_unit).count_noun()  # Humanize the 'to' amount and unit

    # Output the conversion details and result
    print(f'Converting {from_str} to {to_str.split(" ")[-1]}')
    print(f'Result: {to_str}')
