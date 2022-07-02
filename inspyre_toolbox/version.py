from configparser import ConfigParser
from pkgutil import get_data

from inspyred_print import Color, Format

from inspyre_toolbox.core.errors.version import \
    VersionInfoMismatchError, \
    InvalidPreReleaseTypeError
from inspyre_toolbox.pypi.packages import up_to_date


_color = Color()
_format = Format()
_red = _color.red
_end = _format.end_mod

__ver_parser = ConfigParser()
__ver = get_data('inspyre_toolbox', 'VERSION').decode('UTF8')
__ver_parser.read_string(__ver)

# Since v1.3.1:
PRE_RELEASE_TYPES = {
                    'dev': {
                            'tag': 'dev',
                            'full': 'Development',
                            'order': 0
                    },
                    'alpha': {
                            'tag': 'a',
                            'full': 'Alpha',
                            'order': 1
                    },
                    'beta': {
                            'tag': 'b',
                            'full': 'Beta',
                            'order': 2
                    },
                    'rc': {
                            'tag': 'rc',
                            'full': 'Release Candidate',
                            'order': 3
                    }
            }

class Version(object):

    def _check_most_current(self):
        """
        The _check_most_current function checks whether the most recent
        version of inspyre_toolbox is installed. If it is not, then the function returns
         False and a warning message will be printed to stdout.
        Otherwise, it returns True

        Args:
            self: Access attributes of the class within methods

        Returns:
            A boolean value
        """
        res = up_to_date('inspyre_toolbox')

        self.is_latest = res

        return res

    def __init__(self, version_info):
        self.info = version_info['VERSION']
        self.number = self.info['number']

        # Since v1.3.1:
        # Created new attributes for a breakdown of the version number.
        self.major = self.info['major']
        self.minor = self.info['minor']
        self.patch = self.info['patch']

        self.concatenated = f"{self.major}.{self.minor}.{self.patch}"

        if self.concatenated != self.number:
            raise VersionInfoMismatchError(
                f"The version number in the VERSION file ({self.concatenated}) "
                f"does not match the full version number in the VERSION file "
                f"({self.number})")

        self.pre_release = version_info.getboolean('VERSION', 'pre-release')

        if self.pre_release:
            self.pr_info = version_info['PRE-RELEASE']
            self.pr_type = self.pr_info['type']
            self.pr_num = self.pr_info['build-no']

            prt_tag = None
            prt_full = None

            if self.pr_type not in PRE_RELEASE_TYPES:
                raise InvalidPreReleaseTypeError(pr_type=self.pr_type)

            prt_tag = PRE_RELEASE_TYPES[self.pr_type]['tag']
            prt_full = PRE_RELEASE_TYPES[self.pr_type]['full']

            self.pr_tag = str(f"{prt_tag}{self.pr_num}")
            self.pr_full = str(f"{prt_full} Build {self.pr_num}")
        else:
            self.pr_info = None
            self.pr_type = None
            self.pr_num = None
            self.pr_tag = ""

        self.full = str(f"v{self.number} ({self.pr_full})")
        self.full_tagged = str(f"v{self.number}-{self.pr_tag}")

        self.is_latest = None
        self._check_most_current()

    def __repr__(self) -> str:
        """
        The __repr__ function returns a string representation of the class.
        """
        _repr = f"Major: {self.major}\nMinor: {self.minor}\nPatch: {self.patch}"

        if self.pre_release:
            _repr += f"\nPre-Release: {self.pr_type}\nBuild: {self.pr_num}"

        return _repr

    def __str__(self) -> str:
        """
        The __str__ function returns a string representation of the class.
        """
        return self.full


VERSION = Version(__ver_parser)
FULL = VERSION.full_tagged
VERBOSE = VERSION.full
UPDATE_PENDING = not VERSION.is_latest
