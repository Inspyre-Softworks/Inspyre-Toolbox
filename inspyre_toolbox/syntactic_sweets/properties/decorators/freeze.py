class FreezeProperty:

    def __init__(self, fset):
        self.fset = fset
        self.is_set = False

    def __call__(self, instance, value):
        if not self.is_set:
            self.fset(instance, value)
            self.is_set = True
        else:
            raise AttributeError(f"{instance.__class__.__name__}.{self.fset.__name__} is frozen and cannot be "
                                 f"modified.")

    def __get__(self, instance, owner):
        return instance.__dict__[self.fset.__name__]

    def __set__(self, instance, value):
        if not self.is_set:
            self.fset(instance, value)
            self.is_set = True
        else:
            raise AttributeError(f"Property {self.fset.__name__} is frozen and cannot be modified.")


def freeze_property(fset):
    return FreezeProperty(fset)
