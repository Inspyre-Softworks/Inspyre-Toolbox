"""
This module provides a class to convert values between different byte units.

Classes:
    ByteConverter

Functions:
    get_lowest_unit_size:
        Get the lowest unit size for a given size.

Variables:
    VERSION:
        The version of the module.

    MOD_LOGGER:
        The logger for the module.

    MOD_LOGGER_NAME:
        The name of the logger for the module.


ByteConverter:
    A class to convert values between different byte units.

    Attributes:
        units (dict):
            A dictionary holding the conversion units.

        BYTE_FAMILY (list):
            A list of byte units.

        BIT_FAMILY (list):
            A list of bit units.

    Methods:
        convert(unit: str) -> float:
            Converts the bytes value to the specified unit.

        get_lowest_safe_conversion(keep_family: bool) -> tuple(float, str):
            Returns the lowest safe conversion for the value, a tuple containing the value and unit,
            respectively.

    Properties:
        conversion_map:
            Returns the conversion map.

        family_factors:
            Returns the factors of the family of the initial unit.

        keep_family:
            Returns the keep_family attribute.

        initial_bytes:
            Returns the initial value in bytes.

        initial_unit:
            Returns the initial unit of the value.

        initial_value:
            Returns the initial value.


"""
from typing import Any, Union

from inspy_logger import InspyLogger, Loggable

from inspyre_toolbox.common.about.version import VERSION_NUMBER
from inspyre_toolbox.syntactic_sweets.classes import validate_type

VERSION = VERSION_NUMBER

MOD_LOGGER = InspyLogger('inspyre_toolbox.conversions.bytes')

MOD_LOGGER.debug(f'Byte conversion module loaded. | Inspyre-Toolbox v{VERSION}')


class ByteConverter(Loggable):
    """
    ByteConverter class for converting between different units of digital information storage.

    This class provides a flexible way to convert between different byte and bit units
    such as bytes, kilobytes, megabytes, gigabytes, and their respective bit equivalents.

    Attributes:
    ----------
    value (float):
        The numeric value of the data amount.

    unit (str):
        The unit of the data amount, e.g., 'byte', 'kilobyte', etc.

    UNIT_FAMILIES (list):
        A dictionary that organizes units into families based on their scale, e.g., byte-based units.

    UNIT_CONVERSIONS (dict):
        A dictionary that maps unit strings to their conversion factors relative to 1 byte.

    Methods:
    -------
    convert(to_unit, strict_case=True):
        Converts the stored value to a specified unit.

    get_lowest_safe_conversion(keep_family=True):
        Returns the smallest unit (in terms of scale) that represents the value without falling below 1 in the desired family.
    """
    # Dictionary holding the conversion units
    UNIT_CONVERSIONS = {
        'bit': 1/8,
            'byte':      1,
            'kilobit':   125,
            'kilobyte':  1000,
            'megabit':   125000,
            'megabyte':  1000000,
            'gigabit':   125000000,
            'gigabyte':  1000000000,
            'terabit':   125000000000,
            'terabyte':  1000000000000,
            'petabit':   125000000000000,
            'petabyte':  1000000000000000,
            'exabit':    125000000000000000,
            'exabyte':   1000000000000000000,
            'zettabit':  125000000000000000000,
            'zettabyte': 1000000000000000000000,
            'yottabit':  125000000000000000000000,
            'yottabyte': 1000000000000000000000000
            }

    UNIT_FAMILIES = {
            'byte': ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte', 'exabyte', 'zettabyte',
                     'yottabyte'],
            'bit':  ['bit', 'kilobit', 'megabit', 'gigabit', 'terabit', 'petabit', 'exabit', 'zettabit', 'yottabit']
            }

    def __init__(
            self,
            value: Union[int, float],
            unit: str
            ):
        """
        Initialize a ByteConverter object with a specific value and unit.

        Parameters:
        ----------
        value (Union[int, float]):
            The numeric value of the data amount.

        unit : str
            The unit of the data amount, e.g., 'byte', 'kilobyte', etc.
        """
        super().__init__(parent_log_device=MOD_LOGGER)
        # self.__keep_family = None
        #
        # unit = unit.removesuffix('s')
        #
        # if unit not in self.UNITS:
        #     raise ValueError(f'Invalid unit: {unit}')
        #
        # if value < 0:
        #     raise ValueError('Value cannot be negative.')
        #
        # self.__initial_unit = unit
        # self.__initial_value = value
        #
        # # Convert the input value to bytes
        # self.__bytes = value * self.UNITS[unit]
        # self.keep_family = keep_family

        unit = unit.lower()
        self.__initial_value = value
        self.__initial_unit = unit

        self.__value = None

        self.unit = unit.lower()

        self.__family_factors = self.__calculate_family_factors()

    def __calculate_family_factors(self) -> dict:
        """
        Calculate the family factors based on the UNIT_FAMILIES and UNIT_CONVERSIONS.

        Returns:
        -------
        dict:
            A dictionary of family units and their conversion factors.
        """
        family_factors = {}

        for family, units in self.UNIT_FAMILIES.items():
            family_factors[family] = {unit: self.UNIT_CONVERSIONS[unit] for unit in units}

        return family_factors

    def convert(self, to_unit, strict_case=True):
        """
        Convert the stored value to a specified unit.


        Parameters:
        ----------
        to_unit(str):
            The target unit for conversion.

        strict_case(Optional[bool])
            Whether to strictly enforce case sensitivity (default is True).

        Returns:
        -------
        float:
            The converted value.
        """
        log = self.create_child_logger()

        if not strict_case:
            log.debug(f'Lowering the case of the target unit; {to_unit}')
            to_unit = to_unit.lower()
        else:
            log.debug(f'Strict case sensitivity is enabled. Target unit: {to_unit}')

        if to_unit not in self.UNIT_CONVERSIONS:
            log.error(f"Invalid unit: {to_unit}. Valid units are: {list(self.UNIT_CONVERSIONS.keys())}")
            raise ValueError(f"Invalid unit: {to_unit}. Valid units are: {list(self.UNIT_CONVERSIONS.keys())}")

        from_factor = self.UNIT_CONVERSIONS[self.unit]

        to_factor = self.UNIT_CONVERSIONS[to_unit]
        log.debug(f"To factor: {to_factor} | From factor: {from_factor}")

        converted_value = self.value * from_factor / to_factor
        log.debug(f"Converted {self.value} {self.unit} to {converted_value} {to_unit}")

        return converted_value

    def get_lowest_safe_conversion(
            self,
            keep_family: bool = False
            ) -> tuple[Any, int | float]:
        """
        Returns the lowest safe conversion for the value.

        Parameters:
            keep_family (bool):
                A flag indicating whether to keep the family of the initial unit.

        Returns:
            tuple:
                The lowest safe conversion value and unit.
        """
        log_name = f'{self.log_device.name}:get_lowest_safe_conversion'
        log = self.log_device.find_child_by_name(log_name)[0] if self.log_device.has_child(
            log_name) else self.create_child_logger()

        sorted_units = None

        if keep_family:
            log.debug(f'Keeping the family of the initial unit: {self.__initial_unit}')
            for family, units in self.UNIT_FAMILIES.items():
                if self.unit in units:
                    sorted_units = sorted(units, key=lambda x: self.UNIT_CONVERSIONS[x], reverse=True)
                    break
        else:
            sorted_units = sorted(self.UNIT_CONVERSIONS.keys(), key=lambda x: self.UNIT_CONVERSIONS[x], reverse=True)

        if sorted_units is None:
            log.error(f'No units found for the initial unit: {self.__initial_unit}')
            raise ValueError(f'No units found for the initial unit: {self.__initial_unit}')

        for unit in sorted_units:
            converted_value = self.convert(unit)
            if converted_value >= 1:
                log.debug(
                    f'Lowest safe conversion: {converted_value} {unit} | Original value: {self.__initial_value} {self.__initial_unit}')
                return unit, converted_value

        return self.unit, self.value

        #     family = self.BYTE_FAMILY if self.__initial_unit in self.BYTE_FAMILY else self.BIT_FAMILY
        #     log.debug(f'Family of the initial unit: {family}')
        #     factors = [self.UNITS[unit] for unit in family]
        # else:
        #     log.debug('Not keeping the family of the initial unit.')
        #     factors = [self.UNITS[unit] for unit in self.UNITS]
        #
        # log.debug(f'Factors: {factors}')
        #
        # base_value = self.__initial_value * self.UNITS[self.__initial_unit]
        # log.debug(f'Base value: {base_value}')
        #
        # lowest_value = float('inf')
        # lowest_unit = None
        #
        # for unit, factor in self.UNITS.items():
        #     log.debug(f'Checking unit: {unit}')
        #     log.debug(f'Factor: {factor}')
        #     if factor in factors:
        #         log.debug(f'Factor in factors: {factor}')
        #         converted_value = base_value / factor
        #         log.debug(f'Converted value: {Numerical(converted_value, unit).count_noun()}')
        #         if 1.0 <= converted_value < lowest_value:
        #             log.debug(f'Converted value is less than lowest value: {converted_value}')
        #             lowest_value = converted_value
        #             log.debug(f'New lowest value: {lowest_value}')
        #             lowest_unit = unit
        #             log.debug(f'New lowest unit: {lowest_unit}')
        #
        # log.debug(f'Lowest value: {lowest_value}, Lowest unit: {lowest_unit}')
        #
        # if lowest_unit is None:
        #     log.debug('No unit found. Finding the smallest factor.')
        #     smallest_factor_index = factors.index(min(factors))
        #     log.debug(f'Smallest factor index: {smallest_factor_index}')
        #     lowest_unit = list(self.UNITS.keys())[smallest_factor_index]
        #     log.debug(f'Lowest unit: {lowest_unit}')
        #     lowest_value = base_value / min(factors)
        #     log.debug(f'Lowest value: {Numerical(lowest_value, lowest_unit).count_noun()}')
        #
        # log.debug(f'Final lowest value: {lowest_value}, Final lowest unit: {lowest_unit} | '
        #           f'{Numerical(lowest_value, lowest_unit).count_noun()}')
        #
        # return lowest_value, lowest_unit

    @property
    def family_factors(self) -> list[float]:
        """
        Returns the factors of the family of the initial unit.

        Returns:
            list:
                The factors of the family of the initial unit.

        """
        return self.__family_factors

    @property
    def keep_family(self):
        """
        Returns the keep_family attribute.

        Returns:
            bool:
                The keep_family attribute.
        """
        return self.__keep_family

    @keep_family.setter
    @validate_type(bool)
    def keep_family(self, new):
        """
        Sets the keep_family attribute.

        Parameters:
            new (bool):
                The value to set the keep_family attribute to.

        Returns:
            None
        """
        self.__keep_family = new

    @property
    def initial_bytes(self):
        """
        Returns the initial value in bytes.

        Returns:
            float:
                The initial value in bytes.
        """
        return self.__bytes

    @property
    def initial_unit(self) -> str:
        """
        Returns the initial unit of the value.

        Returns:
            str:
                The initial unit of the value
        """
        return self.__initial_unit

    @initial_unit.setter
    def initial_unit(self, unit):
        """
        Placeholder for the initial unit setter.

        This setter is a placeholder and raises an AttributeError when called.

        Parameters:
            unit:
                Unused parameter.

        Returns:
            None

        Raises:
            AttributeError:
                The initial unit cannot be changed.
        """
        raise AttributeError("The initial unit cannot be changed.")

    @property
    def initial_value(self):
        """
        Returns the initial value.

        Returns:
            Union[int, float]:
                The initial value.
        """
        return self.__initial_value

    @initial_value.setter
    def initial_value(self, value):
        """
        Placeholder for the initial value setter.

        This setter is a placeholder and raises an AttributeError when called.

        Parameters:
            value:
                Unused parameter.

        Returns:
            None

        Raises:
            AttributeError:
                The initial value cannot be changed.
        """
        raise AttributeError("The initial value cannot be changed.")

    @property
    def units(self):
        return self.UNITS

    @property
    def value(self):
        return self.__value or self.__initial_value

    @value.setter
    @validate_type(int, float, preferred_type=float)
    def value(self, new):
        self.__value = new

    # Below are property methods that return the value in a specific unit

    @property
    def bits(self):
        """Returns the value in bits"""
        return self.convert('bit')

    @property
    def kilobits(self):
        """Returns the value in kilobits"""
        return self.convert('kilobit')

    @property
    def megabits(self):
        """Returns the value in megabits"""
        return self.convert('megabit')

    @property
    def gigabits(self):
        """Returns the value in gigabits"""
        return self.convert('gigabit')

    @property
    def terabits(self):
        """Returns the value in terabits"""
        return self.convert('terabit')

    @property
    def petabits(self):
        """Returns the value in petabits"""
        return self.convert('petabit')

    @property
    def exabits(self):
        """Returns the value in exabits"""
        return self.convert('exabit')

    @property
    def zetabits(self):
        """Returns the value in zetabits"""
        return self.convert('zetabit')

    @property
    def yottabits(self):
        """Returns the value in yottabits"""
        return self.convert('yottabit')

    @property
    def bytes(self):
        """Returns the value in bytes"""
        return self.convert('byte')

    @property
    def kilobytes(self):
        """Returns the value in kilobytes"""
        return self.convert('kilobyte')

    @property
    def megabytes(self):
        """Returns the value in megabytes"""
        return self.convert('megabyte')

    @property
    def gigabytes(self):
        """Returns the value in gigabytes"""
        return self.convert('gigabyte')

    @property
    def terabytes(self):
        """Returns the value in terabytes"""
        return self.convert('terabyte')

    @property
    def petabytes(self):
        """Returns the value in petabytes"""
        return self.convert('petabyte')

    @property
    def exabytes(self):
        """Returns the value in exabytes"""
        return self.convert('exabyte')

    @property
    def zetabytes(self):
        """Returns the value in zetabytes"""
        return self.convert('zetabyte')

    @property
    def yottabytes(self):
        """Returns the value in yottabytes"""
        return self.convert('yottabyte')

    def __str__(self):
        return f'{self.__initial_value} {self.__initial_unit}'

    def __repr__(self):
        return \
            (
                    f'<ByteConverter@{hex(id(self))}: '
                    f'Initial value: {self.__initial_value} | Initial unit: {self.__initial_unit}>'
            )


def get_lowest_unit_size(size: int) -> tuple[Union[int, float], str]:
    """
    Get the lowest unit size for a given size.

    Parameters:
        size (int):
            The size to convert.

    Returns:
        tuple[Union[int, float], str]:
            The converted size and the unit.

    Examples:
        >>> get_lowest_unit_size(1024)
        (1.0, 'KB')
        >>> get_lowest_unit_size(1024 * 1024)
        (1.0, 'MB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024)
        (1.0, 'GB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024)
        (1.0, 'TB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'PB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'EB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'ZB')
        >>> get_lowest_unit_size(1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024 * 1024)
        (1.0, 'YB')
    """
    units = ['byte', 'kilobyte', 'megabyte', 'gigabyte', 'terabyte', 'petabyte', 'exabyte', 'zetabyte', 'yottabyte']
    units.reverse()
    converter = ByteConverter(size, 'byte')

    for unit in units:
        converted = converter.convert(unit.lower())

        if converted >= 1:
            return converted, unit.upper(),
