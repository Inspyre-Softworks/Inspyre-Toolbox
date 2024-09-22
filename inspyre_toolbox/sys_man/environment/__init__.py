"""
This module contains functions that help determine the environment the program is running in.
"""
from inspyre_toolbox.sys_man import MOD_LOGGER as PARENT_LOGGER, is_windows

MOD_LOGGER = PARENT_LOGGER.get_child('environment')

if is_windows():
    pass
else:
    pass
