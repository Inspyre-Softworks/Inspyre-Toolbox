import re
from typing import Literal

from inspyre_toolbox.ver_man.classes.pypi import PyPiVersionInfo, TestPyPiVersionInfo

RELEASE_MAP = {
    'dev': 'Development Build',
    'alpha': 'Alpha Build',
    'a': 'Alpha Build',
    'beta': 'Beta Build',
    'rc': 'Release Candidate Build',
    'final': 'Final Release Build'
}


class VersionParser:

    RELEASE_MAP = RELEASE_MAP

    def __init__(self, version_str):
        self.__major = None
        self.__minor = None
        self.__patch = None
        self.__release = None
        self.__release_num = None
        self.version_str = version_str
        self.version_info = self.parse_version()

    @property
    def major(self):
        return self.__major

    @property
    def minor(self):
        return self.__minor

    @property
    def patch(self):
        return self.__patch

    @property
    def release(self):
        return self.__release

    @property
    def release_num(self):
        return self.__release_num

    @staticmethod
    def get_release(release_type: Literal[tuple(RELEASE_MAP.keys())]) -> str:
        """
        Gets the release name from the release type.
        """
        if not isinstance(release_type, str):
            raise TypeError(f'Release type must be a string, not {type(release_type)}')

        release_type = release_type.lower()

        if release_type not in VersionParser.RELEASE_MAP:
            raise ValueError(f'Invalid release type: {release_type}. Must be one of '
                             f'{tuple(VersionParser.RELEASE_MAP.keys())}')

        return VersionParser.RELEASE_MAP.get(release_type)

    def parse_version(self):
        """
        Parses the version string and returns the version information.

        Returns:
            dict:
                A dictionary containing the version information.
        """
        match = re.match(r'^(\d+)\.(\d+)(?:\.(\d+))?(?:[-+.]?([a-zA-Z]+)[.\-]?(\d+)?)?$', self.version_str)
        if not match:
            raise ValueError(f"Invalid version format: {self.version_str}")

        major, minor, patch, release_type, release_num = match.groups()
        major, minor = map(int, (major, minor))
        patch = int(patch) if patch else 0
        release_type = release_type or 'final'
        release_num = int(release_num) if release_num else 0

        release = self.RELEASE_MAP.get(release_type, 'Final Release Build')

        self.__major = major
        self.__minor = minor
        self.__patch = patch
        self.__release = release
        self.__release_num = release_num

        return {
            'major': major,
            'minor': minor,
            'patch': patch,
            'release': release,
            'release_abbr': release_type,
            'release_num': release_num
        }

    @property
    def full_version_string(self):
        """
        Returns a formatted full-version string based on the version information.

        Returns:
            str:
                The formatted full-version string.
        """
        major, minor, patch = self.version_info['major'], self.version_info['minor'], self.version_info['patch']
        release, release_num = self.version_info['release'], self.version_info['release_num']

        version_str = f"v{major}.{minor}.{patch}"
        if release not in ('Final Release Build', 'final'):
            version_str += f" {release}"
        if release_num > 0:
            version_str += f" {release_num}"

        return version_str

__all__ = [
    'VersionParser',
    'PyPiVersionInfo',
    'TestPyPiVersionInfo',
    'RELEASE_MAP'
]
