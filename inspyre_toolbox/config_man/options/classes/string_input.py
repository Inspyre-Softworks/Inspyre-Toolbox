"""
A module containing the StringInputOption class.

Classes:
    StringInputOption:
        A class to represent a string input option with a description.

Since:
    1.6.0
"""
from typing import Dict

from inspyre_toolbox.config_man.options import Option


class StringInputOption(Option):
    """
    A class to represent a string input option with a description.

    Attributes:
    -----------
    name (str):
        The name of the option.

    description (str):
        A description of what the option does.

    value (str):
        The current value of the option.

    """

    def set_value(self, value: str):
        """
        Set the value of the option, enforcing type checking.

        Arguments:
            value (str):
                The new value for the option.

        Returns:
            None

        Raises:
            TypeError:
                If the value is not a string.
        """
        if not isinstance(value, str):
            raise TypeError("StringInputOption requires a string value.")
        old_value = self.value
        self.value = value
        self.log_change(old_value, value)

    def to_dict(self) -> Dict:
        """
        Convert the StringInputOption to a dictionary.

        Returns:
            Dict:
                A dictionary representation of the StringInputOption. This dictionary can be used to recreate the
                option, and should contain the following keys:
                    - 'type': The type of the option ('StringInputOption').
                    - 'name': The name of the option.
                    - 'description': A description of what the option does.
                    - 'value': The current value of the option.

        """
        return {
                'type':        'StringInputOption',
                'name':        self.name,
                'description': self.description,
                'value':       self.value
                }

    @staticmethod
    def from_dict(data: Dict):
        """
        Create a StringInputOption from a dictionary. The dictionary should contain the following
        keys:
            - 'name': The name of the option.
            - 'description': A description of what the option does.
            - 'value': The current value of the option.

        Arguments:
            data (Dict):
                A dictionary containing the data needed to create the StringInputOption object. This dictionary should
                contain the keys listed above.

        Returns:
            StringInputOption:
                A new StringInputOption object created from the data in the dictionary.
        """
        return StringInputOption(
                name=data['name'],
                description=data['description'],
                value=data['value']
                )
