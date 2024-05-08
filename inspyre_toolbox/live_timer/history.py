from os import makedirs
from pathlib import Path
from time import time


class TimerHistory(object):

    def __init__(self, elapsed_method):
        self.get_elapsed = elapsed_method
        self.ledger = []
        self.actions = [
                "START",
                "STOP",
                "PAUSE",
                "UNPAUSE",
                "RESET",
                "CREATE",
                "QUERY"
        ]
        self.add("CREATE")

    @property
    def num_resets(self) -> int:
        """
        Get the number of times the timer has been reset

        Returns:
            The number of times the timer has been reset

        """
        return len([entry for entry in self.ledger if entry['action'] == "RESET"])

    def add(self, action: str = "START") -> dict:
        """
        The add function adds a new entry to the ledger.

        Args:
            self:
                Refer to the object instance
            action (str):
                The action you'd like to log to the ledger. (Optional; defaults to 'START')

        Returns:
            The entry that was just added to the ledger

        """
        action = action.upper()
        entry = {
                "time":               time(),
                "elapsed_since_last": "",
                "action":             action,
                "rt_at_create":       ""
        }
        if action == "CREATE":
            entry['elapsed_since_last'] = 0.00
        else:
            entry['elapsed_since_last'] = self.get_elapsed(self.ledger[-1]['time'])
            entry['rt_at_create'] = self.get_elapsed(self.ledger[0]['time'])

        self.ledger.append(entry)

        return entry

    def write(self):
        """
        The write function writes the ledger to a file.

        Args:
            self:
                Refer to the object itself

        Returns:
            None
        """
        data_path = Path("~/Inspyre-Softworks/Inspyre-Toolbox/data").expanduser()

        filename = f'ledger_{str(time()).split(".")[0]}'
        filepath = str(f'{str(data_path)}/{filename}.txt')

        filepath = str(Path(filepath).resolve())

        if not data_path.exists():
            makedirs(data_path)

        with open(filepath, "w") as fp:
            fp.write(str(self.ledger))

    def reset(self) -> None:
        """
        Clear the ledger

        This literally just runs '.clear()' on 'self.ledger'

        Returns:
            None

        """
        self.ledger.clear()
