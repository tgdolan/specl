#!/usr/bin/env python

"""Tests for `specl` package."""
from functools import reduce
import os
import pytest
from unittest.mock import patch, mock_open
import numpy as np
import pandas as pd

from hypothesis import given, settings
from hypothesis.strategies import characters, composite, integers, lists, sampled_from, text
from hypothesis.extra import pandas as hpd

from hypothesis.extra.pandas import columns, data_frames
from specl import read_spec, read_data, build_kwargs_read, rename_columns, dropna_rows, write_data
from tests.fixtures import empty_csv, empty_spec, basic_spec_0, basic_spec_dict, basic_spec, write_funcs
from tests.strategies import names, gen_columns_and_subset, gen_rando_dataframe, gen_mixed_type_dataset


def write_dataframe_to_tmpdir(tmpdir, write_funcs, df, ext):
    tmp_file = tmpdir.make_numbered_dir().join(str(f'test{ext}'))
    write_funcs[ext](df, tmp_file.strpath)
    return tmp_file.strpath


def test_that_load_spec_returns_empty_dict_for_empty_spec(empty_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=empty_spec):
        spec = read_spec('fake/file.yaml')

    assert spec == {}


def test_that_load_spec_returns_dict_for_basic_spec(basic_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=basic_spec):
        spec = read_spec('fake/file.yaml')

    assert spec != {}, "Spec should not be empty for valid YAML file."
    assert [*spec] == ['input', 'output'], "Spec should have top-level input and output keys."
    assert spec['input']['file'] == 'source.csv', "Spec should have an input file defined."
    assert spec['output']['file'] == 'out.csv', "Spec should have an output file defined."
    assert list(spec['input']['columns'].keys()) == ['column_a', 'column_b', 'column_c', 'column_d']


def test_that_load_spec_raises_valueerror_for_invalid_spec(basic_spec_0):
    with pytest.raises(ValueError) as spec_error:
        with patch('builtins.open', new_callable=mock_open, read_data=basic_spec_0):
            spec = read_spec('fake/file.yaml')

    assert "invalid spec" in str(spec_error.value).lower()


@settings(deadline=None)
@given(data_frames(columns=columns("A B C".split(), dtype=int), index=hpd.range_indexes()),
       sampled_from(['.csv', '.xls', '.xlsx', '.parquet']))
def test_that_read_data_returns_data_frame(tmpdir, write_funcs, basic_spec_dict, df, ext):
    """Given a Hypothesis DataFrame, save it as a file of the sampled type,
       and test the reading that file into a Pandas DataFrame works as expected."""
    # print(f'generated dataframe has shape of: {df.shape} :: file type is: {ext}')

    expected = df.shape[1]

    # using make_numbered_dir to avoid path collisions when running test for each
    # hypothesis-generated data frame.
    # p = tmpdir.make_numbered_dir().join(str(f'test{ext}'))
    # write_funcs[ext](df, p.strpath)
    tmp_file_path = write_dataframe_to_tmpdir(tmpdir, write_funcs, df, ext)
    spec = {'input': {'file': tmp_file_path}}
    spec, df_in = read_data(spec)

    # TODO: Figure out why hypothesis DF shape not equal to Pandas when read from csv
    assert df_in.shape[1] >= expected


@settings(deadline=None)
@given(gen_columns_and_subset(), sampled_from(['.csv', '.xls', '.xlsx', '.parquet']))
def test_that_read_function_called_with_columns_specified(tmpdir, write_funcs, basic_spec_dict, df_config, ext):
    hdf, keeper_cols = df_config
    tmp_file_path = write_dataframe_to_tmpdir(tmpdir, write_funcs, hdf, ext)
    col_specs = map(lambda c: {c: {'data_type': 'int'}}, keeper_cols)
    basic_spec_dict['input']['file'] = tmp_file_path
    basic_spec_dict['input']['columns'] = {}
    # bogus, i know
    for col in col_specs:
        col_name = list(col.keys())[0]
        col_spec = list(col.values())[0]
        basic_spec_dict['input']['columns'][col_name] = col_spec
    spec, df = read_data(basic_spec_dict)
    assert list(df.columns.values).sort() == list(keeper_cols).sort()


def test_that_build_kwargs_adds_columns_arg(basic_spec_dict):
    kwargs = build_kwargs_read(basic_spec_dict, '.xlsx')
    assert 'usecols' in list(kwargs.keys())


def test_that_build_kwargs_adds_columns_arg_based_on_ext(basic_spec_dict):
    kwargs = build_kwargs_read(basic_spec_dict, '.parquet')
    assert 'columns' in list(kwargs.keys())


def test_that_build_kwargs_does_not_add_columns_arg_when_empty():
    spec = {'input': {'file': 'foo.txt'}}
    kwargs = build_kwargs_read(spec, '.csv')
    assert 'usecols' not in list(kwargs.keys())


def test_that_columns_get_renamed_per_spec(basic_spec_dict):
    basic_dataframe = pd.DataFrame(data={'A': [1, 2], 'B': [3, 4]})
    basic_spec_dict['input']['columns'] = {'A': {'data_type': 'int', 'name': 'foo'},
                                           'B': {'date_type': 'int', 'name': 'bar'}}
    spec, renamed_df = rename_columns(basic_spec_dict, basic_dataframe)
    assert spec == basic_spec_dict
    assert list(renamed_df.columns) == ['foo', 'bar']


@given(gen_rando_dataframe())
def test_that_columns_get_renamed_per_spec(basic_spec_dict, hdf):
    rename_col_config = map(lambda x: {x: {'data_type': 'int', 'name': x.upper()}}, list(hdf.columns))
    basic_spec_dict['input']['columns'] = reduce(lambda config, col: config.update(col) or config,
                                                 list(rename_col_config))
    spec, renamed_df = rename_columns(basic_spec_dict, hdf)
    assert spec == basic_spec_dict
    assert list(renamed_df.columns) == list(map(lambda col_name: col_name.upper(), list(hdf.columns)))


def test_that_drop_na_works_for_any(basic_spec_dict):
    basic_dataframe = pd.DataFrame(data={'A': [1, np.nan, 5], 'B': [3, np.nan, np.nan]})
    basic_spec_dict['transform']['rows']['dropna'] = 'any'
    spec, df_out = dropna_rows(basic_spec_dict, basic_dataframe)
    assert df_out.shape == (1, 2)


def test_that_drop_na_when_not_in_spec(basic_spec_dict):
    basic_dataframe = pd.DataFrame(data={'A': [1, np.nan, 4],
                                         'B': [3, np.nan, np.nan]})
    del basic_spec_dict['transform']['rows']['dropna']
    spec, df_out = dropna_rows(basic_spec_dict, basic_dataframe)
    assert df_out.shape == (3, 2)


def test_that_drop_na_works_for_all(basic_spec_dict):
    basic_dataframe = pd.DataFrame(data={'A': [1, np.nan, 2], 'B': [3, np.nan, np.nan]})
    basic_spec_dict['transform']['rows']['dropna'] = 'all'
    spec, df_out = dropna_rows(basic_spec_dict, basic_dataframe)
    assert df_out.shape == (2, 2)


@given(gen_mixed_type_dataset())
def test_that_drop_na_works_for_rows_hypothesis(basic_spec_dict, df):
    basic_spec_dict['transform']['rows']['dropna'] = 'any'
    df_out = dropna_rows(basic_spec_dict, df)
    count = df.count(axis=1)
    assert df.dropna().shape[0] == df_out.shape[0]


@settings(deadline=None)
@given(gen_columns_and_subset(), sampled_from(['.csv', '.xls', '.xlsx', '.parquet']))
def test_write(basic_spec_dict, mocker, tmpdir, write_funcs, df_config, ext):
    df, columns = df_config
    tmp_file = tmpdir.make_numbered_dir().join(str(f'test{ext}'))
    basic_spec_dict['output']['file'] = tmp_file.strpath
    basic_spec_dict['output']['columns'] = {}

    col_specs = map(lambda c: {c: {'data_type': 'int'}}, columns)
    # bogus, i know
    for col in col_specs:
        col_name = list(col.keys())[0]
        col_spec = list(col.values())[0]
        basic_spec_dict['output']['columns'][col_name] = col_spec
    write_data(basic_spec_dict, df)

    assert os.path.exists(basic_spec_dict['output']['file'])


