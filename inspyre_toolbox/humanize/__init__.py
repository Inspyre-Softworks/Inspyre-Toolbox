#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 01:23:36 2021

@author: taylor
"""
import typing
from decimal import Decimal
from typing import Any, Optional, Union, Callable, ContextManager

from inflect import engine

from inspyre_toolbox.core_helpers.logging import ROOT_ISL_DEVICE
from inspyre_toolbox.humanize.errors import HumanizeErrors


# Instantiate inflect.engine as 'INF'
INF = engine()

NUM_ERR = HumanizeErrors.NumericalErrors


class NumericalStrings(object):
    less_than_20: list[Union[str, Any]] = [
            "",
            "One",
            "Two",
            "Three",
            "Four",
            "Five",
            "Six",
            "Seven",
            "Eight",
            "Nine",
            "Ten",
            "Eleven",
            "Twelve",
            "Thirteen",
            "Fourteen",
            "Fifteen",
            "Sixteen",
            "Seventeen",
            "Eighteen",
            "Nineteen",
            ]
    tens: list[str] = [
            "",
            "Ten",
            "Twenty",
            "Thirty",
            "Forty",
            "Fifty",
            "Sixty",
            "Seventy",
            "Eighty",
            "Ninety",
            ]
    
    thousands: list[str] = [
            "",
            "Thousand",
            "Million",
            "Billion"
            ]


class Numerical(object):
    """

    A class that allows you to manipulate numbers with greater-flexibility.

    """
    
    
    def __init__(self, number, noun: typing.Optional[str] = None, store_as_float=False):
        """

        Create a new instance, with a new number to manipulate

        Args:
            number (int|float): The subject number.
            noun: The noun to count.
        """
        # First, check whether 'number' is an integer or a float or not. If not; we raise an error
        
        self.__store_as_float = store_as_float
        
        if not isinstance(number, float) and store_as_float:
            try:
                number = int(number)
            except ValueError as e:
                raise NUM_ERR.NotANumberError(
                        var=number,
                        var_name="number",
                        msg=f"Type {type(number)} is not valid. Must be {type(1)} or {type(1.1)}",
                        ) from e
            
            if store_as_float:
                number = float(number)
        
        self.__number = number
        
        self.__noun = noun
        
        self.__commified = self.commify()
        
        self.log_name = 'Inspyre-Toolbox.humanize.Numerical'
        
        self.cls_logger = ROOT_ISL_DEVICE.add_child(self.log_name)
        self.cls_logger.debug(f"Started logger: {self.log_name}")
    
    
    def count_noun(
            self,
            number: Optional[Union[float, str, int]] = None,
            noun: Optional[Union[str, None]] = None,
            save_number: Optional[bool] = True,
            save_noun: Optional[bool] = True,
            **kwargs: object):
        """
        
        Args:
            
            number (Optional, float | int | str):
                The number of the nouns you want to count.
            
            noun (Optional, str):
                The thing you want to describe the number of. Defaults to 'self.__noun'.
            
            save_number (Optional, bool):
                If you provided a value for the 'number' parameter this parameter's value will indicate whether the
                value of 'number' should replace 'self.number'. Defaults to bool(True).
            
            save_noun (Optional, bool):
                If you provided a value for the 'noun' parameter and self.__noun isn't NoneType and differs from the
                provided value 'save_noun' will indicate whether the new value for 'noun' should replace
                'self.__noun'. Defaults to bool(True).
            
            **kwargs:
            
                full_stop (bool):
                 Include a full-stop punctuation mark at the end of the final statement. Users that
                 are from America may know this punctuation mark better as 'period' (or; '.'. See
                 below for the 'period' parameter alias)
                 (Defaults to boo  l(False)

                period (bool):
                    Include a period mark at the end of the final statement. Users from some areas may
                    know this mark better as 'full-stop'
    
                noun (str):
                    Returns a string with the appropriate statement iy,.hy,i for annotating counts of various nouns.
    
                count (int/float, optional):
                    The number of 'noun' that exists.
                    (Defaults to 'Numerical.number')
    
                only_noun (bool, optional):
                    Return only the properly pluralized noun.
                    (Defaults to False)
    
                skip_commify (bool, optional):
                    (Ignored if either 'only_noun' or 'count_to_words' are True) Return the number as
                    part of the statement with commas added to the proper places.
                    (Defaults to False)
    
                to_words (bool, optional):
                    (Ignored if 'only_noun' is True) Modify the first part of the statement
                    (which contains the count) to words instead of numbers.
                    (Defaults to False.)
    
                capitalize (bool, optional):
                    Return the words for the count with the first letter capitalized.
                    (Defaults to False, ignored if 'count_to_words' is False.)
    
                round_num (int, optional):
                    Round the number returned to a given precision in decimal digits.
                    (Defaults to None(NoneType), ignored if 'only_noun' is True.)

        Returns:

        """

        number_changed  = False
        noun_changed    = False
        number_previous = None
        noun_previous   = None
        
        if number is not None:
            try:
                number = float(number)
                if number != self.__number and not save_number:
                    number_previous = self.__number
                    number_changed = True
                
                self.__number = number
            except ValueError as e:
                
                warning = "If passing a noun alone to 'count_noun' you need to include the parameter name\n" \
                          "For example:\n" \
                          "\n" \
                          "number.count_noun(noun='banana')\n" \
                          "NOT\n" \
                          "number.count_noun('banana')"
                
                print(warning)
                
                raise ValueError(warning) from e
        
        if noun is not None:
            
            noun = str(noun)
            try:
                noun = str(noun)
                self.__noun = noun
                if self.__noun is not None and noun != self.__noun:
                    if not save_noun:
                        noun_changed = True
                        noun_previous = self.__noun
                    
                    self.__noun = noun
            except ValueError as e:
                raise ValueError(f"'noun' should be {type(str())} not {type(noun)}") from e
        
        ret = self.__count_noun(noun=self.__noun, count=self.__number, **kwargs)
        
        if number_changed:
            self.__number   = number_previous
            number_previous = None
            number_changed  = False
        if noun_changed:
            self.__noun   = noun_previous
            noun_previous = None
            noun_changed  = None
        
        return ret
    
    
    @property
    def noun(self):
        """

        The value of 'Numerical.noun'.

        Returns:
            Numerical.noun (str):
                The value of 'Numerical.noun'

        """
        return self.__noun
    
    
    @noun.setter
    def noun(self, new_value):
        if isinstance(new_value, str):
            self.__noun = new_value
        else:
            raise ValueError("Can only set a string as 'noun'")
    
    
    @noun.deleter
    def noun(self):
        self.__noun = None
    
    
    @property
    def dec_num(self):
        return Decimal(self.number)
    
    
    @property
    def commified(self):
        return self.commify()
    
    
    @property
    def number(self):
        return self.__number
    
    
    @number.setter
    def number(self, new_value):
        log_name = f'{self.log_name}.number.Setter'
        log = ROOT_ISL_DEVICE.add_child(log_name)
        try:
            float(new_value)
            int(new_value)
        except ValueError as e:
            log.error(f"The new value must be of type 'int' or 'float' not {type(new_value)}")

        self.__number = new_value
        log.info("New value set for 'Numerical.number'")


    @property
    def store_as_float(self):
        return self.__store_as_float

    @store_as_float.setter
    def store_as_float(self, opt):
        log = ROOT_ISL_DEVICE.add_child(__name__)
        changed = False

        log.debug("Checking value validity.")
        if not isinstance(opt, bool):
            raise ValueError()
        else:
            log.debug("Success")

        #log.debug(f"Setting StoreAsFloat to {a}")

        if self.__store_as_float != opt:
            changed = True
            self.__store_as_float = not self.__store_as_float
        if changed:
            if self.__store_as_float:
                self.number = float(self.number)
            else:
                self.number = int(self.number)
        else:
            log.error("Numerical.store_as_float contains the same value as second valve.")


    def __count_noun(
            self,
            noun        : str,
            count       : Optional[Union[int, float]] = None,
            only_noun    = False,
            skip_commify = False,
            capitalize   = False,
            to_words     = False,
            full_stop    = False,
            period       = False,
            round_num    = None,
            as_int       = False
            ):
        """

        An alias for inflect.engine().plural_noun

        Returns the appropriate string for annotating counts of a given noun.

        Parameters:
            full_stop (bool):
                 Include a full-stop punctuation mark at the end of the final statement. Users that
                 are from America may know this punctuation mark better as 'period' (or; '.'. See
                 below for the 'period' parameter alias)
                 (Defaults to bool(False)

            period (bool):
                Include a period mark at the end of the final statement. Users from some areas may
                know this mark better as 'full-stop'

            noun (str):
                Returns a string with the appropriate statement iy,.hy,i for annotating counts of various nouns.

            count (int/float, optional):
                The number of 'noun' that exists.
                (Defaults to 'Numerical.number')

            only_noun (bool, optional):
                Return only the properly pluralized noun.
                (Defaults to False)

            skip_commify (bool, optional):
                (Ignored if either 'only_noun' or 'count_to_words' are True) Return the number as
                part of the statement with commas added to the proper places.
                (Defaults to False)

            to_words (bool, optional):
                (Ignored if 'only_noun' is True) Modify the first part of the statement
                (which contains the count) to words instead of numbers.
                (Defaults to False.)

            capitalize (bool, optional):
                Return the words for the count with the first letter capitalized.
                (Defaults to False, ignored if 'count_to_words' is False.)

            round_num (int, optional):
                Round the number returned to a given precision in decimal digits.
                (Defaults to None(NoneType), ignored if 'only_noun' is True.)
                
            as_int (bool, optional):
                Should number returned be an integer?
                (Defaults to bool(False), ignored if 'to_words' is True)

        Raises:

            ValueError:
                Raised when a value is provided for 'noun' that is not a string.

        """
        # Make sure our noun is a string or raise ValueError
        log = ROOT_ISL_DEVICE.add_child(__name__)
        if not isinstance(noun, str):
            raise ValueError("Noun must be of type: str")
        
        # Make sure 'count' is not 'None' or we can't do anything with it.
        #
        # If 'count' is indeed 'None' we'll use the number that seeded this instance of the
        # 'Numerical' class.
        if count is None:
            count = self.number
        if as_int:
            count = int(count)
        
        # If we received the parameter to round the results, we'll do that.
        if round_num is not None and isinstance(round_num, int):
            count = round(count, round_num)
        
        # Pluralize the noun string
        n_noun = INF.plural_noun(noun, count)
        
        # If the parameter 'to_words' is true, we need to convert the number to words (using the
        # 'to_words' function of this class before we finally concatenate our results.
        if to_words:
            c_count = self.to_words(count)
        else:
            
            # If we did not receive a bool(True) value for the 'skip_commify' parameter we'll
            # send our number off to be commified by self.commify before concatenation
            c_count = self.commify(target_number=count) if not skip_commify else count
        # If the parameter 'only_noun' evaluates to bool(True) the request should not contain
        # the root number in any form.
        statement = n_noun if only_noun else f"{c_count} {n_noun}"
        # If the 'capitalize' parameter evaluates to bool(True) we capitalize the final statement, as
        # one capitalizes a sentence.8h
        if capitalize:
            statement = statement.capitalize()
        
        # If the parameter 'full_stop' evaluates to bool(True) a full-stop (or; 'period' to most of my
        # fellow Americans.
        if full_stop or period:
            statement += "."
        
        # Return the appropriate pluralized (or not) noun based off the number provided
        return statement
    
    
    def to_str(self):
        """

        Return 'self.number' as a string type without modifying it at  all from its original form.

        Returns:
            (int/float): The contents found at 'self.number' but in as a string type.

        """
        return str(self.number)
    
    
    def commify(self, target_number: int = None):
        """

        Return a string containing your number as a string with commas added

        Parameters:
            target_number (int, optional): The number you'd like returned as a commified string. Defaults to
            'Numerical.number'

        Returns:
            str: self.number converted to a string and with appropriately placed commas.

        """
        num = self.number if target_number is None else target_number
        return "{:,}".format(num)
    
    
    def to_words(self, target_num=None):
        """

        An alias to inflect.engine().number_to_words()

        Literally just passes 'target_num' to INF.number_to_words and returns the result of that

        Parameters:
            target_num (int, optional): The number you'd like returned in word-form. Defaults to `Numerical.number`.

        Returns:
            string: A string representing your target number in words.

        Raises:
            NotANumberError: Raised if 'target_num' isn't an integer or a float.

        """
        
        if target_num is None:
            target_num = self.number
        
        if not isinstance(target_num, int) and not isinstance(target_num, float):
            raise ValueError(
                    "The parameter 'target_num' needs to be an integer or a float"
                    )
        
        return INF.number_to_words(str(target_num))
    
    
    def __add__(self, other_num: (int, float), force_return_count: object = False,
                force_return_self: object = False) -> object:
        """

        Return self + other_num.

        Arguments:
            other_num (int|float):
                The number that you wish to add to `num` .

            force_return_count (bool, Optional):
                Return 'count_noun' after getting the sum.

                Optional, defaults to bool(False).

            force_return_self:
                Return the object.

                Optional, defaults to bool(False).

        Note:
            Passing a value of bool(True) (or the evaluated equivalent) to both 'force_return_self' and
            'force_return_count' will result in a 'ValueError' exception being raised.

        Returns:
            float or int

        """
        self.number = self.number + other_num
        
        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number


    def __mul__(self, other, force_return_count=False, force_return_self=False):

        self.number = other if other in [0, 0.0] else self.number * other

        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number

    def __rmul__(self, other, force_return_count=False, force_return_self=False):
        self.number = other if other in [0, 0.0] else other * self.number

        try:
            int(other)
            float(other)
        except ValueError as e:
            raise NUM_ERR.NotANumberError(other) from e

        self.number = other * self.number

        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number

    
    def __rtruediv__(self, principle, force_return_count=False, force_return_self=False):
        if principle == 0 or self.number == 0:
            raise ZeroDivisionError()
        
        self.number = float(principle) / self.number
        
        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
    
    
    def __truediv__(self, divide_by, force_return_count=False, force_return_self=False):
        if divide_by == 0 or self.number == 0:
            raise ZeroDivisionError()
        
        self.number = self.number / float(divide_by)
        
        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
    
    
    def __sub__(self, other, force_return_count=False, force_return_self=False):
        self.number = self.number - float(other)
        if force_return_count and self.__noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
    
    
    def __sqrt__(self) -> Callable[[Optional[ContextManager]], Decimal]:
        return self.dec_num.sqrt

    def __str__(self):
        return self.to_words()


    def __float__(self):
        return float(self.number)

    
    def __repr__(self):
        return self.to_words()
    
    
    def __int__(self):
        return int(self.number)
