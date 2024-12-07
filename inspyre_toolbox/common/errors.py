from inspyre_toolbox.exceptional import CustomRootException


class InspyreToolboxError(CustomRootException):
    """
    Base class for all Inspyre Toolbox errors.
    """
    default_message = 'An unknown error has occurred within the Inspyre Toolbox package.'

    def __init__(self, **kwargs):
        message = kwargs.pop('message', self.default_message)
        super().__init__(message, **kwargs)


class InvalidParameterCombinationError(InspyreToolboxError, ValueError):
    """
    Error raised when an invalid combination of parameters is provided.
    """
    default_message = 'An invalid combination of parameters was provided.'

    def __init__(self, **kwargs):
        message = kwargs.pop('message', self.default_message)
        InspyreToolboxError.__init__(self, message=message, **kwargs)


class MissingRequiredParameterError(InspyreToolboxError, ValueError):
    """
    Error raised when a required parameter is missing.
    """
    default_message = 'A required parameter is missing.'

    def __init__(self, **kwargs):
        message = kwargs.pop('message', self.default_message)
        InspyreToolboxError.__init__(self, message=message, **kwargs)
