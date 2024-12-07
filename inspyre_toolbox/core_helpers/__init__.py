#  Copyright (c) 2024. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech


import inspect
from typing import Any, Union


def is_class(obj: Any) -> bool:
    """
    Determine if an object is a class.

    Parameters:
        obj (Any):
            The object to check.

    Returns:
        bool:
            True if the object (:param:`obj`) is a class; False otherwise.

    Since:
        1.6.0

    Example:
        >>> is_class(str)
        True
        >>> is_class('string')
        False
    """
    return inspect.isclass(obj)


def is_instance(obj: Any) -> bool:
    """
    Determine if an object is an instance of a class, excluding classes themselves.

    Parameters:
        obj (Any):
            The object to check.

    Returns:
        bool:
            :bool:`True` if the provided object (:param:`obj`) is an instance of a class; :bool:`False`,
            otherwise.

    Since:
        1.6.0

    Example:
        >>> is_instance(str)
        False
        >>> is_instance('string')
        True
    """
    return not is_class(obj) and not isinstance(obj, type)


def commify(number: Union[int, float], separator: str = ',') -> str:
    """
    Convert a number to a string with thousands separators.

    This function formats integers and floating-point numbers into a string where thousands are separated by the specified character.

    Parameters:
        number (Union[int, float]):
            The number to convert. Must be an integer or floating-point number.
            separator (str): The character to use as the thousands' separator. Defaults to ','.

    Returns:
        str:
            The number as a string with the specified thousands separators.

    Raises:
        ValueError:
            If the input is not a valid number (int or float), or if the separator is an empty string.

    Since:
        1.6.0

    Example:
        >>> commify(1000000)
        '1,000,000'

        >>> commify(1000000, separator=' ')
        '1 000 000'

        >>> commify(-1234567.89, separator='.')
        '-1.234.567.89'
    """
    if not isinstance(number, (int, float)):
        raise ValueError("Input must be an integer or float")
    if not separator:
        raise ValueError("Separator must be a non-empty string")

    # Create a formatted string with the default comma separator
    formatted = f'{number:,}'

    # Replace commas with the specified separator
    return formatted.replace(',', separator)
