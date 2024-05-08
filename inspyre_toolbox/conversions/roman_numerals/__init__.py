from collections import OrderedDict

from inspyre_toolbox.conversions.roman_numerals.errors import InvalidRomanNumeralStringError
from inspyre_toolbox.core_helpers.logging import ROOT_ISL_DEVICE, add_isl_child
from inspyre_toolbox.humanize import Numerical

ROOT_ISL_DEVICE.set_level('DEBUG')

LOG_NAME = 'conversions.roman_numerals'

MOD_LOG_DEVICE = add_isl_child(LOG_NAME)

LOG = MOD_LOG_DEVICE.logger

LOG.debug('Logger started.')

ROMAN_NUMERALS = OrderedDict(
        {
                'I':  1,
                'IV': 4,
                'V':  5,
                'IX': 9,
                'X':  10,
                'XL': 40,
                'L':  50,
                'XC': 90,
                'C':  100,
                'CD': 400,
                'D':  500,
                'CM': 900,
                'M':  1000
        }
)
"""
.. _rn_constant:

    A list of roman numerals that are constant.
    
    A list of roman numeral strings to compare against. The list is ordered by the 
    value of the roman numeral. The list is primarily used to determine if a provided string 
    is valid.
    
    
"""


def validate_roman_numeral_str(roman_numeral: str):
    """
    The 'validate_roman_numeral_str' function checks to see if the parameter 'roman_numeral' is a string.
    If it is, then each character in the string will be checked against 'ROMAN_NUMERALS'. If any characters are not
    found in :ref:`rn_constant`, an :class:`InvalidRomanNumeralStringError` exception will be raised

    Args:
        roman_numeral:str: Pass the roman numeral string to be validated

    Returns:
        True if the roman_numeral is a valid roman numeral string
    """
    log_device = ROOT_ISL_DEVICE.get_child(f'{LOG_NAME}.validate_roman_numeral_str')
    log = log_device.logger

    try:
        if not isinstance(roman_numeral, str):
            raise TypeError(f"The parameter 'roman_numeral' for 'validate_roman_numeral_str' must be of type 'str' "
                            f"not {type(roman_numeral)}'")

        for char in list(roman_numeral):
            if char not in ROMAN_NUMERALS:
                raise InvalidRomanNumeralStringError(roman_numeral, skip_print=True)
    except TypeError as e:
        log.error(e)
        return False
    except InvalidRomanNumeralStringError as e:
        log.error(e)
        return False
    return True


class RomanNumeral(object):

    def __init__(self, roman_numeral: str, noun: str = None):
        self.__roman_numeral = roman_numeral
        self.__integer = None
        self.__noun = noun
        self.__replace_noun = True
        self.__rn_changed = None

    @property
    def numeral_map(self):
        return ROMAN_NUMERALS

    @property
    def validate(self):
        return validate_roman_numeral_str(self.formatted)

    @property
    def provided(self):
        return self.__roman_numeral

    @provided.setter
    def provided(self, new_roman_numeral):
        nrn = new_roman_numeral.upper()
        if not validate_roman_numeral_str(nrn):
            raise InvalidRomanNumeralStringError(provided=nrn)
        self.__roman_numeral = nrn
        self.__rn_changed = True

    @property
    def formatted(self):
        return self.provided.upper()

    @property
    def noun(self):
        return self.__noun

    @noun.setter
    def noun(self, noun):
        if not isinstance(noun, str):
            raise ValueError(f"Provided property value for 'noun' must be of type 'str' not {type(noun)}")
        else:
            self.__noun = noun

    @property
    def as_numerical(self):
        return Numerical(self.as_int, noun=self.noun or None)

    @property
    def as_int(self):
        i = 0
        num = 0
        while i < len(self.formatted):
            if i + 1 < len(self.formatted) and self.formatted[i:i + 2] in ROMAN_NUMERALS:
                num += ROMAN_NUMERALS[self.formatted[i:i + 2]]
                i += 2
            else:
                num += ROMAN_NUMERALS[self.formatted[i]]
                i += 1
        self.__integer = num

        return self.__integer


def roman_numeral_to_integer(roman_numeral: str, noun: str = None, return_object=False, commify: bool = False):
    """
    The 'roman_numeral_to_integer' function converts a Roman Numeral to an integer.

    Args:
        roman_numeral: (str):
            Specify the roman numeral to be converted. (Required)

        noun: (str):
            Specify a noun for the roman numeral., (Optional, defaults to NoneType)

        return_object (bool):
            Determine whether the function should return an object or a string. (Optional; defaults to False)

        commify(bool)=False: Specify whether the numerical value should be returned with commas separating thousands

    Returns:
        The integer value of a roman numeral string.
    """
    if not isinstance(roman_numeral, str):
        raise TypeError(f'Parameter value for "roman_numeral" must be of type "str" not "{type(roman_numeral)}"')

    rn = RomanNumeral(roman_numeral, noun=noun)

    if return_object:
        return rn

    return rn.as_numerical.commify() if commify else rn.as_int
