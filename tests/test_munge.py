#!/usr/bin/env python

"""Tests for `munge` package."""

import pytest
from unittest.mock import patch, mock_open
from pandas import DataFrame, read_csv
from munge import read_spec, read_data


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


def test_that_read_data_returns_data_frame(tmpdir):
    p = tmpdir.mkdir("sub").join("hello.csv")
    p.write("id,color,wheels\n1,blue,4\n2,red,2")
    spec = {'input': {'file': p.strpath}}
    df = read_data(spec)

    assert df.shape[1] == 3


