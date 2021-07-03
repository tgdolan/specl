"""Decorators used in specl."""
import inspect
import logging
from functools import wraps


def log_cleanup_data(func):
    """When log level set to INFO, log the stats for the DataFrame arguments
       to the given function as well as stats for the DataFrame to be returned.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(
            f'entering {func.__name__}: columns::{args[1].columns} -- shape of data frame in is: {args[1].shape}')

        return_val = func(*args, **kwargs)

        logging.info(
            f'exiting {func.__name__}: columns::{return_val[1].columns} -- shape of data frame out is: {return_val[1].shape}')

        return return_val

    return wrapper
