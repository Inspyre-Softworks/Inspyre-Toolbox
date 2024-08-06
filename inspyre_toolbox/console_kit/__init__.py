# ==============================================================================
#  Copyright (c) Inspyre Softworks 2022.                                       =
#                                                                              =
#  Author:                 T. Blackstone                                       =
#  Author Email:    <t.blackstone@inspyre.tech>                                =
#  Created:              2/10/22, 9:42 PM                                      =
# ==============================================================================

import os
import random
import sys
from time import sleep

from inspyre_toolbox.log_engine import ROOT_LOGGER as PARENT_LOGGER

MOD_LOGGER = PARENT_LOGGER.get_child('console_kit')


def __get_delay(fast=False):
    possible = list(range(45, 100)) if fast else list(range(100, 301))
    return random.choice(possible) / 1000


def clear_console():
    """

    Clear the current terminal screen.

    Returns
    -------
    None.

    """
    cmd = "cls" if os.name in ("nt", "dos") else "clear"

    os.system(cmd)


def animate_typing(
        message: str,
        interval: float = None,
        skip_pre_newline: bool = False,
        skip_post_newline: bool = False,
        clear_screen: bool = False,
        fast_typer: bool = False,
        override_upper_limit: bool = False,
):
    """

    Animate typing in the terminal/console.

    Args:
        message (str):
            The message you'd like to print through a typing animation.

        interval (Optional(int|float)):
            The time (in number of seconds as an integer) that you'd like to have pass between characters being printed
            to the line. (Defaults to random intervals to more realistically simulate typing.

        skip_pre_newline:
            Don't print a newline before commencing the animation.

        skip_post_newline (Optional(bool)):
            Don't print a newline after we're finished with the typing animation. (Optional)

        clear_screen:

         fast_typer:
        override_upper_limit:

    Returns:
        None

    """
    # If we were instructed to clear the screen, do it.
    if clear_screen:
        clear_console()

    # If we weren't instructed to skip a leading newline, print the newline.
    if not skip_pre_newline:
        print("\n")

    for char in message:
        if interval is None:
            time_between = __get_delay(fast_typer)
        else:
            time_between = interval

            time_between = min(time_between, 0.301)
            if time_between <= 0:
                time_between = __get_delay()

        sleep(time_between)
        sys.stdout.write(char)

    # If we weren't instructed to skip the post-animation newline, print the newline.
    if not skip_post_newline:
        print('\n')
