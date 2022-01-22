#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 01:23:36 2021

@author: taylor
"""
from inflect import engine
import typing

from inspyre_toolbox.humanize.errors.numerical import NumericalErrors

# Instantiate inflect.engine as 'INF'
INF = engine()

NUM_ERR = NumericalErrors()


class NumericalStrings(object):
    """

    Number statement string fragments

    Attributes:
        less_than_20 (list): A list of strings each representing a number from 0 (or "") to 19 (or Nineteen).
        tens (list): A list of strings each representing a 'tens' place with all strings below ten being represented
        by "" and with the final element being "Ninety"
        thousands (list): A list of strings each representing a 'thousands' place with all strings below a thousand
        being represented by "" and with the final element being "Billion"
    """

    less_than_20 = [
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
    tens = [
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
    thousands = ["", "Thousand", "Million", "Billion"]


class Numerical(object):
    """

    A class that allows you to manipulate numbers with greater-flexibility.

    """
    
    def __add__(self, other_num, force_return_count=False, force_return_self=False):
        self.number = self.number + other_num

        if force_return_count and self.noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
        
    def __mul__(self, multiplied_by, force_return_count=False, force_return_self=False):
        self.number = self.number * float(multiplied_by)

        if force_return_count and self.noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
    
    def __rtruediv__(self, principle, force_return_count=False, force_return_self=False):
        if principle == 0 or self.number == 0 :
            raise ZeroDivisionError()

        self.number = float(principle) / self.number

        if force_return_count and self.noun is None:
            raise ValueError()
        if force_return_count :
            return self.count_noun()
        elif force_return_self :
            return self
        else :
            return self.number
    
    def __truediv__(self, divide_by, force_return_count=False, force_return_self=False):
        if divide_by == 0 or self.number == 0:
            raise ZeroDivisionError()

        self.number = self.number / float(divide_by)

        if force_return_count and self.noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
            
    def __sub__(self, other, force_return_count=False, force_return_self=False):
        self.number = self.number - float(other)

        if force_return_count and self.noun is None:
            raise ValueError()
        if force_return_count:
            return self.count_noun()
        elif force_return_self:
            return self
        else:
            return self.number
    
    
    def __init__(self, number, noun=None, store_as_float=True):
        """

        Create a new instance, with a new number to manipulate

        Args:
            number (int|float): The subject number.
            noun: The noun to count.
        """
        # First, check whether 'number' is an integer or a float or not. If not; we raise an error
        
        self.store_as_float = store_as_float
        
        if not isinstance(number, float) and store_as_float:
            try:
                number = int(number)
            except ValueError as e:
                raise NUM_ERR.NotANumberError(
                    var=number,
                    var_name="number",
                    msg=f"Type {type(number)} is not valid. Must be {type(1)} or {type(1.1)}",
                )
            
            if store_as_float:
                number = float(number)

        self.number = number

        self.num_commified = self.commify(self.number)
        self.noun = noun

    def count_noun(
            self,
            number = None,
            noun: str = None,
            save_number: bool = True,
            save_noun: bool = True,

            **kwargs):
        """
        
        Args:
            number (Optional, (int|float)):
                The number of nouns there are. Defaults to 'self.number'.
            
            noun (Optional, str):
                The thing you want to describe the number of. Defaults to 'self.noun'.
            
            save_number (Optional, bool):
                If you provided a value for the 'number' parameter this parameter's value will indicate whether the
                value of 'number' should replace 'self.number'. Defaults to bool(True).
            
            save_noun (Optional, bool):
                If you provided a value for the 'noun' parameter and self.noun isn't NoneType and differs from the
                provided value 'save_noun' will indicate whether the new value for 'noun' should replace 'self.noun'. Defaults to bool(True).
            
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

        number_changed = False
        noun_changed = False
        number_previous = None
        noun_previous = None

        if number is not None:
            try:
                number = float(number)
            except ValueError:

                warning = "If passing a noun alone to 'count_noun' you need to include the parameter name\n"\
                      "For example:\n"\
                      "\n"\
                      "number.count_noun(noun='banana')\n"\
                      "NOT\n"\
                      "number.count_noun('banana')"

                print(warning)

                raise ValueError(warning)

            if number != self.number:
                if not save_number:

                    number_changed = True
                    number_previous = self.number

                self.number = number


        if noun is not None:

            noun = str(noun)
            try:
                noun = str(noun)
                if self.noun is not None and noun != self.noun:
                    if not save_noun:
                        noun_changed = True
                        noun_previous = self.noun

                    self.noun = noun
            except:
                raise ValueError(f"'noun' should be {type(str())} not {type(noun)}")



        ret = self.__count_noun(noun=self.noun, **kwargs)

        if number_changed:
            self.number = number_previous
            number_previous = None
            number_changed = False
        if noun_changed:
            self.noun = noun_previous
            noun_previous = None
            noun_changed = None

        return ret

    def __count_noun(
        self,
        noun: str,
        count: int = None,
        only_noun=False,
        skip_commify=False,
        to_words=False,
        capitalize=False,
        full_stop=False,
        period=False,
        round_num=None
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

        Raises:

            ValueError: Raised when a value is provided for 'noun' that is not a string.

        """

        # Make sure our noun is a string or raise ValueError
        if not isinstance(noun, str):
            raise ValueError("Noun must be of type: str")

        # Make sure 'count' is not 'None' or we can't do anything with it.
        #
        # If 'count' is indeed 'None' we'll use the number that seeded this instance of the
        # 'Numerical' class.
        if count is None:
            count = self.number

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

        # Return the appropriate pluaralized (or not) noun based off the number provided
        return statement

    def to_str(self):
        """

        Return 'self.number' as a string type without modifying it at  all from it's original form.

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
            target_num (int, optional): The number you'd like returned in word-form. Defaults to 'Numerical.number'.

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

        return INF.number_to_words(target_num)

    def __repr__(self):
        return self.to_words()
