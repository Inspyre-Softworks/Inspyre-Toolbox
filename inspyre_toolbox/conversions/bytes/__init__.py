from typing import Union

from inspy_logger import InspyLogger, Loggable

from inspyre_toolbox.humanize import Numerical
from inspyre_toolbox.syntactic_sweets.properties import validate_type
from inspyre_toolbox.version import parse_version

VERSION = parse_version()

MOD_LOGGER = InspyLogger('inspyre_toolbox.conversions.bytes')

MOD_LOGGER.debug(f'Byte conversion module loaded. | Inspyre-Toolbox v{VERSION}')


class ByteConverter(Loggable):
    """
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
    """
    # Dictionary holding the conversion units
    UNITS = {
        'byte': 1,
        'kilobyte': 1024,
        'megabyte': 1024**2,
        'gigabyte': 1024**3,
        'terabyte': 1024**4,
        'petabyte': 1024**5,
        'exabyte': 1024**6,
        'zetabyte': 1024**7,
        'yottabyte': 1024**8,
        'bit': 1/8,
        'kilobit': 1024/8,
        'megabit': (1024**2)/8,
        'gigabit': (1024**3)/8,
        'terabit': (1024**4)/8,
        'petabit': (1024**5)/8,
        'exabit': (1024**6)/8,
        'zetabit': (1024**7)/8,
        'yottabit': (1024**8)/8,
            }

    BYTE_FAMILY = [
            'byte', 'kilobyte', 'megabyte',
            'gigabyte', 'terabyte', 'petabyte',
            'exabyte', 'zetabyte', 'yottabyte'
            ]

    BIT_FAMILY = [
            'bit', 'kilobit', 'megabit',
            'gigabit', 'terabit', 'petabit',
            'exabit', 'zetabit', 'yottabit'
            ]

    def __init__(
            self,
            value: Union[int, float],
            unit: str,
            keep_family: bool = False
            ):
        """
        Initializes the ByteConverter class.

        Parameters:
            value (Union[int, float]):
                The value to convert.

            unit (str):
                The unit of the value.

            keep_family (bool):
                A flag indicating whether to keep the family of the initial unit. To keep the
                "family" of a unit means to keep the units that are in the same family as the
                initial unit.

                Examples:
                     - The initial unit is 'kilobyte';
                         The family would be
                            - kilobyte
                            - megabyte
                            - gigabyte
                            - terabyte
                            - petabyte
                            - exabyte
                            - zetabyte
                            - yottabyte

                    - The initial unit is 'kilobit';
                        The family would be
                            - kilobit
                            - megabit
                            - gigabit
                            - terabit
                            - petabit
                            - exabit
                            - zetabit
                            - yottabit
        """
        super().__init__(parent_log_device=MOD_LOGGER)
        self.__keep_family = None

        unit = unit.removesuffix('s')

        if unit not in self.UNITS:
            raise ValueError(f'Invalid unit: {unit}')

        if value < 0:
            raise ValueError('Value cannot be negative.')

        self.__initial_unit = unit
        self.__initial_value = value

        # Convert the input value to bytes
        self.__bytes = value * self.UNITS[unit]
        self.keep_family = keep_family

        self.__family_factors = [self.UNITS[u] for u in self.UNIT_FAMILY]

    def convert(self, unit: str, strict_case: bool = False) -> float:
        """
        Converts the bytes value to the specified unit.

        Parameters:
            unit (str):
                The unit to convert the value to. (Must be a key in the :ref:`units` dictionary)

            strict_case (bool):
                A flag indicating whether to convert the unit to lowercase before checking if it is
                a valid unit.

        Returns:
            float:
                The converted value.
        """
        log_name = f'{self.log_device.name}:convert'
        log = self.log_device.find_child_by_name(log_name)[0] if self.log_device.has_child(
                log_name) else self.create_child_logger()

        unit = unit.removesuffix('s')

        if not strict_case:
            log.debug(f'Converting case ({unit}) to lower.')
            unit = unit.lower()

        log.debug(f'Searching valid units for {unit}...')
        if unit not in self.UNITS:
            log.error(f'Invalid unit: {unit}')
            raise ValueError(f'Invalid unit: {unit}')

        # Convert the bytes value to the specified unit
        return self.initial_bytes / self.units[unit]

    def get_lowest_safe_conversion(
            self,
            keep_family: bool = False
            ) -> tuple[float, str]:
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

        if keep_family:
            log.debug(f'Keeping the family of the initial unit: {self.__initial_unit}')
            family = self.BYTE_FAMILY if self.__initial_unit in self.BYTE_FAMILY else self.BIT_FAMILY
            log.debug(f'Family of the initial unit: {family}')
            factors = [self.UNITS[unit] for unit in family]
        else:
            log.debug('Not keeping the family of the initial unit.')
            factors = [self.UNITS[unit] for unit in self.UNITS]

        log.debug(f'Factors: {factors}')

        base_value = self.__initial_value * self.UNITS[self.__initial_unit]
        log.debug(f'Base value: {base_value}')

        lowest_value = float('inf')
        lowest_unit = None

        for unit, factor in self.UNITS.items():
            log.debug(f'Checking unit: {unit}')
            log.debug(f'Factor: {factor}')
            if factor in factors:
                log.debug(f'Factor in factors: {factor}')
                converted_value = base_value / factor
                log.debug(f'Converted value: {Numerical(converted_value, unit).count_noun()}')
                if 1.0 <= converted_value < lowest_value:
                    log.debug(f'Converted value is less than lowest value: {converted_value}')
                    lowest_value = converted_value
                    log.debug(f'New lowest value: {lowest_value}')
                    lowest_unit = unit
                    log.debug(f'New lowest unit: {lowest_unit}')

        log.debug(f'Lowest value: {lowest_value}, Lowest unit: {lowest_unit}')

        if lowest_unit is None:
            log.debug('No unit found. Finding the smallest factor.')
            smallest_factor_index = factors.index(min(factors))
            log.debug(f'Smallest factor index: {smallest_factor_index}')
            lowest_unit = list(self.UNITS.keys())[smallest_factor_index]
            log.debug(f'Lowest unit: {lowest_unit}')
            lowest_value = base_value / min(factors)
            log.debug(f'Lowest value: {Numerical(lowest_value, lowest_unit).count_noun()}')

        log.debug(f'Final lowest value: {lowest_value}, Final lowest unit: {lowest_unit} | '
                  f'{Numerical(lowest_value, lowest_unit).count_noun()}')

        return lowest_value, lowest_unit

    @property
    def conversion_map(self):
        """
        Returns the conversion map.

        This method returns a dictionary containing the conversion units based on the value of the
        keep_family attribute.

        Returns:
            dict:
                The conversion map.

        """
        return {unit: self.UNITS[unit] for unit in (self.UNIT_FAMILY if self.keep_family else self.UNITS)}

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
    def UNIT_FAMILY(self):
        """
        Returns the family of the initial unit.

        Returns:
            list:
                The family of the initial unit.
        """
        if not self.initial_unit:
            return None

        return self.BYTE_FAMILY if self.initial_unit in self.BYTE_FAMILY else self.BIT_FAMILY

    @property
    def UNIT_FAMILY_NAME(self):
        """
        Returns the name of the family of the initial unit.

        Returns:
            str:
                The name of the family of the initial unit.
        """
        if not self.initial_unit:
            return None

        return 'byte' if self.initial_unit in self.BYTE_FAMILY else 'bit'

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

    def __str__(self) -> str:
        return f'{self.__initial_value} {self.__initial_unit}'

    def __repr__(self):
        return \
            (
                    f'<ByteConverter@{hex(id(self))}: '
                    f'Initial value: {self.__initial_value} | Initial unit: {self.__initial_unit}>'
            )
