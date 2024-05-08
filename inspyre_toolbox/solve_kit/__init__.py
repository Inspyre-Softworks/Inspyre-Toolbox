"""
Project: Inspyre-Toolbox
Author: Inspyre Softworks - https://inspyre.tech
Created: 5/11/2023 @ 8:39 PM
File:
  Name: __init__.py
  Filepath: inspyre_toolbox/solve_kit
"""
from statistics import mean


def how_many_until(current:list, target=.98, iter_limit=pow(10, 10), delay=0):
    global iters

    def _process_():
        global iters
        cur = list(current)
        iters = 0
        while mean(cur) < target and iters < iter_limit:
            cur.append(1)
            iters += 1
        if iters == iter_limit:
            print('Escaping seemingly infinitely recursive loop')
        return iters

    try:
        _process_()
    except KeyboardInterrupt:
        iter_limit = iters





"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
