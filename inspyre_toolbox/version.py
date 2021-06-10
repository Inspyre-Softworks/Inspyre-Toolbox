from pkgutil import get_data
from configparser import ConfigParser

from inspyred_print import Color, Format

from inspyre_toolbox.pypi.packages import up_to_date

_color = Color()
_format = Format()
_red = _color.red
_end = _format.end_mod

__ver_parser = ConfigParser()
__ver = get_data('inspyre_toolbox', 'VERSION').decode('UTF8')
__ver_parser.read_string(__ver)

class Version(object):

    def _check_most_current(self):
        res = up_to_date('inspy_logger')

        self.is_latest = res

        return res

    def __init__(self, version_info):
        self.info = version_info['VERSION']
        self.number = self.info['number']
        self.pre_release = self.info.get_boolean('pre-release')

        if self.pre_release:
            self.pr_info = version_info['PRE-RELEASE']
            self.pr_type = self.pr_info['type']
            self.pr_num = self.pr_info['build_no']
            if self.pr_type.lower() == 'alpha':
                prt_tag = 'a'
            elif self.pr_type.lower() == 'beta':
                prt_tag = 'b'
            self.pr_tag = str(f"{prt_tag}{self.pr_num}")
        else:
            self.pr_info = None
            self.pr_type = None
            self.pr_num = None
            self.pr_tag = ""

        self.full = str(f"{self.number}{self.pr_tag}")
        self.is_latest = None
        self._check_most_current()

VERSION = Version(__ver)
UPDATE_PENDING = not VERSION.is_latest
