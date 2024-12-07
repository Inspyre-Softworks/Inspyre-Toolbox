from inspyre_toolbox.common.errors import InspyreToolboxError


class PyPiError(InspyreToolboxError):
    """
    Base class for PyPi errors.
    """
    default_message = 'An unknown error has occurred while interacting with PyPi.'

    def __init__(self, **kwargs):
        msg = kwargs.pop('message', self.default_message)
        super().__init__(message=msg, **kwargs)


class PyPiPackageNotFoundError(PyPiError):
    """
    Raised when a package is not found on PyPi.
    """
    default_message = 'The package was not found on PyPi.'

    def __init__(self, **kwargs):
        message = kwargs.pop('message', self.default_message)
        super().__init__(message=message, **kwargs)
