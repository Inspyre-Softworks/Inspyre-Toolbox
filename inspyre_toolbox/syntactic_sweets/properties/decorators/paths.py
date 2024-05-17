from functools import wraps
from pathlib import Path


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


def provision_path(func):
    """
    Provisions a path.

    Returns:
        Path:
            The provisioned path.
    """

    @wraps(func)
    def wrapper(self, new, **kwargs):
        print(kwargs)
        if isinstance(new, str) and not kwargs.get('do_not_convert', False):
            new = Path(new)

        if not isinstance(new, Path):
            raise TypeError(f"Expected Path object, got {type(new).__name__}")

        no_expand = kwargs.get('do_not_expand', False)
        no_resolve = kwargs.get('do_not_resolve', False)

        if not no_expand:
            new = new.expanduser()

        if not no_resolve:
            new = new.resolve()

        func(self, new)

    return wrapper
