__all__ = [
    'AUTHORS',
    'RELEASE_MAP',
    'URLS',
    'VERSION'
]


URLS = dict(
    developer_url='https://inspyre.tech',
    docs_url='https://inspyre-toolbox.readthedocs.io/en/latest',
    github_url='https://github.com/tayjaybabee/Inspyre-Toolbox',
    pypi_url='https://pypi.org/project/inspyre-toolbox',
)
"""The URLs used in the project."""


AUTHORS = [
    ('Inspyre-Softworks', URLS['developer_url']),
    ('Taylor-Jayde Blackstone', '<t.blackstone@inspyre.tech>')
]
"""The authors of the project."""


RELEASE_MAP = {
    'dev': 'Development Build',
    'alpha': 'Alpha Build',
    'beta': 'Beta Build',
    'rc': 'Release Candidate Build',
    'final': 'Final Release Build'
}
"""The release map for the project."""


VERSION = {
    'major': 1,
    'minor': 4,
    'patch': 0,
    'release': 'final',
    'release_num': 0
}
"""The version information for the project."""
