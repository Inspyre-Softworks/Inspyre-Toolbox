from inspyre_toolbox.common.about.package import PACKAGE_INFO
from inspyre_toolbox.common.about.pypi import PYPI_VERSION_INFO
from inspyre_toolbox.common.about.version import RELEASE_MAP

AUTHORS   = PACKAGE_INFO['developer']['org']['developers']
PROG_NAME = PACKAGE_INFO['name']['full']
URLS = PACKAGE_INFO['urls']

from inspyre_toolbox.common.about.version import *

_VERSION = VERSION

VERSION   = _VERSION.parse_version()


__all__ = [
        'AUTHORS',
        'PACKAGE_INFO',
        'PROG_NAME',
        'PYPI_VERSION_INFO',
        'URLS',
        'VERSION'
]
