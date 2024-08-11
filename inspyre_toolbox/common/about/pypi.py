from inspyre_toolbox.common.about import MOD_LOGGER as PARENT_LOGGER
from inspyre_toolbox.ver_man.classes import PyPiVersionInfo


MOD_LOGGER = PARENT_LOGGER.get_child('pypi')


PYPI_VERSION_INFO = PyPiVersionInfo('inspyre-toolbox')
