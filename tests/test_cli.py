from specl import cli
from unittest.mock import patch
import sys

def test_that_main_returns_message_when_no_args_provided(capsys):
    """ Calling cli.main() without any args should result in usage message displayed to terminal.
        Test works when running with pytest, but not pytest --cov=specl --cov-report html.
        Need to figure out how to populate args to cli here, vs those passed in from pytest command."""
    testargs = ["prog"]
    with patch.object(sys, 'argv', testargs):
        result = cli.main()
        out, err = capsys.readouterr()
        assert 'usage' in err
