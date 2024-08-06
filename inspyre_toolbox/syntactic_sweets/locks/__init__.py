from contextlib import contextmanager


@contextmanager
def flag_lock(instance, flag_name):
    """
    Context manager to set and unset a private flag attribute in an instance.

    This context manager ensures that a specified private flag attribute
    in the given instance is set to True when entering the context and
    reset to False upon exiting the context. This is useful for indicating
    that an operation is in progress within a specific scope.

    Parameters:
        instance (object):
            The instance containing the private flag attribute.

        flag_name (str):
            The name of the flag attribute (without leading underscore).

    Raises:
        AttributeError:
            If the instance does not have the specified private flag attribute.

    Example usage:
        handler = OperationHandler()
        with flag_lock(handler, 'flag'):
            # Perform some operation
            pass

    This will automatically set handler._flag to True within the context
    and reset it to False when exiting the context.
    """
    private_flag_name = f"_{flag_name}"
    if not hasattr(instance, private_flag_name):
        raise AttributeError(f"{instance} has no attribute '{private_flag_name}'")

    setattr(instance, private_flag_name, True)
    try:
        yield
    finally:
        setattr(instance, private_flag_name, False)
