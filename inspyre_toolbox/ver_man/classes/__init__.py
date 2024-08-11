from typing import Literal
import re
import contextlib

from inspyre_toolbox.ver_man.classes.pypi import PyPiVersionInfo


RELEASE_MAP = {
    'dev': 'Development Build',
    'alpha': 'Alpha Build',
    'beta': 'Beta Build',
    'rc': 'Release Candidate Build',
    'final': 'Final Release Build'
}



class VersionParser:

    RELEASE_MAP = RELEASE_MAP

    def __init__(self, version_str):
        self.version_str = version_str
        self.version_info = self.parse_version()

    @staticmethod
    def get_release(release_type: Literal[tuple[RELEASE_MAP.keys()]]) -> str:
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
        parts = self.version_str.split('-')
        version_numbers = parts[0].split('.')
        major, minor, patch = map(int, version_numbers)

        release = 'final'
        release_num = 0
        release_type = 'final'  # Default release type

        if len(parts) > 1:
            release_info = parts[1]
            release_info_parts = re.split(r'[\.\+]', release_info)
            release_type = release_info_parts[0]
            release = self.RELEASE_MAP.get(release_type, 'final')

            if len(release_info_parts) > 1 and release_info_parts[1].isdigit():
                release_num = int(release_info_parts[1])

        return {
            'major': major,
            'minor': minor,
            'patch': patch,
            'release': release,
            'release_abbr': release_type,
            'release_num': release_num
        }

    def to_full_version_string(self):
        """
        Returns a formatted full-version string based on the version information.

        Returns:
            str:
                The formatted full-version string.
        """
        major, minor, patch = self.version_info['major'], self.version_info['minor'], self.version_info['patch']
        release, release_num = self.version_info['release'], self.version_info['release_num']

        version_str = f"v{major}.{minor}.{patch}"
        version_str += (
            f" {release}"
            if release not in ('final', 'Final Release Build')
            else ''
        )
        if release_num > 0:
            version_str += f" {release_num}"

        return version_str

    def print_version(self, skip_rich=False):
        """
        Prints the version information using the specified method.

        Parameters:
            skip_rich (bool):
                If True, skips the rich print method and prints the version information using the default print
                method. Default is False.

        Returns:
            None
        """
        if not skip_rich:
            with contextlib.suppress(ImportError):
                self.__rich__()
                return
        self._print_version()

    def _print_version(self):
        version_info = self.version_info
        print(version_info)

    def __str__(self):
        return self.version_str

    def __repr__(self):
        return f"VersionParser('{self.version_str}\n')"

    def __rich__(self):
        from rich.table import Table
        from rich import box
        table = Table(box=box.SIMPLE)
        table.add_column('Major', justify='right', style='cyan')
        table.add_column('Minor', justify='right', style='magenta')
        table.add_column('Patch', justify='right', style='green')
        table.add_column('Release', justify='right', style='yellow')
        table.add_column('Release Num', justify='right', style='blue')
        table.add_row(str(self.version_info['major']), str(self.version_info['minor']), str(self.version_info['patch']),
                      self.version_info['release'], str(self.version_info['release_num']))
        return table

    @property
    def full_version_string(self):
        """
        Property that returns the formatted full version-string based on the version information.

        Returns:
            str:
                The formatted full-version string.
        """
        return self.to_full_version_string()

    @property
    def major(self):
        """
        Property that returns the major version number.

        Returns:
            int:
                The major version number
        """
        return self.version_info['major']

    @property
    def minor(self):
        """
        Property that returns the minor version number.

        Returns:
            int:
                The minor version number
        """
        return self.version_info['minor']

    @property
    def patch(self):
        """
        Property that returns the patch version number.

        Returns:
            int:
                The patch version number
        """
        return self.version_info['patch']

    @property
    def release(self):
        """
        Property that returns the release type.

        Returns:
            str:
                The release type
        """
        return self.version_info['release']

    @property
    def release_num(self):
        """
        Property that returns the release number.

        Returns:
            int:
                The release number (0 if not specified)
        """
        return self.version_info['release_num']

    # Arithmetic operations
    def __add__(self, other):
        if isinstance(other, VersionParser):
            return VersionParser(f"{self.major + other.major}.{self.minor + other.minor}.{self.patch + other.patch}")
        elif isinstance(other, (int, float)):
            return VersionParser(f"{self.major}.{self.minor}.{self.patch + int(other)}")
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'VersionParser' and '{type(other)}'"
            )

    def __sub__(self, other):
        if isinstance(other, VersionParser):
            return VersionParser(f"{self.major - other.major}.{self.minor - other.minor}.{self.patch - other.patch}")
        elif isinstance(other, (int, float)):
            return VersionParser(f"{self.major}.{self.minor}.{self.patch - int(other)}")
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: 'VersionParser' and '{type(other)}'"
            )

    # Comparison operations
    def __eq__(self, other):
        if isinstance(other, VersionParser):
            return self.version_info == other.version_info
        return False

    def __lt__(self, other):
        if isinstance(other, VersionParser):
            return (
                (self.major, self.minor, self.patch, self.version_info['release_abbr'], self.release_num)
                < (other.major, other.minor, other.patch, other.version_info['release_abbr'], other.release_num)
            )
        return NotImplemented

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if isinstance(other, VersionParser):
            return (
                (self.major, self.minor, self.patch, self.version_info['release_abbr'], self.release_num)
                > (other.major, other.minor, other.patch, other.version_info['release_abbr'], other.release_num)
            )
        return NotImplemented

    def __ge__(self, other):
        return self == other or self > other


__all__ = ['VersionParser', 'PyPiVersionInfo']
