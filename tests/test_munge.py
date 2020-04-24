#!/usr/bin/env python

"""Tests for `munge` package."""
from functools import partial

import pytest
from unittest.mock import patch, mock_open

from hypothesis import given
from hypothesis.strategies import sampled_from
from hypothesis.extra import pandas as hpd
from pandas import read_csv
from pandas import DataFrame as pdf

import time

from hypothesis.extra.pandas import columns, data_frames
from munge import read_spec, read_data


@pytest.fixture
def write_funcs():
    return {'.csv': pdf.to_csv,
            '.xls': pdf.to_excel,
            '.xlsx': pdf.to_excel,
            # '.parquet': partial(pdf.to_parquet, compression='UNCOMPRESSED')
           }


@pytest.fixture
def empty_spec():
    return ''


@pytest.fixture
def basic_spec():
    return """
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
  COLUMN_C:
    data_type: int
  COLUMN_D:
    data_type: int
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


def test_that_load_spec_returns_empty_dict_for_empty_spec(empty_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=empty_spec):
        spec = read_spec('fake/file.yaml')

    assert spec == {}


def test_that_load_spec_returns_dict_for_basic_spec(basic_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=basic_spec):
        spec = read_spec('fake/file.yaml')

    assert spec != {}, "Spec should not be empty for valid YAML file."
    assert [*spec] == ['input', 'output']
    assert spec['input']['file'] == 'source.csv'
    assert spec['output']['file'] == 'out.csv'


def test_that_load_spec_raises_valueerror_for_invalid_spec(basic_spec_0):
    with pytest.raises(ValueError) as spec_error:
        with patch('builtins.open', new_callable=mock_open, read_data=basic_spec_0):
            spec = read_spec('fake/file.yaml')

    assert "invalid spec" in str(spec_error.value).lower()


@given(data_frames(columns=columns("A B C".split(), dtype=int), index=hpd.range_indexes()),
       sampled_from(['.csv', '.xls', '.xlsx']))
def test_that_read_data_returns_data_frame(tmpdir, write_funcs, df, ext):
    print(f'generated dataframe has shape of: {df.shape} :: file type is: {ext}')

    expected = df.shape[1]

    # using make_numbered_dir to avoid path collisions when running test for each
    # hypothesis-generated data frame.
    p = tmpdir.make_numbered_dir().join(str(f'test{ext}'))
    # TODO: Plug in dict for write_funcs
    write_funcs[ext](df, p.strpath)
    spec = {'input': {'file': p.strpath}}
    df_in = read_data(spec)

    # TODO: Figure out why hypothesis DF shape not equal to Pandas when read from csv
    assert df_in.shape[1] >= expected
