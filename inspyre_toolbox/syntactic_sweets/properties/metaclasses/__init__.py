class FreezePropertyError(Exception):
    """Exception raised when attempting to modify a frozen property."""
    pass


class FrozenProperty:

    def __init__(self, name, default=None):
        self.name = f"_{name}"
        self.default = default
        self.getter = None
        self.setter = None

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = getattr(instance, self.name, self.default)
        if self.getter:
            return self.getter(instance)
        return value

    def __set__(self, instance, value):
        if getattr(instance, self.name, self.default) != self.default:
            raise FreezePropertyError(f"Cannot modify frozen property '{self.name[1:]}'")
        if self.setter:
            value = self.setter(instance, value)
        setattr(instance, self.name, value)

    def set_getter(self, func):
        self.getter = func
        return self

    def set_setter(self, func):
        self.setter = func
        return self


class FreezePropertyMeta(type):

    def __new__(mcs, name, bases, dct):
        cls = super().__new__(mcs, name, bases, dct)
        cls._frozen_properties = {}
        for key, value in dct.items():
            if isinstance(value, FrozenProperty):
                cls._frozen_properties[key] = value
        return cls

    def __setattr__(cls, key, value):
        if key in cls.__dict__.get('_frozen_properties', {}):
            raise FreezePropertyError(f"Cannot modify frozen property '{key}' at class level")
        super().__setattr__(key, value)
