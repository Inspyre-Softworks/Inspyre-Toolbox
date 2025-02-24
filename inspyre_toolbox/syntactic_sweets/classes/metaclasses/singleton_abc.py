from abc import ABCMeta


class SingletonABCMeta(ABCMeta):
    """
    Metaclass for creating singletons with abstract base classes.

    This metaclass is used to create singletons from abstract base classes. The singleton pattern is implemented by
    overriding the `__call__` method of the class. This metaclass is used to enforce the singleton pattern on abstract
    base classes, ensuring that only one instance of each concrete subclass is created.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Override the `__call__` method to enforce the singleton pattern.

        This method overrides the `__call__` method of the class to enforce the singleton pattern. If an instance of the
        class has already been created, the existing instance is returned. Otherwise, a new instance is created and
        returned.

        Arguments:
            *args:
                Positional arguments to be passed to the class constructor.
            **kwargs:
                Keyword arguments to be passed to the class constructor.

        Returns:
            SingletonABCMeta:
                The singleton instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)

        return cls._instances[cls]
