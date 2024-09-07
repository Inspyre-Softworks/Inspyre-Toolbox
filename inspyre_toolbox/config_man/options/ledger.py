from datetime import datetime
from typing import Optional

from inspyre_toolbox.syntactic_sweets.classes.decorators.freeze import freeze_property
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type


class OptionLedgerEntry:
    """
    A class to represent a ledger entry for tracking changes in option values.

    Attributes:
    -----------
    option_name (str):
        The name of the option being changed. Required, cannot be None.

    old_value (Optional[Any]):
        The old value of the option before the change. Can be None.

    new_value (Optional[Any]):
        The new value of the option after the change. Cannot be None.

    timestamp (datetime):
        The time when the change occurred.
    """

    def __init__(self, option_name: str, old_value: Optional[object], new_value: Optional[object]):
        self.__initialized = False
        self.__option_name = None
        self.__old_value = None
        self.__new_value = None
        self.__timestamp = None

        self.option_name = option_name
        self.old_value = old_value
        self.new_value = new_value

        self.__timestamp = datetime.now()
        self.__initialized = True

    @property
    def initialized(self):
        return self.__initialized

    @property
    def new_value(self):
        return self.__new_value

    @new_value.setter
    @validate_type(object)
    def new_value(self, new_value):
        if self.initialized:
            raise AttributeError("Cannot modify 'new_value' after the entry has been initialized.")

        self.__new_value = new_value

    @property
    def old_value(self):
        return self.__old_value

    @old_value.setter
    @validate_type(object)
    def old_value(self, old_value):
        if self.initialized:
            raise AttributeError("Cannot modify 'old_value' after the entry has been initialized.")
        self.__old_value = old_value

    @property
    def option_name(self):
        return self.__option_name

    @option_name.setter
    @validate_type(str)
    @freeze_property
    def option_name(self, option_name):
        if self.initialized:
            raise AttributeError("Cannot modify 'option_name' after the entry has been initialized.")

        self.__option_name = option_name

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return (f"Option '{self.option_name}' changed from '{self.old_value}' "
                f"to '{self.new_value}' at {self.timestamp}")


class OptionLedger:
    """
    A class to track changes to option values.

    Attributes:
    -----------
    entries : List[OptionLedgerEntry]
        A list of all changes to option values.
    """

    def __init__(self):
        self.entries = []

    def add_entry(self, entry: OptionLedgerEntry):
        """Add a new entry to the ledger."""
        self.entries.append(entry)

    def get_entries(self):
        """Return all ledger entries."""
        return self.entries

    def __repr__(self):
        return "\n".join([str(entry) for entry in self.entries])
