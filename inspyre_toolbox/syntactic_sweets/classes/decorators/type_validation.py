from functools import wraps
from pathlib import Path
from typing import Union

def validate_type(*allowed_types, preferred_type=None, allowed_values=None, case_sensitive=True, conversion_funcs=None):
    """
    A decorator for validating the type and optionally the value of a value passed to a class
    property setter, with an option to convert to a preferred type if specified and to enforce
    value restrictions.

    Parameters:
        *allowed_types:
            Variable length list of allowed types for the property value.

        preferred_type (type, optional):
            The preferred type to which values should be converted if possible. (If None, no conversion is attempted)

        allowed_values (iterable, optional):
            An iterable of values that are allowed. If None, all values of the correct type are allowed.

        case_sensitive (bool, optional):
            Specifies whether string comparisons should be case-sensitive. Defaults to True. Ignored for non-string
            types.

        conversion_funcs (dict, optional):
            A dictionary mapping types to conversion functions. These functions should convert from the
            specified type to the preferred type.

    Returns:
        A decorator function for the property setter.

    Raises:
        TypeError:
            If the incoming value does not match one of the allowed types, cannot be converted to the preferred type,
            or is not in the list of allowed values.

        ValueError:
            If the value is of the correct type but not in the allowed values list.

    Example:
        >>> class MyClass:
        ...     @property
        ...     def my_property(self):
        ...         return self._my_property
        ...
        ...     @my_property.setter
        ...     @validate_type(str, allowed_values=["hello", "world"], case_sensitive=False)
        ...     def my_property(self, value):
        ...         self._my_property = value
        ...
        >>> obj = MyClass()
        >>> obj.my_property = "HELLO"  # This is accepted and set
        >>> obj.my_property = "hello"  # This is also accepted and set
        >>> obj.my_property = "Hi"  # This raises ValueError
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, tuple(allowed_types)):
                allowed = ', '.join([t.__name__ for t in allowed_types])
                raise TypeError(f"Value must be of type {allowed}, got type {type(value).__name__}")

            if preferred_type and not isinstance(value, preferred_type):
                if conversion_funcs and type(value) in conversion_funcs:
                    try:
                        value = conversion_funcs[type(value)](value)
                    except Exception as e:
                        raise TypeError(f"Conversion failed: {e}")
                else:
                    try:
                        value = preferred_type(value)
                    except Exception as e:
                        raise TypeError(f"Could not convert value to preferred type {preferred_type.__name__}: {e}")

            if allowed_values is not None:
                if isinstance(value, str) and not case_sensitive:
                    validation_passed = any(val.lower() == value.lower() for val in allowed_values)
                else:
                    validation_passed = value in allowed_values

                if not validation_passed:
                    allowed_vals = ', '.join(map(str, allowed_values))
                    raise ValueError(f"Value must be one of {allowed_vals}, got {value}")

            return func(self, value)

        return wrapper

    return decorator