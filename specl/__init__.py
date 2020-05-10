"""Top-level package for specl."""

__author__ = """Tom Dolan"""
__email__ = 'tgdolan@gmail.com'
__version__ = '0.1.0'

# __all__ = ['specl']
from .specl import read_spec, read_data, build_kwargs_read, build_kwargs_write, rename_columns, execute, dropna_rows, \
    write_data, main
from .decorators import log_cleanup_data
