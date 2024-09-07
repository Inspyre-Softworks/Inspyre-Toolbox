import json
from typing import Dict, Union

from inspyre_toolbox.config_man.options.shortcuts import Option, StringInputOption, YesNoOption


class OptionManager:
    """
    Manages various options, acting like a dictionary with type enforcement.
    Tracks changes through the OptionLedger.
    """

    def __init__(self):
        self._options = {}

    @property
    def options(self):
        return self._options

    def add_option(self, option: Option):
        """Add an option to the manager."""
        if option.name in self._options:
            raise ValueError(f"Option '{option.name}' already exists.")
        self._options[option.name] = option

    def set_option_value(self, name: str, value: Union[bool, str]):
        """Set the value of an option by name."""
        option = self._options.get(name)
        if option:
            option.set_value(value)
        else:
            raise KeyError(f"Option '{name}' not found.")

    def __getitem__(self, key: str) -> Union[bool, str]:
        """Allow dictionary-style access to get option values."""
        return self._options[key].value

    def __setitem__(self, key: str, value: Union[bool, str]):
        """Allow dictionary-style access to set option values."""
        self.set_option_value(key, value)

    def __contains__(self, key: str) -> bool:
        """Check if an option exists by key."""
        return key in self._options

    def __repr__(self):
        """Return a string representation of all options."""
        return "\n".join([f"{name}: {option}" for name, option in self._options.items()])

    def save_to_dict(self) -> Dict[str, Dict]:
        """Convert all options to a dictionary that can be serialized."""
        return {name: option.to_dict() for name, option in self._options.items()}

    def load_from_dict(self, data: Dict[str, Dict]):
        """Load options from a dictionary."""
        for name, option_data in data.items():
            option_type = option_data.pop('type')
            if option_type == 'YesNoOption':
                self._options[name] = YesNoOption.from_dict(option_data)
            elif option_type == 'StringInputOption':
                self._options[name] = StringInputOption.from_dict(option_data)

    def save_to_file(self, filename: str):
        """Save all options to a file."""
        with open(filename, 'w') as file:
            json.dump(self.save_to_dict(), file, indent=4)

    def load_from_file(self, filename: str):
        """Load options from a file."""
        with open(filename, 'r') as file:
            data = json.load(file)
            self.load_from_dict(data)

    def get_ledger_entries(self):
        """Get the ledger entries for all tracked changes."""
        if Option.ledger is None:
            return "No changes have been recorded."
        return Option.ledger
