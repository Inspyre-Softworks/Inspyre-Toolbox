"""


Author: 
    Inspyre Softworks

Project:
    Inspyre-Toolbox

File: 
    inspyre_toolbox/ver_man/classes/pypi/helpers.py
 

Description:
"""
from inspyre_toolbox.ver_man.classes.pypi.errors import PyPiPackageNotFoundError

DOUBLE_FAIL_MSG_1 = 'Unable to find '
DOUBLE_FAIL_MSG_2 = ' on either PyPi or TestPyPi. Please check the package name and try again.'


def load_pypi_version_info(package_name, include_pre_releases_in_update_check=False, skip_test_pypi_on_fail=False):
    """
    Loads the PyPi version info for a package.

    Parameters:
        package_name (str):
            The name of the package.

        include_pre_releases_in_update_check (bool, optional):
            If True, includes pre-releases in the update check. Defaults to False.

        skip_test_pypi_on_fail (bool, optional):
            If True, skips the test PyPi on failure. Defaults to False.

    Returns:
        PyPiVersionInfo:
            The PyPi version info.

    Since:
        v1.6.0

    Example Usage:
        >>> from inspyre_toolbox.ver_man.classes.pypi.helpers import load_pypi_version_info
        >>> pypi_version_info = load_pypi_version_info('inspyre-toolbox')
        >>> print(pypi_version_info)
        PyPiVersionInfo('inspyre-toolbox')

        >>> pypi_version_info = load_pypi_version_info('some-dev-package')
        >>> print(pypi_version_info)
        TestPyPiVersionInfo('some-dev-package')
    """
    pypi = None
    from inspyre_toolbox.ver_man.classes.pypi import PyPiVersionInfo, TestPyPiVersionInfo

    final_err_msg = f'{DOUBLE_FAIL_MSG_1}"{package_name}"{DOUBLE_FAIL_MSG_2}'

    try:
        pypi = PyPiVersionInfo(package_name, include_pre_release_for_update_check=include_pre_releases_in_update_check)
    except PyPiPackageNotFoundError as e:
        print('PyPi package not found. Trying TestPyPi...')
        if not skip_test_pypi_on_fail:
            try:
                pypi = TestPyPiVersionInfo(package_name,
                                           include_pre_release_for_update_check=include_pre_releases_in_update_check)
            except PyPiPackageNotFoundError as e:
                raise PyPiPackageNotFoundError(message=final_err_msg) from e

    return pypi
