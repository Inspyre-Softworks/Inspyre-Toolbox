from inspyre_toolbox.common.meta import VERSION as _VERSION, URLS as _URLS, RELEASE_MAP
import requests
from packaging import version as pkg_version
import sys
from rich.table import Table
from rich import print


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


class PyPiVersionInfo:
    """
    A class to represent the version information for this package from PyPi.

    Attributes:
        latest_stable (packaging.version.Version):
            The latest stable version of the package on PyPi.

        latest_pre_release (packaging.version.Version):
            The latest pre-release version of the package.
    Since:
        v1.3.1
    """
    __all_versions: (list[str], None)
    __url = f'{_URLS["pypi_url"]}/json'
    __installed = parse_version()
    __checked_for_update = False
    __newer_available_version = None

    def __init__(self, include_pre_release_for_update_check=False):
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
    def checked_for_update(self):
        return self.__checked_for_update

    @property
    def installed(self):
        """
        Gets the installed version of the package.
        """
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
            response = requests.get(self.__url)
            response.raise_for_status()
            data = response.json()

            self.__all_versions = list(data['releases'].keys())
            self.__latest_stable = data['info']['version']
        except requests.RequestException as e:
            # Handle connection errors, HTTP errors, etc.
            print(f"Error querying PyPi: {e}")

    @property
    def update_available(self):
        """
        Checks if an update is available.
        """
        if self.__newer_available_version is None:
            self.check_for_update()
        return self.__newer_available_version is not None

    def check_for_update(self, include_pre_releases=False):
        latest_version = self.latest_stable

        if include_pre_releases or self.include_pre_release_for_update_check:
            latest_version = max(latest_version, self.latest_pre_release)

        if latest_version > self.installed:
            self.__newer_available_version = latest_version

        self.__checked_for_update = True

        return latest_version > self.installed

    def update(self):
        """
        Checks for updates to inspy-logger.

        Returns:
            None`

        Since:
            v1.3.2
        """

        local_newer_statement = 'Local version is newer than latest version. This is likely a development build.'

        if not self.installed_newer_than_latest:
            local_newer_statement = ''

        try:
            if self.update_available:
                print(f'\n\n[bold green]Update Available![/bold green] New version: '
                      f'[bold cyan]{self.update_available}[/bold cyan]')
            else:
                print(f'\n\n[bold green]No update available.[/bold green] Current version: '
                      f'[bold cyan]{parse_version()}[/bold cyan] {local_newer_statement}')

        except Exception as e:
            print(f'An error occurred during the update check: {str(e)}')

    def print_version_info(self):
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
        table.add_row('Version', parse_version(), )
        table.add_row('Full Version Name', get_full_version_name())

        if self.update_available:
            table.add_row('Update Available', '[bold green]Yes[/bold green]')
            table.add_row('Latest Version', f'{self.new_version_available_num}')

        table.add_row('Python Executable Path', sys.executable)
        table.add_row('Python Version', sys.version)

        print(table)
