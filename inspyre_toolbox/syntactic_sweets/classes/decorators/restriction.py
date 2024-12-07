"""
This module contains decorators for restricting the change of classes.

Functions:

    restricted_to_internal_use:
        A decorator for restricting the use of a method to internal use only. This decorator raises a PermissionError if
        the function is called from outside the class, with an optional suggestion for an alternative method to use.

    restrict_change_to_default:
        A decorator for restricting the change of a property to only when it is set to the default value. This is kinda
        like a read-only property, but it allows changes only when the property is set to a specific value.
"""
import inspect
from functools import wraps


def restricted_to_internal_use(alternative_method=None):
    """
    A decorator for restricting the use of a method to internal use only.

    Parameters:
        alternative_method (str, optional):
            The name of an alternate method to suggest if the restricted method is called from outside the class.

    Returns:
        A wrapper function that raises a PermissionError if the function is called from outside the class.

    Raises:
        PermissionError:
            If the function is called from outside the class, a PermissionError is raised with an optional suggestion for an alternative method.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get the current frame and the caller's frame
            current_frame = inspect.currentframe()
            caller_frame = current_frame.f_back

            # Get the caller's class
            caller_class = caller_frame.f_locals.get('self', None).__class__

            # Check if the caller's class is the same as the class of the instance
            if caller_class is not self.__class__:
                suggestion = ""
                if alternative_method and hasattr(self, alternative_method):
                    suggestion = f" You may want to use the '{alternative_method}' method instead."
                raise PermissionError(f"The method {func.__name__} is restricted to internal use only.{suggestion}")

            return func(self, *args, **kwargs)

        return wrapper

    return decorator


def restrict_change_to_default(default_value, allowed_types=None, allowed_values=None, change_error=None,
                               type_error=None, value_error=None, allow_deletion=False):
    """
    A decorator for restricting the change of a property to only when it is set to the default value and
    optionally checking for allowed types and allowed values. Optionally allows deletion of the property
    which resets it to the default value.

    Parameters:
        default_value (Any):
            The default value to which the property should be set in order to allow changes.
        allowed_types (tuple, optional):
            A tuple of allowed types for the property value.
        allowed_values (iterable, optional):
            An iterable of allowed values for the property.
        change_error (Exception, optional):
            The exception to raise if the property is not set to the default value.
        type_error (Exception, optional):
            The exception to raise if the property value is not of an allowed type.
        value_error (Exception, optional):
            The exception to raise if the property value is not an allowed value.
        allow_deletion (bool, optional):
            If True, allows deletion of the property which resets it to the default value.

    Returns:
        A decorator function for the property setter and deleter.

    Raises:
        change_error:
            If the property is not set to the default value, the specified error or AttributeError is raised.
        type_error:
            If the property value is not of an allowed type, the specified error or TypeError is raised.
        value_error:
            If the property value is not an allowed value, the specified error or ValueError is raised.
    """

    def decorator(setter):
        property_name = setter.__name__

        def wrapper(instance, value):
            if getattr(instance, property_name, default_value) != default_value:
                raise (change_error or AttributeError)(
                        f"This property cannot be changed unless it is set to the default value: {default_value}."
                        )

            if allowed_types is not None and not isinstance(value, allowed_types):
                raise (type_error or TypeError)(
                        f"The property value must be of type(s) {allowed_types}, but got type {type(value)}."
                        )

            if allowed_values is not None and value not in allowed_values:
                raise (value_error or ValueError)(
                        f"The property value must be one of {allowed_values}, but got {value}."
                        )

            setter(instance, value)

        def deleter(instance):
            setattr(instance, property_name, default_value)

        return property(fget=lambda instance: getattr(instance, property_name, default_value),
                        fset=wrapper,
                        fdel=deleter if allow_deletion else None)

    return decorator
