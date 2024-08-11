import inspect

from .errors import UnmetConditionError


class RestrictedSetter:
    """
    A descriptor class that restricts the setting of a property based on type, value, and custom conditions.

    This class is designed to be used as a descriptor for class classes, allowing for the definition of restrictions
    on the setting of the property. These restrictions can include type checking, value checking, and custom conditions
    that must be met for the property to be set. If any of the restrictions are violated, an exception is raised.

    The `RestrictedSetter` class also allows for the definition of an initial value for the property, which is used if
    the property has not been set. This can be useful for defining default values for classes.

    Notes:
      - If a `preferred_type` is specified, the value will be converted to that type if possible. If the value cannot be converted to the preferred type, a `TypeError` will be raised.

      - If a custom condition is specified, the condition must be met for the property to be set. If the condition is not met, an `UnmetConditionError` will be raised.

      - If an exception is specified, it will be raised instead of the default `UnmetConditionError` if the custom condition is not met.

      - If `allowed_values` is specified, the value must be in the set of allowed values for the property to be set. If the value is not in the set, a `ValueError` will be raised.

      - If `restrict_setter` is set to `True`, the setter can only be called within class methods. If the setter is called outside of class methods, a `PermissionError` will be raised.
    """

    def __init__(
            self,
            name,
            initial=None,
            allowed_types=None,
            preferred_type=None,
            allowed_values=None,
            condition=None,
            exception=None,
            exception_args=None,
            restrict_setter=True
    ):
        """
        Initialize a new RestrictedSetter instance.

        Parameters:

            name (str):
                The name of the property.

            initial (Any, optional):
                The initial value of the property.

            allowed_types (Union[type, Tuple[type]], optional):
                The type(s) allowed for the property.

            preferred_type (type, optional):
                The preferred type for the property.

            allowed_values (Iterable, optional):
                The set of allowed values for the property.

            condition (Callable, optional):
                A condition that must be met for the property to be set.

            exception (Exception, optional):
                The exception to raise if the condition is not met.

            exception_args (Dict, optional):
                Arguments to pass to the exception.

            restrict_setter (bool, optional):
                Whether to restrict the setter to class methods.


        Example:

                >>> class MyClass:
                ...     _my_property = RestrictedSetter(
                ...         'my_property',
                ...         allowed_types=(int, float),
                ...         preferred_type=int,
                ...         condition=lambda self: self._my_property > 0,
                ...         exception=ValueError,
                ...         exception_args={'message': "Value must be greater than 0."}
                ...     )
                ...
                ...     @property
                ...     def my_property(self):
                ...         return self._my_property
                ...
                ...     @my_property.setter
                ...     def my_property(self, value):
                ...         self._my_property = value
                ...
                >>> obj = MyClass()
                >>> obj.my_property = 10

        Example:
            >>> class MyClass:
            ...     _my_property = RestrictedSetter(
            ...         'my_property',
            ...         allowed_types=(int, float),
            ...         preferred_type=int,
            ...         allowed_values={10, 20, 30},
            ...         condition=lambda self: self._my_property > 0,
            ...         exception=ValueError,
            ...         exception_args={'message': "Value must be greater than 0."}
            ...     )
            ...
            ...     @property
            ...     def my_property(self):
            ...         return self._my_property
            ...
            ...     @my_property.setter
            ...     def my_property(self, value):
            ...         self._my_property = value
            ...
            >>> obj = MyClass()
            >>> obj.my_property = 10  # Valid
            >>> obj.my_property = 5   # Raises an exception if 5 is not in allowed_values
        """

        self.name = f'_{name}'
        self.initial = initial
        self.restrict_setter = restrict_setter

        # Ensure `allowed_types` is a tuple or list
        if not isinstance(allowed_types, (tuple, list)):
            allowed_types = (allowed_types,)

        self.allowed_types = allowed_types if isinstance(allowed_types, (tuple, list)) else (allowed_types,)
        self.preferred_type = preferred_type

        self.allowed_values = (
            allowed_values if isinstance(
                allowed_values, (tuple, list)) else (allowed_values,)
        ) if allowed_values is not None else None

        self.condition = condition
        self.exception = exception
        self.exception_args = exception_args or {}

    def __get__(self, obj, obj_type=None):
        """
        Retrieves the value of the property.

        This method is a getter for the property, returning its current value. If the property has not been set,
        it returns the initial value specified during the creation of the `RestrictedSetter` instance.

        Parameters:

            obj (object):
                The instance of the class whose property is being retrieved.

            obj_type (type, optional):
                The type of the object. This parameter is not used but is part of the descriptor protocol.

        Returns:
            The current value of the property.
        """
        return getattr(obj, self.name, self.initial)

    def __set__(self, obj, value):
        """
        Sets the value of the property, enforcing any restrictions.

        This method acts as a setter for the property, applying the defined restrictions such as type checking,
        value restrictions, and custom conditions. If any restriction is violated, an appropriate exception is raised.

        Parameters:

            obj (object):
                The instance of the class whose property is being set.

            value (Any):
                The new value for the property.

        Raises:
            PermissionError:
                If the setter is called outside-of class methods when `restrict_setter` is True.

            ValueError:
                If the provided value is not in the `allowed_values` set.

            PermissionError:
                If a custom `condition` is not satisfied.

            TypeError:
                If the provided value is not of an allowed type.

            Any exception specified by the `exception` attribute,
                if the custom condition fails.
        """
        if (self.allowed_types and not isinstance(value, self.allowed_types)) and value is not None:
            raise TypeError(
                f"Value must be of type {', '.join([t.__name__ for t in self.allowed_types])}, got type {type(value).__name__}.")

        if self.preferred_type and not isinstance(value, self.preferred_type):
            value = self.preferred_type(value)

        if self.restrict_setter:
            caller_frame = inspect.stack()[1]
            caller_self = caller_frame.frame.f_locals.get('self', None)
            if caller_self is None or caller_self.__class__ != obj.__class__:
                raise PermissionError("Property can only be set within class methods.")

        if self.allowed_values is not None and value not in self.allowed_values:
            allowed_vals = ', '.join(map(str, self.allowed_values))
            raise ValueError(f"Value must be one of {allowed_vals}, got {value}")

        if self.condition and not self.condition(obj):
            if self.exception:
                raise self.exception(**self.exception_args)
            raise UnmetConditionError("Condition for setting property not met.")

        setattr(obj, self.name, value)

    def __delete__(self, obj):
        """
        Resets the property to its initial value.

        This method allows for the property to be reset or deleted, setting it back to the initial value specified
        during the creation of the `RestrictedSetter` instance. This can be useful for resetting the state of an
        instance property to its default.

        Parameters:

            obj (object):
                The instance of the class whose property is being reset.
        """
        setattr(obj, self.name, self.initial)
