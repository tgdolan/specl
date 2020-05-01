"""Decorators used in specl."""
import inspect
import logging

def log_cleanup_data(func):
    """When log level set to INFO, log the stats for the DataFrame arguments
       to the given function as well as stats for the DataFrame to be returned.

       Accessing args to function described here:
       https://avacariu.me/writing/2017/python-decorators-inspecting-function-arguments
       """
    # sig = inspect.signature(func)

    def wrapper(*args, **kwargs):
        # bound_arguments = sig.bind(*args, **kwargs)
        # bound_arguments.apply_defaults()
        logging.info(f'entering {func.__name__}: shape of data frame in is: {args[0].shape}')
        return_val = func(*args, **kwargs)
        logging.info(f'exiting {func.__name__}: shape of data frame out is: {return_val.shape}')
    return wrapper
