"""
File:
    inspyre_toolbox/cli/ist_bytes_converter/helpers

Author:
    Inspyre-Softworks
    Taylor-Jayde <t.blackstone@inspyre.tech>

Description:
    Helpers for the `ist-bytes-converter` CLI-App.

Functions:
    clean_unit_str:
        Cleans and standardizes the  unit string by removing plural 's' and converting to lowercase.

Variables:
    __all__:

"""


__all__ = [
    'clean_unit_str',
    'convert_if_whole_number'
]


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


def convert_if_whole_number(value):
    """
    Convert a float to an integer if the float is a whole number.

    Args:
        value (float): The float value to be converted.

    Returns:
        int or float: The converted integer if `value` is a whole number, otherwise the original float.

    Example:
        >>> convert_if_whole_number(3.0)
        3
        >>> convert_if_whole_number(3.5)
        3.5
    """
    if value.is_integer():
        return int(value)
    else:
        return value

