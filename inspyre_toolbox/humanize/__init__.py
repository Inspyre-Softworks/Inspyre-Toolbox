#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 01:23:36 2021

@author: taylor
"""
from inflect import engine

# Instantiate inflect.engine as 'INF'
INF = engine()

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

    def count_noun(self, noun:str, count:int=self.number):
        """

        An alias for inflect.engine().plural_noun

        Returns the appropriate string for annotating counts of a given noun.

        Parameters:
            noun: Returns a string with the appropriate string for annotating counts of various nouns.

        Raises:
            ValueError: Raised when a value is provided for 'noun' that is not a string.

        """

        # Make sure our noun is a string or raise ValueError
        if not isinstance(noun, str):
            raise ValueError('Noun must be of type: str')

        # Return the appropriate pluaralized (or not) noun based off the number provided
        return INF.plural_noun(noun, count)

    def to_str(self):
        """

        Return 'self.number' as a string type without modifying it at  all from it's original form.

        :return: The contents found at 'self.number' but in as a string type.
        :rtype: TYPE

        """
        return str(self.number)

    def commify(self, target_number:int=self.number):
        """

        Return a string containing your number as a string with commas added

        Parameters:
            target_number (int): (Optional) The number you'd like returned as a commified string. (Default: self.number)'

        Returns:
            str: self.number converted to a string and with appropriately placed commas.

        """
        num = self.number
        res = "{:,}".format(num)

        return res

    def to_words(self, target_num=self.number):
        """

        An alias to inflect.engine().number_to_words()

        Literally just passes 'target_num' to INF.number_to_words and returns the result of that

        Parameters:
            target_num (int): (Optional, Default: self.number) The number you'd like returned in word-form'

        Returns:
            string: A string representing your target number in words.

        Raises:
            ValueError: Raised if 'target_num' isn't an integer or a float.

        """
        if not isinstance(target_num, str) and not isinstance(target_num, float):
            raise ValueError("The parameter 'target_num' needs to be an integer or a float")

        return INF.number_to_words(target_num)
