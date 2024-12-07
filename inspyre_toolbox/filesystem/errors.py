class NeedsProcessingError(Exception):
    """
    Raised when an operation is attempted on a file collection that hasn't yet been processed.

    Attributes:
        message (str):
            The error message.

    Note:
        This exception can usually be resolved by calling the `process_files` method on the file-collection object
        before attempting the operation.
    """

    def __init__(self, message: str = 'The file collection has not yet been processed!'):
        self.message = message
        super().__init__(self.message)
