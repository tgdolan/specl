import pytest

from specl import cli


def test_that_main_returns_message_when_no_args_provided(capsys):
    cli.main()
    console_msg = capsys.readouterr().err

    assert 'usage' in console_msg
