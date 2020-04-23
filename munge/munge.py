"""Main module."""
from typing import Dict, Callable

from yaml import load, load_all, FullLoader
from yaml.scanner import ScannerError
from pandas import DataFrame, read_csv


def data_read_function(path: str) -> Callable:
    """Decorator for determining appropriate 'read' function
    based on the file extension."""



def read_spec(path: str) -> dict:
    """Reads in a munge spec file and creates a dict from it.
    This dict will be used to provide arguments to the various
    data munging functions."""
    with open(path) as yaml_spec:
        try:
            spec = load(yaml_spec, Loader=FullLoader)

        except ScannerError as scan_error:
            raise ValueError(f'Invalid spec found at: {path}')

    return spec if spec else {}


def read_data(spec: Dict) -> DataFrame:
    """Creates Pandas DataFrame by reading file at path.
    Note: Should create decorator to create a 'reader' that
    handles both .csv and .parquet."""

    path = spec['input']['file']
    return read_csv(path)
