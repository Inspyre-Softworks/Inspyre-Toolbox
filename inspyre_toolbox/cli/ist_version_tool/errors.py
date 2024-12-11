from inspyre_toolbox.common.errors import InspyreToolboxError


class ISTVersionToolError(InspyreToolboxError):
    """
    Base class for all errors in the ist-version-tool program.
    """
    pass


class NonExistentCommandError(InspyreToolboxError):
    """
    Raised when an invalid command is provided to the IST-Version-Tool program.
    """
    default_message = ' is not a valid command!'

    def __init__(self, command, additional_message=None, **kwargs):
        message = f'{command}{self.default_message}'
        self.__additional_message = None
        super().__init__(message=message, **kwargs)

        if additional_message:
            self.additional_message = additional_message

    @property
    def additional_message(self):
        return self.__additional_message

    @additional_message.setter
    def additional_message(self, new):
        if not isinstance(new, str):
            raise ValueError('additional_message must be a string.')
        self.__additional_message = new.strip()
