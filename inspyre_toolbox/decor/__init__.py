"""


Author:
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File:
    inspyre_toolbox/decor/__init__.[y

Description:
    This module contains decorators that can be used to add functionality to classes and functions.

    The available decorators are:
        - method_alias: A decorator that allows you to add aliases to a class's method.
        - add_aliases: A decorator to add aliases to a class's methods.
        - validate_type: A decorator for validating the type and optionally the value of a value passed to a class
          property setter, with an option to convert to a preferred type if specified and to enforce value restrictions.
        - validate_func_args: A decorator for validating the type and optionally the value of arguments passed to a function.
"""
from functools import wraps
from typing import Optional

from .descriptors import RestrictedSetter


def convert_to_preferred_type(preferred_types):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            new_args = []
            for i, (arg, _) in enumerate(zip(args, preferred_types)):
                preferred_type = preferred_types[i]
                if preferred_type and not isinstance(arg, preferred_type):
                    try:
                        arg = preferred_type(arg)
                    except Exception as e:
                        raise TypeError(f"Could not convert argument {i} to preferred type {preferred_type.__name__}: {e}")
                new_args.append(arg)
            return func(*new_args, **kwargs)
        return wrapper
    return decorator


def validate_func_args(*validators):
    """
    A decorator for validating the type and optionally the value of arguments passed to a function.
    Each argument can have its own set of allowed types, a preferred type, and allowed values.

    Parameters:
        *validators (dict): Each dictionary in validators specifies the validation rules for one argument.
                            The keys in the dictionary can be:
                            - 'allowed_types': A tuple of allowed types for the argument.
                            - 'preferred_type': The preferred type to which the argument should be converted if possible.
                            - 'allowed_values': A list of values that the argument is allowed to have.
                            - 'case_sensitive': Specifies whether string comparisons should be case sensitive.

    Returns:
        A decorator function for the function.

    Raises:
        TypeError: If an argument does not match one of the allowed types or cannot be converted to the preferred type.
        ValueError: If the argument is of the correct type but not in the allowed values list.

    Example:
        >>> @validate_func_args(
        ...     {'allowed_types': (str,), 'allowed_values': ["hello", "world"], 'case_sensitive': False},
        ...     {'allowed_types': (int,), 'preferred_type': float}
        ... )
        ... def my_function(word, number):
        ...     print(f"{word} {number}")
        ...
        >>> my_function("HELLO", 123)  # This is valid and prints 'hello 123.0'
        >>> my_function("unknown", 123)  # This raises ValueError for the first argument
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            new_args = []
            for i, (arg, validator) in enumerate(zip(args, validators)):
                allowed_types = validator.get('allowed_types', ())
                preferred_type = validator.get('preferred_type')
                allowed_values = validator.get('allowed_values')
                case_sensitive = validator.get('case_sensitive', True)

                validate_type_decorator = validate_type(allowed_types)
                convert_type_decorator = convert_to_preferred_type(preferred_type)
                validate_value_decorator = validate_value(allowed_values, case_sensitive)

                arg = validate_type_decorator(lambda x: x)(arg)
                arg = convert_type_decorator(lambda x: x)(arg)
                arg = validate_value_decorator(lambda x: x)(arg)

                new_args.append(arg)

            return func(*new_args, **kwargs)

        return wrapper

    return decorator



def validate_value(allowed_values, case_sensitive=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i, (arg, _) in enumerate(zip(args, allowed_values)):
                if allowed_values[i] is not None:
                    if isinstance(arg, str) and not case_sensitive:
                        validation_passed = any(val.lower() == arg.lower() for val in allowed_values[i])
                    else:
                        validation_passed = arg in allowed_values[i]

                    if not validation_passed:
                        allowed_values_str = ', '.join(map(str, allowed_values[i]))
                        raise ValueError(f"Argument {i} must be one of {allowed_values_str}, got {arg}")
            return func(*args, **kwargs)
        return wrapper
    return decorator



class FrozenProperty(RestrictedSetter):

    def __init__(self, name, allowed_types=None, **kwargs):
        """
        Initialize the FrozenProperty object.

        Args:
            name (str): Name of the property.
            allowed_types (type or tuple of types, optional): Allowed types for the property value.

        Raises:
            AttributeError: If the initial value is not of the correct type.
        """
        super().__init__(name, allowed_types=allowed_types, **kwargs)

    def __call__(self, setter):
        def wrapped_setter(instance, value):
            if not instance.__dict__.get(f"_{self.name}_frozen", False):
                if self.allowed_types and not isinstance(value, self.allowed_types):
                    raise AttributeError(
                            f"Value must be of type {self.allowed_types}, not {type(value)}"
                            )
                setter(instance, value)
                instance.__dict__[f"_{self.name}_frozen"] = True
            else:
                raise AttributeError(f"Cannot modify a frozen property: {self.name}")

        return wrapped_setter


def frozen_property(name, allowed_types=None, restrict_setter=True):
    return FrozenProperty(name, allowed_types=allowed_types, restrict_setter=restrict_setter)
