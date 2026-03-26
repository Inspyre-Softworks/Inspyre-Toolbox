"""
Tests for PyPiVersionInfo offline (no-internet) behavior.
"""
import requests
import pytest
from unittest.mock import patch

from inspyre_toolbox.ver_man.classes.pypi import PyPiVersionInfo

_PATCH_TARGET = 'inspyre_toolbox.ver_man.classes.pypi.requests.get'
_CONSOLE_TARGET = 'inspyre_toolbox.ver_man.classes.pypi.CONSOLE'


def _make_offline_instance():
    with patch(_PATCH_TARGET, side_effect=requests.ConnectionError('Network unreachable')):
        return PyPiVersionInfo('some-package')


@pytest.fixture
def offline_version_info():
    """Create a PyPiVersionInfo instance that simulates an offline environment."""
    return _make_offline_instance()


# ---------------------------------------------------------------------------
# Offline construction
# ---------------------------------------------------------------------------

def test_offline_does_not_raise():
    """PyPiVersionInfo.__init__ must not raise when a ConnectionError occurs."""
    instance = _make_offline_instance()
    assert instance is not None


def test_offline_prints_exception():
    """A descriptive message should be output when a connection error occurs."""
    with patch(_CONSOLE_TARGET) as mock_console, \
         patch(_PATCH_TARGET, side_effect=requests.ConnectionError('Network unreachable')):
        PyPiVersionInfo('some-package')
    args, _ = mock_console.print.call_args
    assert 'Network unreachable' in args[0]


# ---------------------------------------------------------------------------
# Offline property behaviour
# ---------------------------------------------------------------------------

def test_offline_all_versions_empty(offline_version_info):
    """all_versions should return an empty list when offline."""
    assert offline_version_info.all_versions == []


def test_offline_latest_stable_none(offline_version_info):
    """latest_stable should return None when offline."""
    assert offline_version_info.latest_stable is None


def test_offline_latest_pre_release_none(offline_version_info):
    """latest_pre_release should return None when offline."""
    assert offline_version_info.latest_pre_release is None


def test_offline_latest_none(offline_version_info):
    """latest should return None when offline (no version data available)."""
    assert offline_version_info.latest is None


def test_offline_installed_newer_than_latest_false(offline_version_info):
    """installed_newer_than_latest must return False when latest is None."""
    assert offline_version_info.installed_newer_than_latest is False


def test_offline_check_for_update_returns_false(offline_version_info):
    """check_for_update must return False gracefully when offline."""
    assert offline_version_info.check_for_update() is False


def test_offline_newer_available_version_none(offline_version_info):
    """newer_available_version must be None when offline."""
    assert offline_version_info.newer_available_version is None


# ---------------------------------------------------------------------------
# print_version_info signature fix
# ---------------------------------------------------------------------------

def test_print_version_info_no_args_required(offline_version_info):
    """print_version_info() must be callable with no arguments."""
    offline_version_info.print_version_info()


def test_print_version_info_with_args(offline_version_info):
    """print_version_info(args) must still work for CLI compatibility."""
    offline_version_info.print_version_info(args=None)


def test_print_version_info_produces_output():
    """print_version_info() should complete without raising an exception."""
    instance = _make_offline_instance()
    instance.print_version_info()
