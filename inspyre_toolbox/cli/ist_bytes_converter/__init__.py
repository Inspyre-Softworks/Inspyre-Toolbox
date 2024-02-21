"""
This script provides a command-line interface to convert between different units of digital information storage.
It uses the inspyre_toolbox library to perform the conversion and to humanize the numerical output.
The user can specify the amount and units for conversion, and the script will output the result in the desired unit.
"""


# Our imports
from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.humanize import Numerical
from inspyre_toolbox.cli.ist_bytes_converter.arguments import Arguments
from inspyre_toolbox.cli.ist_bytes_converter.helpers import clean_unit_str, convert_if_whole_number


# Define a function to handle the main application operations.
def main(cli_args=None):
    """
    Main function that handles the conversion between different units of digital information storage.

    Parameters:
        cli_args (argparse.Namespace, optional):
            Parsed command-line arguments. If `None`, the function will parse the arguments itself.
    
    Returns:
        None
    """
    # If `cli_args` is `None` we should create an instance 
    # of the parser.
    args = Arguments().parsed if cli_args is None else cli_args  # Parse command-line arguments

    # Gather the arguments from the command-line
    from_unit = clean_unit_str(args.from_unit)  # Clean and standardize the 'from' unit
    to_unit = clean_unit_str(args.to_unit)  # Clean and standardize the 'to' unit

    # Grab our given amount and pass it to be converted to an integer if
    # it is a whole number.
    amount = convert_if_whole_number(args.amount)

    # Create a converter object.
    converter = ByteConverter(amount, from_unit)  # Initialize the ByteConverter with the specified amount and 'from' unit
   
    # Use it to convert from our starting unit to the target unit.
    result = converter.convert(to_unit)  # Perform the conversion to the 'to' unit

    # Grab our result and pass it to be converted to an integer if it is a whole number.
    result = convert_if_whole_number(result)
    
    # Format our starting string properly by;
    #   - Passing it through the `Numerical` class,
    #   - Grabbing the resulting string and break it into a list delimited by a space,
    #   - Grab the last item in the list that results from the above operation.
    from_str = Numerical(amount, from_unit, store_as_float=False).count_noun()  # Humanize the 'from' amount and unit
    
    # Format out target string properly by;
    #   - Passing it through the `Numerical` class,
    #   - Grabbing the resulting string and break it into a list delimited by a space,
    #   - Grab the last item in the list that results from the above operation.
    to_str = Numerical(result, to_unit, store_as_float=False).count_noun()  # Humanize the 'to' amount and unit

    # Output the conversion details and result
    print(f'Converting {from_str} to {to_str.split(" ")[-1]}')
    print(f'Result: {to_str}')
