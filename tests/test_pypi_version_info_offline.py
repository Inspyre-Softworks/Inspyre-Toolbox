"""
Tests for PyPiVersionInfo offline (no-internet) behavior.
"""
import requests
import pytest
from unittest.mock import patch

from inspyre_toolbox.ver_man.classes.pypi import PyPiVersionInfo

_PATCH_TARGET = 'inspyre_toolbox.ver_man.classes.pypi.requests.get'


@pytest.fixture
def offline_version_info(capsys):
    """Create a PyPiVersionInfo instance that simulates an offline environment."""
    with patch(_PATCH_TARGET, side_effect=requests.ConnectionError('Network unreachable')):
        instance = PyPiVersionInfo('some-package')
    return instance, capsys


def test_offline_does_not_raise(capsys):
    """PyPiVersionInfo.__init__ must not raise when a ConnectionError occurs."""
    with patch(_PATCH_TARGET, side_effect=requests.ConnectionError('Network unreachable')):
        instance = PyPiVersionInfo('some-package')
    assert instance is not None


def test_offline_prints_exception(capsys):
    """The connection error message should be printed to stdout."""
    with patch(_PATCH_TARGET, side_effect=requests.ConnectionError('Network unreachable')):
        PyPiVersionInfo('some-package')
    captured = capsys.readouterr()
    assert 'Network unreachable' in captured.out


def test_offline_all_versions_empty(offline_version_info):
    """all_versions should return an empty list when offline."""
    instance, _ = offline_version_info
    assert instance.all_versions == []


def test_offline_latest_stable_none(offline_version_info):
    """latest_stable should return None when offline."""
    instance, _ = offline_version_info
    assert instance.latest_stable is None


def test_offline_latest_pre_release_none(offline_version_info):
    """latest_pre_release should return None when offline."""
    instance, _ = offline_version_info
    assert instance.latest_pre_release is None
