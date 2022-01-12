#  Copyright (c) 2021. Taylor-Jayde Blackstone <t.blackstone@inspyre.tech> https://inspyre.tech
"""

This module contains exceptions for 'InspyreToolbox.proc_man'

"""


class NoFoundProcessesError(Exception):
    """

    Raised when 'InspyreToolbox.proc_man.kill_all_by_name' finds no processes that contain the provided string.

    """

    def __init__(self, *args):
        self.message = args[0] if args else None

    def __str__(self):
        if self.message:
            return 'NoFoundProcessesError, {0} '.format(self.message)
        else:
            return 'NoFoundProcessesError has been raised!'
