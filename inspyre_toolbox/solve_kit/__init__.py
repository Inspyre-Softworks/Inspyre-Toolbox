"""
Project: Inspyre-Toolbox
Author: Inspyre Softworks - https://inspyre.tech
Created: 5/11/2023 @ 8:39 PM
File:
  Name: __init__.py
  Filepath: inspyre_toolbox/solve_kit
"""
from statistics import mean

from inspyre_toolbox.conversions.bytes import ByteConverter
from inspyre_toolbox.log_engine import ROOT_LOGGER as PARENT_LOGGER
from inspyre_toolbox.version import parse_version

__VERSION__ = parse_version()

MOD_LOGGER = PARENT_LOGGER.get_child('solve_kit')

MOD_LOGGER.debug(f'Module loaded: solve_kit (inspyre_toolbox - v{__VERSION__})')

DOWNLOAD_SPEED_UNITS = {
        'bps':  {'unit': 'bit', 'factor': 1},
        'kbps': {'unit': 'kilobit', 'factor': pow(10, 3)},
        'mbps': {'unit': 'megabit', 'factor': pow(10, 6)},
        'gbps': {'unit': 'gigabit', 'factor': pow(10, 9)},
        'tbps': {'unit': 'terabit', 'factor': pow(10, 12)},
        'ebps': {'unit': 'exabit', 'factor': pow(10, 15)},
        'zbps': {'unit': 'zettabit', 'factor': pow(10, 18)},
        'ybps': {'unit': 'yottabit', 'factor': pow(10, 21)},
        }


def find_unit(unit: str, case_sensitive=False):
    """
    Find a unit in the DOWNLOAD_SPEED_UNITS dictionary by its unit name or abbreviation.

    Parameters:
        unit (str):
            The unit to find.

    Returns:
        dict:
            The unit data.
    """
    if not case_sensitive:
        unit = unit.lower()

    return next(
            (
                    v
                    for k, v in DOWNLOAD_SPEED_UNITS.items()
                    if k == unit or v['unit'] == unit
                    ),
            None,
            )


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


def download_time(file_size_bytes: int, download_speed: int, download_speed_unit: str = 'bit', return_in_seconds=False):
    bc = ByteConverter(file_size_bytes, 'byte')
    speed_data = find_unit(download_speed_unit.lower())

    if not speed_data:
        raise ValueError(f"Invalid download speed unit: {download_speed_unit}")

    # Convert download speed to bits per second
    download_speed_bps = download_speed * speed_data['factor']

    # Calculate download time in seconds
    download_time_seconds = bc.bytes_to_bits() / download_speed_bps

    if return_in_seconds:
        return download_time_seconds

    # Convert download time to appropriate unit
    time_unit = 'second' if download_time_seconds < 60 else 'minute'
    time_value = download_time_seconds if time_unit == 'second' else download_time_seconds / 60

    return f"{time_value:.2f} {time_unit}"





"""
The MIT License (MIT)
Copyright © 2023 Inspyre Softworks - https://inspyre.tech
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
