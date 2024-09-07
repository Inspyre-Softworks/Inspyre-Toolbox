from inspyre_toolbox.exceptional import CustomRootException


class InspyreToolboxError(CustomRootException):
    """
    Base class for all Inspyre Toolbox errors.
    """
    default_message = 'An unknown error has occurred within the Inspyre Toolbox package.'

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)


class InvalidParameterCombinationError(InspyreToolboxError, ValueError):
    """
    Error raised when an invalid combination of parameters is provided.
    """
    default_message = 'An invalid combination of parameters was provided.'

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)


class MissingRequiredParameterError(InspyreToolboxError, ValueError):
    """
    Error raised when a required parameter is missing.
    """
    default_message = 'A required parameter is missing.'

    def __init__(self, message: str = None):
        super().__init__(message or self.default_message)
