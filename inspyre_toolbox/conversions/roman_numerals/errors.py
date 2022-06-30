"""

Contains errors for inspyre_toolbox.conversions.roman_numerals

"""


class InvalidRomanNumeralStringError(Exception):
    """
    .. _rn_constant:

    """
    message = "An invalid Roman numeral string was passed to the 'provided' parameter."

    def __init__(self, provided, message=message, skip_print=True):
        """

        Raised when a string is passed to 'RomanNumerals' that does not match one of the Roman numeral characters (or
        pair)

        Parameters:
            provided (str):
                The string provided to the 'RomanNumeral' class that's invalid.

            message (str):
                Any additional information the caller might want to be made clear in the exception being raised to the
                end-user. (Optional)

            skip_print (bool):
                Should the exception print it's 'message' contents. (Optional)

        """

        self.message = self.message

        if message:
            self.message += f"\nSome additional information from caller: {message}"

        if not skip_print:
            print(self.message)
