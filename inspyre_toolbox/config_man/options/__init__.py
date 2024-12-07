from abc import ABC, abstractmethod
from typing import Dict, Optional

from inspyre_toolbox.config_man.options.ledger import OptionLedger, OptionLedgerEntry


# Base Option Class
class Option(ABC):
    """
    Base class for all options.
    """
    ledger = None  # This will be initialized when the first option is added

    def __init__(self, name: str, description: str, value: Optional[object] = None):
        self.name = name
        self.description = description
        self.value = value

    @abstractmethod
    def set_value(self, value):
        """Set the value of the option, enforcing type checking."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict:
        """Convert the option to a dictionary."""
        pass

    @staticmethod
    @abstractmethod
    def from_dict(data: Dict):
        """Create an Option object from a dictionary."""
        pass

    def help(self):
        return self.description

    def log_change(self, old_value, new_value):
        """Log the change in the option's value to the ledger."""
        if Option.ledger is None:
            Option.ledger = OptionLedger()  # Create the ledger when the first option change is made
        entry = OptionLedgerEntry(self.name, old_value, new_value)
        Option.ledger.add_entry(entry)
