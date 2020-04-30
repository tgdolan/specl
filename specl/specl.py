"""Main module."""
from typing import Dict, Callable
from pathlib import Path

from yaml import load, load_all, FullLoader
from yaml.scanner import ScannerError
from pandas import DataFrame, read_csv, read_excel, read_parquet

read_funcs = {'.csv': read_csv,
              '.xls': read_excel,
              '.xlsx': read_excel,
              '.parquet': read_parquet}


def data_read_function(path: str) -> Callable:
    """Decorator for determining appropriate 'read' function
    based on the file extension."""



def read_spec(path: str) -> dict:
    """Reads in a specl spec file and creates a dict from it.
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
       Appropriate read_* pandas method will be called based
       on the extension of the input file specified."""

    path = spec['input']['file']
    ext = Path(path).suffix
    kwargs = build_kwargs(spec, ext)
    print(kwargs)
    return read_funcs[ext](path, **kwargs)


def execute(spec: str):
    """The entry point for the data munging process"""
    pass


def build_kwargs(spec, ext):
    """Builds up kwargs for the Pandas read_* functions."""
    col_arg_names = {'.parquet': 'columns',
                     '.xls': 'usecols',
                     '.xlsx': 'usecols',
                     '.csv': 'usecols'}
    kwargs = {}
    if 'columns' in list(spec['input'].keys()):
        kwargs[col_arg_names[ext]] = list(spec['input']['columns'].keys())

    return kwargs
