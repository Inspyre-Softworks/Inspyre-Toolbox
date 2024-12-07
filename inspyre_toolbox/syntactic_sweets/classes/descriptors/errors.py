"""
Contains the custom errors for the descriptors module.
"""


class UnmetConditionError(PermissionError):
    """
    An error raised when a condition is not met.
    """

    def __init__(self, message):
        """
        Initialize a new UnmetConditionError instance.

        Parameters:

            message (str):
                The error message.
        """
        super().__init__(message)
