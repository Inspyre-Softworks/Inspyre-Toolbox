from inspy_logger import InspyLogger
from inspyre_toolbox.common.about.package import PLATFORM_DIRS
from inspyre_toolbox.settings import log_level as INSPY_LOG_LEVEL

DEFAULT_LOG_DIR_PATH = PLATFORM_DIRS.user_log_path()
DEFAULT_LOG_FILE_PATH = DEFAULT_LOG_DIR_PATH.joinpath('inspyre_toolbox.log')

ROOT_LOGGER = InspyLogger('InspyreToolbox', console_level=INSPY_LOG_LEVEL, filename=DEFAULT_LOG_FILE_PATH)

ROOT_LOGGER.debug('Module loaded: log_engine')
