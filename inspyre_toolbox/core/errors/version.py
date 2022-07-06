class InvalidPreReleaseTypeError(Exception):

    message = "The pre-release type found in the VERSION file is not valid."

    def __init__(self, message=None, pr_type=None, skip_print=False):
        """
        The __init__ function is the constructor for a class. It is called whenever
        an instance of a class is created.

        The __init__ function can take arguments, but those arguments are only
        stored as attributes on the instance.

        Arguments:
            message (:class:`str`):
                Provide a custom message for the exception. (Optional, defaults to
                ``None``)

            pr_type (:class:`str`):
                The pre-release type found in the VERSION file. (Optional, defaults
                to ``None``)

            skip_print (:class:`bool`)
                Prevent the printing of an error message when the exception is
                raised in a try/except block. (Optional, defaults to ``False``).
        """
        if pr_type:
            self.message = f'The provided pre-release type "{pr_type}" is not valid.'
        if message:
            self.message += f"Addditional information from the caller: {message}"

        if not skip_print:
            print(self.message)




class VersionInfoMismatchError(Exception):
    message = 'The version number does not match the concatenation of the ' \
              'minor, major, and patch numbers.'

    def __init__(
            self,
            version_number: str,
            concatenated: str,
            message=None,
            skip_print=False,
            *args, **kwargs):
        """
        The :class:`VersionInfoMismatchError` class is used to raise an error if the
        version number does not match the concatenation of the minor, major,
        and patch numbers.

        Arguments:
            version_number:
                The version number of the current version of
                                       inspyre_toolbox

        Args:
            self:
            version_number:
            concatenated:
            message:
            skip_print:
            *args:
            **kwargs:

        Returns:

        """
        mismatch_statement = f"Ver. Number: {version_number} | " \
                             f"Concatenated: {concatenated}"
        from_caller = f"Additional information from caller: {message}" if message else ""
        self.message = \
            message or f"{self.message}\n{mismatch_statement}\n{from_caller}"
        super().__init__(self.message, *args, **kwargs)
