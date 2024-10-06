"""


Author: 
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File: 
    inspyre_toolbox/type_parser/boolean.py
 

Description:
    

"""
from typing import Any, Optional

DEFAULT_TRUTHY_VALUES = ['true', 't', 'yes', 'y', '1', 1, True]
DEFAULT_FALSEY_VALUES = ['false', 'f', 'no', 'n', '0', 0, False]
DEFAULT_BOOLEAN_TYPES = (int, str, bool)


def __prepare_boolean_values(true_false: bool, additional: list[Any]=None, exclude: list[Any]=None):

    # If true_false is True, we are preparing truthy values
    if true_false:
        values = DEFAULT_TRUTHY_VALUES.copy()
    else:
        # If true_false is False, we are preparing falsey values
        values = DEFAULT_FALSEY_VALUES.copy()

    # If additional is None, set it to an empty list
    if additional is None:
        additional = []
    else:
        # If additional is not a list, convert it to a list
        if not isinstance(additional, list):
            additional = list(additional)

    # If exclude is None, set it to an empty list
    if exclude is None:
        exclude = []
    else:
        # If exclude is not a list, convert it to a list
        if not isinstance(exclude, list):
            exclude = list(exclude)

    # Remove excluded values
    for value in exclude:
        if value in values:
            values.remove(value)
        elif isinstance(value, str):
            if value.lower() in values:
                values.remove(value.lower())

    for value in values:
        if isinstance(value, str):
            values.append(value.lower())

    value_types = [type(value) for value in values]

    return values, value_types



def parse_boolean(
        value,
        false_on_not_found=False,
        false_on_error=False,
        truthy_additional: Optional[list[Any]]=None,
        truthy_exclude: Optional[list] = None,
        falsey_additional: Optional[list[Any]]=None,
        falsey_exclude: Optional[list] = None
):
    truthy_values, truthy_types = __prepare_boolean_values(True, truthy_additional, truthy_exclude)
    falsey_values, falsey_types = __prepare_boolean_values(False, falsey_additional, falsey_exclude)
