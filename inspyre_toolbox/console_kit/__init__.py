
# ==============================================================================
#  Copyright (c) Inspyre Softworks 2022.                                       =
#                                                                              =
#  Author:                 T. Blackstone                                       =
#  Author Email:    <t.blackstone@inspyre.tech>                                =
#  Created:              2/10/22, 9:42 PM                                      =
# ==============================================================================

from time import sleep
import random
import sys
import os


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
        message:
        interval:
        skip_pre_newline:
        skip_post_newline:
        clear_screen:
        fast_typer:
        override_upper_limit:

    Returns:

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
