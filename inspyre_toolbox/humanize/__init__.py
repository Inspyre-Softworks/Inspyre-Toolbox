#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 01:23:36 2021

@author: taylor
"""
from inflect import engine

# Instantiate inflect.engine as 'INF'
INF = engine()

class NotANumberError(Exception):
    def __init__(self, var, var_name:str=None, msg:str=None, skip_print:bool=False, redirect_print=None):
        """

        Raised when a parameter is provided that is not an integer or a float where one was expectecd.

        Args:
            var (Any): The variable which triggered the raising of this exception.
            var_name (str, optional): The name of the variable that was passed to raise this exception. Defaults to None.
            msg (str, optional): The message you'd like the end-user to see upon raising. Defaults to None.
            skip_print (bool, optional): Should we skip printing the message on initialization. Defaults to False.
            redirect_print (any output, optional): An object to redirect our printing to. Ignored if 'skip_print' is True. Defaults to None.


        Returns:
            None.

        """

        if var_name is None:
            msg1 = "The variable provided is neither an integer or a float. One or the other is needed."
        else:
            var_type = type(var)
            msg1 = f"{var_name} has a value of {var} and is of type {var_type}. An integer or float was needed."

        if msg is None:
            msg = msg1
        else:
            msg = msg1 + ' ' + msg

        self.msg = msg
        self.message = self.msg

        if not skip_print:
            if redirect_print:
                redirect_print(self.message)
            else:
                print(self.message)



class NumericalStrings(object):
    """

    Number statement string fragments

    Attributes:
        less_than_20 (list): A list of strings each representing a number from 0 (or "") to 19 (or Nineteen).
        tens (list): A list of strings each representing a 'tens' place with all strings below ten being represented by "" and with the final element being "Ninety"
        thousands (list): A list of strings each representing a 'thousands' place with all strings below a thousand being represented by "" and with the final element being "Billion"
    """
    less_than_20 = ["", "One", "Two", "Three", "Four", "Five", "Six",
"Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve", "Thirteen",
"Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen",
"Nineteen"]
    tens = ["","Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty",
"Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Million", "Billion"]


class Numerical:
    def __init__(self, number):
        self.number = number
        self.num_commified = self.commify(self.number)

    def count_noun(self,
                   noun:str,
                   count:int=None,
                   only_noun=False,
                   skip_commify=False,
                   count_to_words=False,
                   capitalize=False,
                   period=False,
                   round_num=None):
        """

        An alias for inflect.engine().plural_noun

        Returns the appropriate string for annotating counts of a given noun.

        Parameters:
            noun (str): Returns a string with the appropriate string for annotating counts of various nouns.
            count (int/float, optional): The number of 'noun' that exists. Defaults to 'Numerical.number'
            only_noun (bool, optional): Return only the properly pluralized noun. Defaults to False.
            skip_commify (bool, optional): (Ignored if either 'only_noun' or 'count_to_words' are True) Return the number as part of the statement with commas added to the proper places. Defaults to False.
            count_to_words (bool, optional): (Ignored if 'only_noun' is True) Modify the first part of the statement (which contains the count) to words instead of numbers. Defaults to False.
            capitalize (bool, optional): Return the words for the count with the first letter capitalized. Defaults to False, ignored if 'count_to_words' is False.
            round_num (int, optional): Round the number returned to a given precision in decimal digits. Defaults to None, ignored if 'only_noun' is True.

        Raises:
            ValueError: Raised when a value is provided for 'noun' that is not a string.

        """

        # Make sure our noun is a string or raise ValueError
        if not isinstance(noun, str):
            raise ValueError('Noun must be of type: str')

        if count is None:
            count = self.number

        if round_num is not None and isinstance(round_num, int):
            count = round(count, round_num)

        n_noun = INF.plural_noun(noun, count)
        if count_to_words:
            c_count = self.to_words(count)
        else:
            if not skip_commify:
                c_count = self.commify(target_number=count)
            else:
                c_count = count

        statement = f"{c_count} {n_noun}"

        if capitalize:
            statement = statement.capitalize()

        # Return the appropriate pluaralized (or not) noun based off the number provided
        return statement

    def to_str(self):
        """

        Return 'self.number' as a string type without modifying it at  all from it's original form.

        Returns:
            (int/float): The contents found at 'self.number' but in as a string type.

        """
        return str(self.number)

    def commify(self, target_number:int=None):
        """

        Return a string containing your number as a string with commas added

        Parameters:
            target_number (int, optional): The number you'd like returned as a commified string. Defaults to 'Numerical.number'

        Returns:
            str: self.number converted to a string and with appropriately placed commas.

        """
        if target_number is None:
            num = self.number
        else:
            num = target_number
        res = "{:,}".format(num)

        return res

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
            raise ValueError("The parameter 'target_num' needs to be an integer or a float")

        return INF.number_to_words(target_num)
