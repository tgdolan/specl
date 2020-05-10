"""Pytest fixtures"""
import pytest
from pandas import DataFrame as pdf
from functools import partial


@pytest.fixture(scope='module')
def write_funcs():
    return {'.csv': pdf.to_csv,
            '.xls': pdf.to_excel,
            '.xlsx': pdf.to_excel,
            '.parquet': partial(pdf.to_parquet, compression='UNCOMPRESSED')
            }


@pytest.fixture(scope='module')
def read_funcs():
    return {'.csv': read_csv,
            '.xls': read_excel,
            '.xlsx': read_excel,
            '.parquet': read_parquet}


@pytest.fixture(scope='module')
def empty_spec():
    return ''


@pytest.fixture(scope='module')
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


@pytest.fixture(scope='module')
def basic_spec_dict():
    return {'input': {'columns': {'column_a': {'data_type': 'int', 'name': 'COLUMN_A'},
                                  'column_b': {'data_type': 'int', 'name': 'COLUMN_B'},
                                  'column_c': {'data_type': 'string', 'name': 'COLUMN_C'},
                                  'column_d': {'composed_of': ['column_a', 'column_b'], 'operation': 'multiply'}},
                      'file': 'source.csv'},
            'transform': {'rows': {'dropna': 'any'},
                          'columns': {'COLUMN_A': {'dropna': 'all'},
                                      'COLUMN_B': {'dropna': 'any'},
                                      'COLUMN_C': {'dropna': 'all'}}},
            'output': {'columns': {'COLUMN_C': {'data_type': 'int'}, 'COLUMN_D': {'data_type': 'int'}},
                       'file': 'out.csv'}}


@pytest.fixture(scope='module')
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


@pytest.fixture(scope='module')
def empty_csv():
    return ''
