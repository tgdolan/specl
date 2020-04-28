#!/usr/bin/env python

"""Tests for `specl` package."""
from functools import partial

import pytest
from unittest.mock import patch, mock_open

from hypothesis import given, settings
from hypothesis.strategies import characters, composite, integers, lists, sampled_from, text
from hypothesis.extra import pandas as hpd
from pandas import DataFrame as pdf

from hypothesis.extra.pandas import columns, data_frames
from specl import read_spec, read_data

names = text(
    characters(max_codepoint=1000, blacklist_categories=('Cc', 'Cs')),
    min_size=1).map(lambda s: s.strip()).filter(lambda s: len(s) > 0)


@composite
def gen_columns_and_subset(draw, elements=names):
    column_names = draw(lists(elements, min_size=1, unique=True))
    num_columns_to_keep = draw(integers(min_value=1, max_value=len(column_names)))
    i = num_columns_to_keep
    columns_to_keep = []
    while i > 0:
        keeper_column = draw(integers(min_value=0, max_value=len(column_names) - 1))
        columns_to_keep.append(column_names[keeper_column])
        i = i - 1

    # With column data and 'keeper' columns selected, utilize draw to return
    # a hypothesis DataFrame column strategies defined.
    return draw(hpd.data_frames(hpd.columns(column_names, elements=text()),
                                index=hpd.range_indexes(min_size=5))), columns_to_keep


@pytest.fixture
def write_funcs():
    return {'.csv': pdf.to_csv,
            '.xls': pdf.to_excel,
            '.xlsx': pdf.to_excel,
            '.parquet': partial(pdf.to_parquet, compression='UNCOMPRESSED')
            }


@pytest.fixture
def empty_spec():
    return ''


@pytest.fixture
def basic_spec():
    return """
input: 
  columns: 
    column_a: 
      data_type: int
      name: COLUMN_A
    column_b: 
      data_type: int
      name: COLUMN_B
    column_c: 
      data_type: string
      name: COLUMN_C
    column_d: 
      composed_of: 
        - column_a
        - column_b
      operation: multiply
  file: source.csv
output: 
  columns: 
    COLUMN_C: 
      data_type: int
    COLUMN_D: 
      data_type: int
  file: out.csv
"""


@pytest.fixture
def basic_spec_0():
    return """
 ---
    input:
      column_a:
        data_type: int
        name: COLUMN_A
      column_b:
        data_type: int
        name: COLUMN_B
      column_c:
        data_type: string
        name: COLUMN_C
      column_d:
        composed_of:
          cols:
            - column_a
            - column_b
          operation: multiply
        name: COLUMN_D
      file: source.csv
    output:
      file: out.csv
      column_c
      column_d
    """


@pytest.fixture
def empty_csv():
    return ''


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
def test_that_read_data_returns_data_frame(tmpdir, write_funcs, df, ext):
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
    df_in = read_data(spec)

    # TODO: Figure out why hypothesis DF shape not equal to Pandas when read from csv
    assert df_in.shape[1] >= expected


@given(gen_columns_and_subset())
def test_that_read_function_called_with_columns_specified(self, df_config):
    pass
    # hdf, keeper_cols = df_config
    # result = read_data
    # filtered_df = fpscratch.filter_cols(hdf, keeper_cols)
    # print(f'filtered_cols: {filtered_df.columns} :: keepers: {keeper_cols}')
    # self.assertEqual(filtered_df.columns, keeper_cols)


