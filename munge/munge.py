"""Main module."""
from yaml import load, FullLoader


def read_spec(path: str) -> dict:
    """Reads in a munge spec file and creates a dict from it.
    This dict will be used to provide arguments to the various
    data munging functions."""
    with open(path) as yaml_spec:
        spec = load(yaml_spec, Loader=FullLoader)

    return spec if type(spec) == 'dict' else {}
