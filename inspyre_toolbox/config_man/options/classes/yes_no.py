from typing import Dict, Optional

from inspyre_toolbox.config_man.options import Option


class YesNoOption(Option):

    def __init__(self, name: str, description: str, value: Optional[bool] = None, frozen: bool = False):
        super().__init__(name, description, value)
        self.frozen = frozen

    def set_value(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError("YesNoOption requires a boolean value.")
        if self.frozen:
            raise ValueError(f"Option '{self.name}' is frozen and cannot be modified.")
        old_value = self.value
        self.value = value
        self.log_change(old_value, value)

    def freeze(self):
        self.frozen = True

    def unfreeze(self):
        self.frozen = False

    def to_dict(self) -> Dict:
        return {
                'type':        'YesNoOption',
                'name':        self.name,
                'description': self.description,
                'value':       self.value,
                'frozen':      self.frozen
                }

    @staticmethod
    def from_dict(data: Dict):
        return YesNoOption(
                name=data['name'],
                description=data['description'],
                value=data['value'],
                frozen=data['frozen']
                )
