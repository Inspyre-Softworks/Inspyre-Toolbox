import inspect
from argparse import ArgumentParser


class CommandRegistrar:
    _instance = None
    _invoking_classes = set()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, parser: ArgumentParser = None):

        if hasattr(self, "_initialized") and self._initialized:
            return  # Prevent re-initialization in singleton pattern

        from inspyre_toolbox.cli.ist_version_tool.arguments import Arguments  # Import here to avoid circular issues

        self._commands = set()
        self.__argument_parser = None
        self.argument_parser = parser if parser is not None else Arguments(command_registrar=self)

        self._initialized = True  # Mark instance as initialized

    @classmethod
    def get_invokers(cls):
        return cls._invoking_classes

    @property
    def argument_parser(self) -> ArgumentParser:
        """
        Get the argument parser instance.

        Returns:
            ArgumentParser:
                The argument parser instance.
        """
        return self.__argument_parser

    @argument_parser.setter
    def argument_parser(self, new):
        """
        Set the argument parser instance.

        Parameters:
            new (ArgumentParser):
                The new argument parser instance.

        Raises:
            ValueError:
                If the argument parser is already set or if the new argument parser is not an instance of ArgumentParser.
        """
        if self.__argument_parser is not None:
            raise ValueError("Argument parser already set.")

        if not isinstance(new, ArgumentParser):
            raise ValueError("Argument parser must be an instance of ArgumentParser.")

        self.__argument_parser = new

    @property
    def commands(self):
        """
        Get the list of registered command classes.

        Returns:
            List:
                A list of registered command classes.
        """
        return self._commands

    @property
    def initialized(self):
        return self._initialized

    @property
    def invoking_classes(self):
        return self._invoking_classes

    def inject_all(self):
        """
        Call `inject` method on all registered command classes.

        Returns:
            None
        """
        for command in self._commands:
            command.inject()

    def track_invocation(self):
        stack = inspect.stack()

        for frame in stack:
            caller = frame.frame.f_locals.get('self')  # Check that method was called from a class
            if caller and isinstance(caller, object):  # Ensure it's an object
                caller_class = type(caller)
                self._invoking_classes.add(caller_class)

    def check_registered(self, command_class):
        """
        Check if a command class is registered with the registrar.

        Parameters:
            command_class:
                The command class to check.

        Returns:
            bool:
                True if the command class is registered, False otherwise.
        """
        return command_class in self._commands

    def register_command(self, command_class):
        """
        Register a command class with the registrar.

        Parameters:
            command_class:
                The command class to register.

        Returns:
            None
        """
        if command_class not in self._commands:
            self._commands.add(command_class())
