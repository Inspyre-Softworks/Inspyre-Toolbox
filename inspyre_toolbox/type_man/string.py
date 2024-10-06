"""
Author: 
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File: 
    inspyre_toolbox/type_man/string.py

Description:
    A custom string class that supports case-insensitive comparisons.
"""


class String(str):
    """
    A custom string class that supports case-insensitive comparisons.

    Parameters:
        value (str):
            The string value.

        compare_sensitively (bool, optional):
            If True, comparisons will be case-sensitive. Default is False.
    """
    def __new__(cls, value, *args, compare_sensitively=False, **kwargs):
        instance = super().__new__(cls, value)
        instance._compare_sensitively = compare_sensitively
        return instance

    @property
    def compare_sensitively(self):
        """
        Get the case sensitivity of the string.

        Returns:
            bool:
                True if the string is case-sensitive, False otherwise.
        """
        return self._compare_sensitively

    @compare_sensitively.setter
    def compare_sensitively(self, new):
        """
        Set the case sensitivity of the string.

        Parameters:
            new (bool):
                True if the string should be case-sensitive, False otherwise.:

        Returns:
            None
        """
        self._compare_sensitively = new

    def __eq__(self, other):
        me = str(self)
        if hasattr(other, 'compare_sensitively'):
            other = str(other)
        if not self.compare_sensitively:
            if hasattr(other, 'compare_sensitively'):
                other = str(other)
            me = me.lower()
            other = other.lower()
        return me == other
