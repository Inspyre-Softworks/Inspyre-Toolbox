from inspy_logger import InspyLogger

from inspyre_toolbox.settings import log_level as INSPY_LOG_LEVEL

ROOT_LOGGER = InspyLogger('InspyreToolbox', console_level=INSPY_LOG_LEVEL)

ROOT_LOGGER.debug('Module loaded: log_engine', stack_level=4)
