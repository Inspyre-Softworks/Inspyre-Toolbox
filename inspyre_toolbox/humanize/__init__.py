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

    def count_noun(self, noun:str, count:int=None):
        """

        An alias for inflect.engine().plural_noun

        Returns the appropriate string for annotating counts of a given noun.

        Parameters:
            noun: Returns a string with the appropriate string for annotating counts of various nouns.

        """

        # Populate 'count' with self.number if no value for 'count' was provided on calling.
        if count is None:
            count = int(self.number)
        else:
            count = int(count)

        if not isinstance(noun, str):
            raise ValueError('Noun must be of type: str')

        return INF.plural_noun(noun, count)


    def to_str(self):
        """

        Return 'self.number' as a string type without modifying it at  all from it's original form.

        :return: The contents found at 'self.number' but in as a string type.
        :rtype: TYPE

        """
        return str(self.number)

    def to_words(self):
        if self.number == 0:
            return 'Zero'
        num = self.number
        ans = ""
        i = 0
        while num > 0:
            if num % 1000 != 0:
                ans = self.helper(num %  1000) + NumericalStrings.thousands[i] + " " + ans
                i += 1
                num //= 1000
            return ans.strip()

    def helper(self, n):
        if n == 0:
            return ""
        elif n < 20:
            return NumericalStrings.less_than_20[n] + " "
        elif n < 100:
            return NumericalStrings.tens[n//10] + " " + self.helper(n % 10)
        else:
            return NumericalStrings.less_than_20[n // 100]  + " " + "Hundred " + self.helper(n % 100)
