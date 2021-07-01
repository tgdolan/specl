import logging

from hypothesis import given
from strategies import gen_columns_and_subset, a_b_dataframe

from specl.decorators import log_cleanup_data

import pandas as pd


def test_should_log_function_arg_and_result_stats_fog_log_level_info(caplog):

    df = pd.DataFrame()

    @log_cleanup_data
    def mock_func(spec, df):
        return spec, df

    with caplog.at_level(logging.INFO, logger='root'):
        mock_func(None, df)
        assert 'entering mock_func:' in caplog.text
        assert 'exiting mock_func:' in caplog.text

def test_should_not_log_function_arg_stats_fog_log_level_warning(caplog):

    @log_cleanup_data
    def mock_func(spec, df):
        return spec, df

    with caplog.at_level(logging.WARNING, logger='root'):
        mock_func(None, pd.DataFrame())
        assert 'entering:' not in caplog.text
        assert 'exiting:' not in caplog.text


@given(gen_columns_and_subset())
def test_should_log_data_frame_shape(caplog, df_config):
    caplog.set_level(logging.INFO)
    data_frame, cols = df_config

    @log_cleanup_data
    def mock_func(spec, df, cols):
        return spec, df[cols]
    with caplog.at_level(logging.INFO, logger='root'):
        mock_func(None, pd.DataFrame())
        assert 'shape of data frame in' in caplog.text
        assert 'shape of data frame out' in caplog.text
