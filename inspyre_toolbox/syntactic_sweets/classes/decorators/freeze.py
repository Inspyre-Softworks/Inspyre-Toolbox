class FreezeProperty:
    """
    A descriptor that provides a property which can only be set once.

    Attributes:
        fset (function): The setter function for the property.
        is_set (bool): A flag to indicate if the property has been set.
    """

    def __init__(self, fset):
        """
        Initialize the FreezeProperty.

        Args:
            fset (function): The setter function for the property.
        """
        self.fset = fset
        self.is_set = False

    def __call__(self, instance, value):
        """
        Set the value of the property. Can only be done once.

        Args:
            instance (object): The instance to which the property belongs.
            value: The value to set for the property.

        Raises:
            AttributeError: If the property has already been set.
        """
        if self.is_set:
            raise AttributeError(
                f"{instance.__class__.__name__}.{self.fset.__name__} is frozen and cannot be modified.")
        self.fset(instance, value)
        self.is_set = True

    def __get__(self, instance, owner):
        """
        Get the value of the property.

        Args:
            instance (object): The instance to which the property belongs.
            owner (type): The class to which the property belongs.

        Returns:
            The value of the property.
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.fset.__name__, None)

    def __set__(self, instance, value):
        """
        Set the value of the property. Can only be done once.

        Args:
            instance (object): The instance to which the property belongs.
            value: The value to set for the property.

        Raises:
            AttributeError: If the property has already been set.
        """
        if self.is_set:
            raise AttributeError(f"Property {self.fset.__name__} is frozen and cannot be modified.")
        self.__call__(instance, value)


def freeze_property(fset):
    """
    Create a FreezeProperty instance.

    Args:
        fset (function): The setter function for the property.

    Returns:
        FreezeProperty: A new FreezeProperty instance.
    """
    return FreezeProperty(fset)
