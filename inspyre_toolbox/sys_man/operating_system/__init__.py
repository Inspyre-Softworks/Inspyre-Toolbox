from inspyre_toolbox.sys_man import MOD_LOGGER as PARENT_LOGGER
from .checks import is_linux, is_windows

MOD_LOGGER = PARENT_LOGGER.get_child('operating-system')
