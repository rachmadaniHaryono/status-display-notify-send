"""Tests for the `cli` module."""

import pytest

from status_display_notify_send import cli

try:
    from status_display_notify_send.cli import DEFAULT_CMUS_INFO
except ImportError:
    DEFAULT_CMUS_INFO = None

import pytest


def test_main():
    """Basic CLI test."""
    with pytest.raises(SystemExit):
        cli.main()


def test_show_help():
    """
    Show help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main()


@pytest.mark.parametrize(
    "cmus_data, res_update",
    [
        (["status", "playing", "file", "/home/user/1.mp3"], {"status": "playing"}),
    ],
)
def test_status_data(cmus_data, res_update):
    if DEFAULT_CMUS_INFO is None:
        pytest.skip("can't get DEFAULT_CMUS_INFO")
        return
    exp_res = DEFAULT_CMUS_INFO.copy()
    exp_res.update(res_update)
    assert cli.status_data(cmus_data=cmus_data) == exp_res
