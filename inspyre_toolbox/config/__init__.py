import json
from pathlib import Path

from inspyre_toolbox.syntactic_sweets.classes.decorators import validate_type

CONFIG_SYSTEMS = {
        'path'
        }


def get_system_config_schema_path(system: str) -> Path:
    """
    Get the path to the schema for the specified system.

    Parameters:
        system (str):
            The system to get the schema for.

    Returns:
        Path:
            The path to the schema file.

    Raises:
        ValueError:
            Raised when the specified system is not supported.
    """
    if system not in CONFIG_SYSTEMS:
        raise ValueError(f"Unsupported system: '{system}'")

    return Path(__file__).parent.joinpath(f'{system}.json')


class Config:
    """
    A class to manage configuration settings from a JSON file.

    The `Config` class reads configuration data from a JSON file and dynamically creates
    classes based on the configuration parameters. Each property includes a getter and setter
    with type validation.

    Attributes:
        json_path (str):
            Path to the JSON file containing configuration data.

    Methods:
        __init__(json_path):
            Initializes the :class:`Config` instance by loading configuration from the specified JSON file.

        _load_from_json(json_path):
            Loads configuration data from the JSON file and creates classes dynamically.

        _create_property(name, description, type_):
            Creates a property with the given name, description, and type.
    """

    def __init__(self, json_path):
        """
        Initializes the `Config` instance by loading configuration from the specified JSON file.

        Parameters:
            json_path (str): Path to the JSON file containing configuration data.

        Returns:
            None
        """
        self._load_from_json(json_path)

    def _load_from_json(self, json_path):
        """
        Loads configuration data from the JSON file and creates classes dynamically.

        Parameters:
            json_path (str): Path to the JSON file containing configuration data.

        Returns:
            None
        """
        with open(json_path, 'r') as file:
            data = json.load(file)
        for key, value in data.items():
            setattr(self, f"_{key}", value['default'])
            self._create_property(key, value['description'], value['type'])

    def _create_property(self, name, description, type_):
        """
        Creates a property with the given name, description, and type.

        Parameters:
            name (str): The name of the property.
            description (str): A description of the property.
            type_ (str): The type of the property, one of 'string', 'bool', 'int', 'float', 'list', or 'dict'.

        Returns:
            None
        """
        type_map = {
                "string": str,
                "bool":   bool,
                "int":    int,
                "float":  float,
                "list":   list,
                "dict":   dict
                }
        type_cls = type_map.get(type_, str)

        def getter(self):
            return getattr(self, f"_{name}")

        def setter(self, value):
            setattr(self, f"_{name}", value)

        getter.__doc__ = f"""
        Returns the {name} attribute.

        Returns:
            {type_cls.__name__}:
                {description}
        """
        setter.__doc__ = f"""
        Sets the {name} attribute.

        Parameters:
            new ({type_cls.__name__}):
                The value to set the {name} attribute to.

        Returns:
            None
        """
        setter = validate_type(type_cls)(setter)

        prop = property(getter, setter)
        setattr(self.__class__, name, prop)


def load_sample_config(config_system: str) -> dict:
    """
    Load the sample configuration file.

    Parameters:
        config_system (str):
            The configuration system to use.

    Returns:
        dict:
            The sample configuration.
    """
    if config_system.lower() not in CONFIG_SYSTEMS:
        raise ValueError(f"Invalid config system: '{config_system}'")

    sample_config_file = Path(__file__).parent.joinpath(f'{config_system}.json')

    if not sample_config_file.exists():
        raise FileNotFoundError(f"Sample configuration file not found: '{sample_config_file}'")

    with open(sample_config_file, 'r') as file:
        sample_config = json.load(file)

    return sample_config
