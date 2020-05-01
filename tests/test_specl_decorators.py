import pytest
import logging

from hypothesis import given
from .strategies import gen_columns_and_subset

from specl.specl_decorators import log_cleanup_data


def test_should_log_function_arg_and_result_stats_fog_log_level_info(caplog):
    caplog.set_level(logging.INFO)

    @log_cleanup_data
    def mock_func(df):
        pass

    mock_func('data_frame_name')
    assert 'entering mock_func:' in caplog.text
    assert 'exiting mock_func:' in caplog.text


def test_should_not_log_function_arg_stats_fog_log_level_warning(caplog):
    caplog.set_level(logging.WARNING)

    @log_cleanup_data
    def mock_func(df):
        pass

    mock_func('data_frame_name')
    assert 'entering:' not in caplog.text
    assert 'exiting:' not in caplog.text


@given(gen_columns_and_subset())
def test_should_log_data_frame_shape(caplog, df_config):
    caplog.set_level(logging.INFO)
    data_frame, cols = df_config

    @log_cleanup_data
    def mock_func(df):
        return df

    mock_func(data_frame)
    assert 'shape of data frame in' in caplog.text
    assert 'shape of data frame out' in caplog.text


