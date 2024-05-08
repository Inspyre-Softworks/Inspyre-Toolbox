"""
Inspyre-Toolbox Generations Module

This module is part of the Inspyre-Toolbox project. It provides functionalities
for generating random decimal numbers within a specified range. The main function
in this module, `generate_random_decimal`, can generate a specified number of
random decimal numbers, each within a given range.

This module can be useful for various applications, such as creating random
datasets for testing, generating noise for simulations, or any other situation
where random decimal numbers are needed.

Function:

generate_random_decimal(number_of_results=1, minimum=0, maximum=1, force_list=False):
Generates a list of random decimal numbers within a specified range.
This module is released under The MIT License.

Project: Inspyre-Toolbox
Author: Inspyre Softworks - https://inspyre.tech
Created: 5/11/2023 @ 7:48 PM
File:
  Name: init.py
  Path: inspyre_toolbox/generations
"""
import random


def generate_random_decimal(number_of_results=1, minimum=0, maximum=1, force_list=False):
    """
    Generates a list of random decimal numbers within a specified range.

    This function generates a list of random decimal numbers, each of which is
    between the specified minimum and maximum values. If only one number is
    requested, the function returns that number directly unless 'force_list'
    is set to True, in which case a list containing that number is returned.

    Arguments:
        number_of_results (int, optional): The number of random numbers to generate.
            (default: 1)
        minimum (float, optional): The lower bound for the random numbers.
            (default: 0)
        maximum (float, optional): The upper bound for the random numbers.
            (default: 1)
        force_list (bool, optional): Whether to always return a list, even when
            only one number is generated. (default: False)

    Returns:
        float or list of float: A list of random decimal numbers. If only one
            number is generated and 'force_list' is False, that number is
            returned directly.
    """
    res = [random.uniform(minimum, maximum) for _ in range(number_of_results)]
    return res[0] if number_of_results == 1 and not force_list else res



"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
