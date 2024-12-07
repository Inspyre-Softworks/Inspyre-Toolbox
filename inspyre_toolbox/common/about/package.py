"""
Package information for Inspyre-Toolbox.

This module contains the package information for Inspyre-Toolbox.

Constants:
    GITHUB_URL (str):
        The URL to the Inspyre-Toolbox GitHub repository.

    PACKAGE_INFO (dict):
        The package information for Inspyre-Toolbox. This includes the name, included CLI entrypoints, URLs, and
        developer information. It has the following structure:

            {
                'name': {
                        'full':    'Inspyre-Toolbox',
                        'library': 'inspyre_toolbox',
                    },

                'included_cli_entrypoints': [
                        'ist-bytes-converter',
                        'ist-add-to-path'
                        ],

                'version': {
                            'semantic': str(VERSION),
                            'full': VERSION.to_full_version_string(),
                            'dict': {
                                        'major':       VERSION.major,
                                        'minor':       VERSION.minor,
                                        'patch':       VERSION.patch,
                                        'release':     VERSION.release,
                                        'release_num': VERSION.release_num
                                    },
                            'on_pypi': PYPI_VERSION_INFO,
                        },

                'urls': {
                        'version_control': {
                                'github': {
                                        'main':     GHU,
                                        'releases': f"{GHU}/releases",
                                        'issues':   f"{GHU}/issues",
                                        'wiki':     f"{GHU}/wiki",
                                        },
                                },
                        'pypi': {
                                'main':     'https://pypi.org/project/inspyre-toolbox',
                                'releases': 'https://pypi.org/project/inspyre-toolbox/#history',
                                },
                        },

                'developer': {
                        'org':  SOFTWARE_ORG,
                        'lead': SOFTWARE_ORG['developers'][0]
                        }
            }

    PYPI_URL (str):
        The URL to the Inspyre-Toolbox PyPi page.

Since:
    v1.6.0
"""
from platformdirs import PlatformDirs

from inspyre_toolbox.common.about.author import SOFTWARE_ORG
from inspyre_toolbox.common.about.pypi import PYPI_VERSION_INFO
from inspyre_toolbox.common.about.version import VERSION

PACKAGE_NAME = 'Inspyre-Toolbox'
GITHUB_URL = f"{SOFTWARE_ORG['urls']['github']}/{PACKAGE_NAME}"
PYPI_URL =   SOFTWARE_ORG['urls']['pypi']

PLATFORM_DIRS = PlatformDirs(appname=PACKAGE_NAME, appauthor=SOFTWARE_ORG['name'])


GHU = GITHUB_URL


PACKAGE_INFO = {

        'name': {
                'full':    'Inspyre-Toolbox',
                'library': 'inspyre_toolbox',
            },

        'version': {
                    'semantic': str(VERSION),
                    'full': VERSION.to_full_version_string(),
                    'dict': {
                                'major':       VERSION.major,
                                'minor':       VERSION.minor,
                                'patch':       VERSION.patch,
                                'release':     VERSION.release,
                                'release_num': VERSION.release_num
                            },
                    'on_pypi': PYPI_VERSION_INFO,
                },

        'included_cli_entrypoints': [
                'ist-bytes-converter',
                'ist-add-to-path'
                ],

        'urls': {
                'version_control': {
                        'github': {
                                'main':     GHU,
                                'releases': f"{GHU}/releases",
                                'issues':   f"{GHU}/issues",
                                'wiki':     f"{GHU}/wiki",
                                },
                        },
                'pypi': {
                        'main':     'https://pypi.org/project/inspyre-toolbox',
                        'releases': 'https://pypi.org/project/inspyre-toolbox/#history',
                        },
                },

        'developer': {
                'org':  SOFTWARE_ORG,
                'lead': SOFTWARE_ORG['developers']['lead']
                }

    }



# Cleanup
del GHU
del SOFTWARE_ORG


__all__ = [
        'GITHUB_URL',
        'PACKAGE_INFO',
    'PLATFORM_DIRS',
        'PYPI_URL'

        ]
