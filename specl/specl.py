"""Main module."""
from functools import reduce, partial
from typing import Dict, Callable
from pathlib import Path
import logging
from yaml import load, load_all, FullLoader
from yaml.scanner import ScannerError
from pandas import DataFrame, read_csv, read_excel, read_parquet
from specl.decorators import log_cleanup_data
import importlib

read_funcs = {'.csv': read_csv,
              '.xls': read_excel,
              '.xlsx': read_excel,
              '.parquet': read_parquet}

write_funcs = {'.csv': DataFrame.to_csv,
               '.xls': DataFrame.to_excel,
               '.xlsx': DataFrame.to_excel,
               '.parquet': partial(DataFrame.to_parquet, compression=None)
               }


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
def rename_columns(spec: Dict, data_frame: DataFrame) -> (Dict, DataFrame):
    columns = spec['input']['columns']
    columns_to_rename = filter(lambda x: 'name' in x[1].keys(), list(columns.items()))
    column_name_keys = map(lambda col_config: {col_config[0]: col_config[1]['name']}, list(columns_to_rename))
    column_rename_data = reduce(lambda col_kv, src: col_kv.update(src) or col_kv, column_name_keys, {})
    df_renamed = data_frame.rename(columns=column_rename_data)
    return spec, df_renamed


@log_cleanup_data
def transform_columns(spec: Dict, data_frame: DataFrame) -> (Dict, DataFrame):
    columns = spec['transform']['columns']

    columns_to_transform = list(filter(lambda c: 'operation' in c[1], columns.items()))

    for new_col, config in columns_to_transform:
        pkg, method_name = config['operation'].rsplit('.', 1)

        mod = importlib.import_module(pkg)
        tx_method = getattr(mod, method_name)

        data_frame[new_col] = tx_method(data_frame[config['composed_of'][0]], data_frame[config['composed_of'][1]])

    return spec, data_frame


def read_data(spec: Dict) -> (Dict,DataFrame):
    """Creates Pandas DataFrame by reading file at path.
       Appropriate read_* pandas method will be called based
       on the extension of the input file specified."""

    path = spec['input']['file']
    ext = Path(path).suffix
    kwargs = build_kwargs_read(spec, ext)
    return spec, read_funcs[ext](path, **kwargs)


def dropna_rows(spec: Dict, data_frame: DataFrame) -> (Dict, DataFrame):
    """Drops rows in data_frame based on value of transform.rows.dropna in spec."""
    df_out = data_frame
    if 'dropna' in spec['transform']['rows']:
        df_out = data_frame.dropna(how=spec['transform']['rows']['dropna'])

    return spec, df_out


def write_data(spec, data_frame):
    output_path = spec['output']['file']
    ext = Path(output_path).suffix
    kwargs = build_kwargs_write(spec, ext)
    print(kwargs)
    write_funcs[ext](data_frame, output_path, **kwargs)


def execute(spec_path: str):
    """The entry point for the data cleanup process"""
    spec = read_spec(spec_path)
    spec, df1 = read_data(spec)
    spec, df2 = rename_columns(spec, df1)
    spec, df3 = transform_columns(spec, df2)
    return spec, df3


def build_kwargs_read(spec, ext):
    """Builds up kwargs for the Pandas read_* functions."""
    col_arg_names = {'.parquet': 'columns',
                     '.xls': 'usecols',
                     '.xlsx': 'usecols',
                     '.csv': 'usecols'}
    kwargs = {}
    if 'columns' in list(spec['input'].keys()):
        kwargs[col_arg_names[ext]] = list(spec['input']['columns'].keys())

    return kwargs


def build_kwargs_write(spec, ext):
    """Builds up kwargs for the Pandas to_* functions."""
    col_arg_names = {'.parquet': 'partition_cols',
                     '.xls': 'columns',
                     '.xlsx': 'columns',
                     '.csv': 'columns'}
    kwargs = {}

    if 'columns' in list(spec['output'].keys()) and not ext == '.parquet':
        kwargs[col_arg_names[ext]] = list(spec['output']['columns'].keys())

    return kwargs


def main(spec_path):
    spec, df = execute(spec_path)
    write_data(spec, df)


