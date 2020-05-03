"""Main module."""
from functools import reduce
from typing import Dict, Callable
from pathlib import Path
import logging
from yaml import load, load_all, FullLoader
from yaml.scanner import ScannerError
from pandas import DataFrame, read_csv, read_excel, read_parquet
from specl.specl_decorators import log_cleanup_data



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


@log_cleanup_data
def rename_columns(spec, data_frame):
    columns = spec['input']['columns']
    columns_to_rename = filter(lambda x: 'name' in x[1].keys(), list(columns.items()))
    column_name_keys = map(lambda col_config: {col_config[0]: col_config[1]['name']}, list(columns_to_rename))
    column_rename_data = reduce(lambda col_kv, src: col_kv.update(src) or col_kv, column_name_keys, {})
    rnf = data_frame.rename(columns=column_rename_data)
    return spec, rnf


def read_data(spec: Dict) -> DataFrame:
    """Creates Pandas DataFrame by reading file at path.
       Appropriate read_* pandas method will be called based
       on the extension of the input file specified."""

    path = spec['input']['file']
    ext = Path(path).suffix
    kwargs = build_kwargs(spec, ext)
    return read_funcs[ext](path, **kwargs)


def execute(spec_path: str):
    """The entry point for the data munging process"""
    spec = read_spec(spec_path)
    df1 = read_data(spec)
    spec, df2 = rename_columns(spec, df1)
    print(df2)


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


if __name__ == '__main__':
    execute('../samples/spec/sample_spec.yml')
