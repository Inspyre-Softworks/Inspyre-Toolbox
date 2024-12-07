from functools import wraps
from pathlib import Path

from .type_validation import validate_type


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
                path = Path(path)
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
