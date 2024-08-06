import winreg

KEY_PATHS = {
        "Environment":           r"Environment",
        "Inspyre-Toolbox":       r"Software\Inspyre-Softworks\Inspyre-Toolbox",
        r"Inspyre-Toolbox\Path": r"Software\Inspyre-Softworks\Inspyre-Toolbox\Path",
        }


class RegistryManager:
    """
    A class to manage registry keys and values for a specific path in the Windows Registry.
    """

    KEY_PATH = KEY_PATHS['Inspyre-Toolbox']

    def __init__(self, key_path: str = None):
        """
        Initialize the RegistryManager with a specific registry key path.

        Parameters:
            key_path (str, optional):
                The path to the registry key. Defaults to the class-level KEY_PATH.
        """
        self.key_path = key_path or self.KEY_PATH

    @property
    def as_dict(self):
        """
        Get the registry key as a dictionary.

        Returns:
            dict:
                The registry key as a dictionary.

                The dictionary is structured as follows:
                - Keys are the names of the registry values.
                  - The names have '_' instead of '\\'.
                - Values are the corresponding values from the registry.
                - Subkeys are included as nested dictionaries, with their names joined by underscores to the base key path.

        Example Usage:
            reg_manager = RegistryManager()
            registry_dict = reg_manager.as_dict
            print(registry_dict)

        """
        _dict = {value[0]: value[1] for value in self.list_values()}
        for key in self.list_keys():
            _dict['_'.join(key.key_path.split('\\')[2:])] = key.as_dict
        return _dict

    @property
    def key_exists(self) -> bool:
        """
        Check if the key exists in the registry.

        Returns:
            bool: Whether the key exists.
        """
        return self.check_key_exists()

    @property
    def number_of_subkeys(self) -> int:
        """
        Get the number of subkeys in the registry key.

        Returns:
            int:
                The number of subkeys.
        """
        return self.get_number_of_subkeys()

    @property
    def num_subkeys(self) -> int:
        """
        Alias for the number_of_subkeys property.

        Returns:
            int:
                The number of subkeys.

        """
        return self.number_of_subkeys

    @property
    def subkeys(self) -> list:
        """
        List the keys in the registry key.

        Returns:
            list: The keys in the registry key.
        """
        return self.list_keys()

    @property
    def full_key_path(self) -> str:
        """
        Get the full key path.

        Returns:
            str: The full key path.
        """
        return f'HKEY_CURRENT_USER\\{self.key_path}'

    def check_key_exists(self) -> bool:
        """
        Check if the key exists in the registry.

        Returns:
            bool: Whether the key exists.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ):
                return True
        except FileNotFoundError:
            return False

    def create(self):
        """
        Create the key in the registry.
        """
        try:
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.key_path) as key:
                pass
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def get_number_of_subkeys(self):
        """
        Get the number of subkeys in the registry key.

        Returns:
            int:
                The number of subkeys.
        """
        return len(self.list_keys())

    def has_value(self, value_name: str) -> bool:
        """
        Check if a value exists in the registry.

        Parameters:
            value_name (str):
                The name of the value to check.

        Returns:
            bool: Whether the value exists.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ) as key:
                winreg.QueryValueEx(key, value_name)
                return True
        except FileNotFoundError:
            return False
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def list_keys(self):
        """
        List the keys in the registry key.

        Returns:
            list: The keys in the registry key.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ) as key:
                i = 0
                keys = []
                while True:
                    try:
                        name = winreg.EnumKey(key, i)
                        keys.append(RegistryManager(f'{self.key_path}\\{name}'))
                        i += 1
                    except OSError:
                        break
                return keys
        except FileNotFoundError:
            return None
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def list_key_paths(self):
        for key in self.list_keys():
            print(key.key_path)

    def list_values(self):
        """
        List the values in the registry key.

        Returns:
            list: The values in the registry key.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ) as key:
                i = 0
                values = []
                while True:
                    try:
                        name, value, type = winreg.EnumValue(key, i)
                        values.append((name, value, type))
                        i += 1
                    except OSError:
                        break
                return values
        except FileNotFoundError:
            return None
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def set_value(self, value_name: str, value: str):
        """
        Set a value in the registry.

        Parameters:
            value_name (str):
                The name of the value to set.

            value (str):
                The value to set.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE) as key:
                winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, value)
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def get_value(self, value_name: str) -> str:
        """
        Get a value from the registry.

        Parameters:
            value_name (str):
                The name of the value to get.

        Returns:
            str: The value.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_READ) as key:
                return winreg.QueryValueEx(key, value_name)[0]
        except FileNotFoundError:
            raise KeyError(f"Value '{value_name}' not found.")
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def delete_value(self, value_name: str):
        """
        Delete a value from the registry.

        Parameters:
            value_name (str):
                The name of the value to delete.
        """
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.key_path, 0, winreg.KEY_WRITE) as key:
                winreg.DeleteValue(key, value_name)
        except FileNotFoundError:
            raise KeyError(f"Value '{value_name}' not found.")
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def delete_key(self, skip_confirm: bool = False):
        """
        Delete the key from the registry.
        """
        try:
            winreg.DeleteKey(winreg.HKEY_CURRENT_USER, self.key_path)
        except FileNotFoundError:
            raise KeyError(f"Registry key '{self.key_path}' not found.")
        except OSError as e:
            if e.errno == 5:
                raise PermissionError("Access denied. Run as administrator.")
            else:
                raise e from e

    def __repr__(self):
        return f"<RegistryManager(key_path='{self.key_path}')> @ {hex(id(self))} with {self.number_of_subkeys} subkeys"


def delete_key(key_path: str):
    """
    Delete a key from the registry.

    Parameters:
        key_path (str):
            The path to the key to delete.
    """
    try:
        winreg.DeleteKey(winreg.HKEY_CURRENT_USER, key_path)
    except FileNotFoundError:
        raise KeyError(f"Registry key '{key_path}' not found.")
    except OSError as e:
        if e.errno == 5:
            raise PermissionError("Access denied. Run as administrator.")
        else:
            raise e from e


def has_key(key_path: str):
    """
    Check if a key exists in the registry.

    Parameters:
        key_path (str):
            The path to the key to check.

    Returns:
        bool: Whether the key exists.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_READ):
            return True
    except FileNotFoundError:
        return False
    except OSError as e:
        if e.errno == 5:
            raise PermissionError("Access denied. Run as administrator.")
        else:
            raise e from e


def set_registry_key(root, key, subkey, value):
    """
    The set_registry_key function sets a registry key.

    Args:
        root (HKEY):
            The root key to set.
        key (str):
            The key to set.
        subkey (str):
            The subkey to set.
        value (str):
            The value to set.

    Returns:
        None
    """
    with winreg.ConnectRegistry(None, root) as root_key:
        with winreg.OpenKey(root_key, key, 0, winreg.KEY_WRITE) as key:
            winreg.SetValue(key, subkey, winreg.REG_SZ, value)


def set_path_variable(value):
    set_registry_key(winreg.HKEY_CURRENT_USER, "Environment", "Path", value)


def find_registry_key(root, key, subkey):
    """
    The find_registry_key function finds a registry key.

    Args:
        root (HKEY):
            The root key to search in.
        key (str):
            The key to search for.
        subkey (str):
            The subkey to search for.

    Returns:
        The key if found, None if not found.
    """
    try:
        with winreg.ConnectRegistry(None, root) as root_key:
            with winreg.OpenKey(root_key, key, 0, winreg.KEY_READ) as key:
                try:
                    with winreg.OpenKey(key, subkey, 0, winreg.KEY_READ) as subkey:
                        return subkey
                except FileNotFoundError:
                    return None
    except FileNotFoundError:
        return None


def list_registry_keys(root, subkey):
    try:
        with winreg.OpenKey(root, subkey) as key:
            i = 0
            keys = []
            while True:
                try:
                    name, value, type = winreg.EnumValue(key, i)
                    keys.append((name, value, type))
                    i += 1
                except OSError:
                    break
            return keys
    except FileNotFoundError:
        return None


def get_registry_dict(root, subkey):
    return RegistryManager(f'{root}\\{subkey}').as_dict


def get_directories_from_registry_path():
    from inspyre_toolbox.sys_man.helpers.path import separate_path

    reg_man = RegistryManager(KEY_PATHS['Environment'])
    return separate_path(path) if (path := reg_man.as_dict['Path']) else None
