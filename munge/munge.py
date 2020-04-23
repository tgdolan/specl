"""Main module."""
from yaml import load, FullLoader
from yaml.scanner import ScannerError


def read_spec(path: str) -> dict:
    """Reads in a munge spec file and creates a dict from it.
    This dict will be used to provide arguments to the various
    data munging functions."""
    with open(path) as yaml_spec:
        try:
            spec = load(yaml_spec, Loader=FullLoader)

        except ScannerError as scan_error:
            raise ValueError(f'Invalid spec found at: {path}')

    return spec if type(spec) == 'dict' else {}
