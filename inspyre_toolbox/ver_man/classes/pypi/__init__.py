import sys

import requests
from packaging import version as pkg_version
from rich.console import Console
from rich.table import Table

from inspyre_toolbox.ver_man.classes.pypi.errors import PyPiPackageNotFoundError
from inspyre_toolbox.ver_man.classes.pypi.helpers import load_pypi_version_info

CONSOLE = Console()

BASE_URL = 'https://pypi.org/pypi/'
TEST_PYPI_BASE_URL = 'https://test.pypi.org/pypi/'


class PyPiVersionInfo:
    """
    A class to represent the version information for a package from PyPi.

    Attributes:
        package_name (str):
            The name of the package on PyPi.
        latest_stable (packaging.version.Version):
            The latest stable version of the package on PyPi.
        latest_pre_release (packaging.version.Version):
            The latest pre-release version of the package.
    Since:
        v1.6.0
    """

    def __init__(self, package_name, include_pre_release_for_update_check=False):
        """
        Initialize the PyPiVersionInfo object.

        Args:
            package_name:
            include_pre_release_for_update_check:
        """
        self.package_name = package_name
        if not hasattr(self, '_url'):
            self._url = f'{BASE_URL}{self.package_name}/json'
        self.__installed = self.get_installed_version()
        self.__checked_for_update = False
        self.__newer_available_version = None
        self.__latest_stable = None
        self.__latest_pre_release = None
        self.__all_versions = None
        self.include_pre_release_for_update_check = include_pre_release_for_update_check
        self.__query_versions()

    @property
    def all_versions(self):
        if self.__all_versions is None:
            self.__query_versions()
        return sorted([pkg_version.parse(v) for v in self.__all_versions])

    @property
    def all_stable_versions(self):
        return [v for v in self.all_versions if not v.is_prerelease]

    @property
    def checked_for_update(self):
        return self.__checked_for_update

    def get_installed_version(self):
        """
        Gets the installed version of the package.
        This method should be implemented to get the installed version of the package.
        For example, it can use importlib.metadata or pkg_resources to find the installed version.
        """
        import importlib.metadata

        try:
            return importlib.metadata.version(self.package_name)
        except importlib.metadata.PackageNotFoundError:
            return None

    @property
    def installed(self):
        """
        Gets the installed version of the package.
        """
        if self.__installed is None:
            return None
        return pkg_version.parse(self.__installed)

    @property
    def installed_newer_than_latest(self):
        return self.installed > self.latest

    @property
    def latest(self):
        return (
                self.all_versions[-1]
                if self.include_pre_release_for_update_check
                else self.latest_stable
        )

    @property
    def latest_stable(self):
        """
        Gets the latest stable version of the package on PyPi.
        """
        if self.__latest_stable is None:
            self.__query_versions()
        return pkg_version.parse(self.__latest_stable)

    @property
    def latest_pre_release(self):
        """
        Gets the latest pre-release version of the package.
        """
        if self.__all_versions is None:
            self.__query_versions()
        pre_release_versions = [v for v in self.all_versions if v.is_prerelease]
        return pre_release_versions[-1] if pre_release_versions else None

    @property
    def newer_available_version(self):
        if self.__newer_available_version is None:
            self.check_for_update()

        return self.__newer_available_version

    def __query_versions(self):
        """
        Queries the versions from PyPi.
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            data = response.json()

            self.__all_versions = list(data['releases'].keys())
            self.__latest_stable = data['info']['version']
        except requests.RequestException as e:
            raise PyPiPackageNotFoundError(
                message='Package not found on PyPi.',
                skip_print=self.__class__.__name__ == 'TestPyPiVersionInfo',
            ) from e

    @property
    def update_available(self):
        """
        Checks if an update is available.
        """
        if self.__newer_available_version is None and self.installed:
            self.check_for_update()
        elif not self.installed:
            return False
        return self.__newer_available_version is not None
    
    @property
    def url(self):
        return self._url

    def check_for_update(self, include_pre_releases=False):
        latest_version = self.latest_stable

        if include_pre_releases or self.include_pre_release_for_update_check:
            latest_version = max(latest_version, self.latest_pre_release)

        if latest_version > self.installed:
            self.__newer_available_version = latest_version

        self.__checked_for_update = True

        return latest_version > self.installed

    def get_all_versions(self, exclude_pre_releases=False, excluded_versions=None, before_version=None,
                         after_version=None):
        """
        Get all versions of the package.

        Args:
            exclude_pre_releases (bool, optional):
                Whether to exclude pre-releases. Defaults to False.

            excluded_versions (list, optional):
                A list of versions to exclude. Defaults to None.

            before_version (str, optional):
                A version string to only include versions before this version. Defaults to None.

            after_version (str, optional):
                A version string to only include versions after this version. Defaults to None.

        Returns:
            list:
                A list of versions of the package.
        """
        versions = self.all_versions

        if exclude_pre_releases:
            versions = [v for v in versions if not v.is_prerelease]

        if excluded_versions:
            excluded_versions = [pkg_version.parse(v) for v in excluded_versions]
            versions = [v for v in versions if v not in excluded_versions]

        if before_version:
            versions = [v for v in versions if v < pkg_version.parse(before_version)]

        if after_version:
            versions = [v for v in versions if v > pkg_version.parse(after_version)]

        return versions

    def get_version_info(self, version):
        """
        Get information about a specific version of the package.

        Args:
            version (str):
                The version string for which to get information.

        Returns:
            dict:
                A dictionary containing information about the version.
        """
        try:
            url = ''.join([f'{part}/' for part in self.url.split('/')[:-1]])[:-1]
            response = requests.get(f'{url}/{version}/json')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise PyPiPackageNotFoundError(
                message='Package not found on PyPi.',
                skip_print=self.__class__.__name__ == 'TestPyPiVersionInfo',
            ) from e

    def update(self):
        """
        Checks for updates to the package.

        Returns:
            None

        """
        local_newer_statement = 'Local version is newer than latest version. This is likely a development build.'
        console_print = CONSOLE.print

        if not self.installed_newer_than_latest:
            local_newer_statement = ''

        try:
            if self.update_available:
                console_print(f'\n\n[bold green]Update Available![/bold green] New version: '
                      f'[bold cyan]{self.newer_available_version}[/bold cyan]')
            else:
                console_print(f'\n\n[bold green]No update available.[/bold green] Current version: '
                      f'[bold cyan]{self.installed}[/bold cyan] {local_newer_statement}')

        except Exception as e:
            console_print(f'An error occurred during the update check: {str(e)}')

    def print_version_info(self, args):
        """
        Print version information in a formatted table.

        This function creates a table using the `Table` class and populates it with version information about the current Python environment. It then prints the table to the console.

        Parameters:
            self: The current instance of the class.

        Returns:
            None
        """

        # Create a table

        table = Table(show_header=False, show_lines=True, expand=True, border_style='bright_blue',
                      row_styles=['none', 'dim'])

        # Add columns
        table.add_column('Property', style='cyan', width=20)
        table.add_column('Value', justify='center')

        # Add rows
        table.add_row('Package Name', self.package_name)

        installed_version = str(self.installed) if self.installed else "[bold red]Not installed[/bold red]"

        table.add_row('Installed Version', installed_version)
        table.add_row('Latest Stable Version', str(self.latest_stable))
        table.add_row('Latest Pre-release Version', str(self.latest_pre_release))

        if self.update_available:
            table.add_row('Update Available', '[bold green]Yes[/bold green]')
            table.add_row('Latest Version', str(self.newer_available_version))

        table.add_row('Python Executable Path', sys.executable)
        table.add_row('Python Version', sys.version)

        CONSOLE.print(table)


class TestPyPiVersionInfo(PyPiVersionInfo):
    """
    A class to query information from test.pypi.org.
    """
    def __init__(self, package_name, include_pre_release_for_update_check=False):
        self.package_name = package_name
        self._url = f'{TEST_PYPI_BASE_URL}{self.package_name}/json'

        super().__init__(package_name, include_pre_release_for_update_check)


__all__ = [
    'PyPiVersionInfo',
    'TestPyPiVersionInfo',
    'load_pypi_version_info'
]
