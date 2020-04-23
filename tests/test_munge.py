#!/usr/bin/env python

"""Tests for `munge` package."""

import pytest
from unittest.mock import patch, mock_open

from munge import read_spec


@pytest.fixture
def empty_spec():
    return ''


@pytest.fixture
def basic_spec():
    return """
cities:
  - Bratislava
  - Kosice
  - Trnava
  - Moldava
  - Trencin
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
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_that_load_spec_returns_empty_dict_for_empty_spec(empty_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=empty_spec):
        spec = read_spec('fake/file.yaml')

    assert (spec == {})


def test_that_load_spec_returns_dict_for_basic_spec(basic_spec):
    with patch('builtins.open', new_callable=mock_open, read_data=basic_spec):
        spec = read_spec('fake/file.yaml')

    assert (spec != {})


def test_that_load_spec_raises_ValueError_for_invalid_spec(basic_spec_0):
    with pytest.raises(ValueError) as spec_error:
        with patch('builtins.open', new_callable=mock_open, read_data=basic_spec_0):
            spec = read_spec('fake/file.yaml')

    assert "invalid spec" in str(spec_error.value).lower()


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string
