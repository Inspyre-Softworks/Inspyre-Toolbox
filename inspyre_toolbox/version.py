from inspyre_toolbox.common.meta import RELEASE_MAP, VERSION as _VERSION
from inspyre_toolbox.ver_man import PyPiVersionInfo


def get_full_version_name():
    """
    Gets the full version name.

    Returns:
        str: The full version name.

    Since:
        v1.3.2
    """
    ver = parse_version()
    ver = ver.split('-')[0]

    release_type = RELEASE_MAP[_VERSION["release"]]
    release_num = _VERSION["release_num"]
    release_str = f" {release_type} {'' if _VERSION['release'].lower() == 'final' else f'({release_num})'}"
    return f'v{ver}{release_str}'


def parse_version() -> str:
    """
    Parses the version information into a string.

    Returns:
        str: The version information.

    Since:
        v1.3.2
    """
    version = f'{_VERSION["major"]}.{_VERSION["minor"]}.{_VERSION["patch"]}'

    if _VERSION['release'] != 'final':
        version += f'-{_VERSION["release"]}.{_VERSION["release_num"]}'

    return version


PYPI_VERSION_INFO = PyPiVersionInfo('inspyre-toolbox')
