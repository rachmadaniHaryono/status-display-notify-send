"""Tests for the `cli` module."""

import pytest

from status_display_notify_send import cli


def test_main():
    """Basic CLI test."""
    with pytest.raises(SystemExit):
        cli.main()


def test_show_help(capsys):
    """
    Show help.

    Arguments:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main()
    assert capsys.readouterr().out
