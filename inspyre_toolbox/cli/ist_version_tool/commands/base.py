from abc import ABC, abstractmethod

from inspyre_toolbox.cli.ist_version_tool.commands.registrar import CommandRegistrar
from inspyre_toolbox.syntactic_sweets.classes.metaclasses.singleton_abc import SingletonABCMeta


class Command(ABC, metaclass=SingletonABCMeta):
    """
    Abstract base class for commands.

    This class defines the interface for all command classes. Each command class should inherit from this class and
    implement the `inject` method.
    """

    REGISTRAR = CommandRegistrar()

    @property
    @abstractmethod
    def command_parser(self):
        """
        Abstract property to be implemented by subclasses for command parser access. MUST BE IMPLEMENTED BY SUBCLASSES.
        """
        pass

    @property
    def registered(self):
        return self.REGISTRAR.check_registered(self)

    def __init_subclass__(cls, **kwargs):
        """
        Automatically register subclasses with the registrar.

        Parameters:
            **kwargs:
                Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init_subclass__(**kwargs)

        cls.register()

    @classmethod
    def register(cls):
        cls.REGISTRAR.register_command(cls)

    @abstractmethod
    def inject(self):
        """
        Abstract method to be implemented by subclasses for injection logic.

        Returns:
            None
        """
        pass
