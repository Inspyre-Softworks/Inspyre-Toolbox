from inspy_logger import InspyLogger

from inspyre_toolbox.version import parse_version

__VERSION__ = parse_version()

ROOT_LOGGER = InspyLogger('InspyreToolbox')

ROOT_LOGGER.debug(f'Module loaded: log_engine (inspyre_toolbox - v{__VERSION__})')
