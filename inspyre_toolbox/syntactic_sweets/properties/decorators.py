from functools import wraps
from pathlib import Path


def validate_type(*allowed_types, preferred_type=None, allowed_values=None, case_sensitive=True):
    """
    A decorator for validating the type and optionally the value of a value passed to a class
    property setter, with an option to convert to a preferred type if specified and to enforce
    value restrictions.

    Parameters:
        preferred_type (type, optional): The preferred type to which values should be converted
                                          if possible. If None, no conversion is attempted.
        *allowed_types: Variable length list of allowed types for the property value.
        allowed_values (iterable, optional): An iterable of values that are allowed. If None,
                                             all values of the correct type are allowed.
        case_sensitive (bool, optional): Specifies whether string comparisons should be case
                                         sensitive. Defaults to True. Ignored for non-string types.

    Returns:
        A decorator function for the property setter.

    Raises:
        TypeError: If the incoming value does not match one of the allowed types, cannot be
                   converted to the preferred type, or is not in the list of allowed values.
        ValueError: If the value is of the correct type but not in the allowed values list.

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


def validate_path(exists=False, create=False, callback=None, do_not_resolve=False, do_not_expanduser=False):
    """
    A decorator for validating a path.

    Parameters:
        exists (bool, optional):
            If True, ensures that the path exists.

        create (bool, optional):
            If True and the path does not exist, creates the path.

        callback (callable, optional):
            A callback function to call if the path does not exist. Ignored if 'create' is True.

        do_not_resolve (bool, optional):
               If True, does not resolve the path.

        do_not_expanduser (bool, optional):
                If True, does not expand the user in the path.

    Returns:
        A decorator function for the property setter.

    Raises:
        ValueError: If 'exists' is True and the path does not exist.
        FileNotFoundError: If 'exists' is True and 'create' is False, and the path does not exist.
        TypeError: If the value is not a Path object.

    Example:
        >>> class MyClass:
        ...     @property
        ...     def my_path(self):
        ...         return self._my_path
        ...
        ...     @my_path.setter
        ...     @validate_path(exists=True)
        ...     def my_path(self, path):
        ...         self._my_path = path
        ...
        >>> obj = MyClass()
        >>> obj.my_path = Path("/path/to/existing/folder")  # This is accepted and set
        >>> obj.my_path = "/nonexistent/folder"  # This raises TypeError
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, path):
            prop_name = f'{self.__class__.__name__}.{func.__name__}'
            if isinstance(path, str):
                path = Path()
            if not isinstance(path, Path):
                raise TypeError(f"`{prop_name}` must be a `pathlib.Path` or `string` object!")

            if not do_not_expanduser:
                path = path.expanduser()

            if not do_not_resolve:
                path = path.resolve()

            path_exists = path.exists()
            if exists and not path_exists:
                raise ValueError(f"{prop_name} must be an existing path, got {path}")

            if not path_exists and create:
                path.mkdir(parents=True, exist_ok=True)

            if not path_exists and callback and not create:
                callback(path)

            return func(self, path)

        return wrapper

    return decorator
