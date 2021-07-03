"""Console script for specl."""
import argparse
import sys
import specl

import logging


def _set_log_level(loglevel):
    """ Snipped from Python doc:
    https://docs.python.org/3/howto/logging.html#logging-to-a-file"""
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level)


def main():
    """Console script for specl."""
    parser = argparse.ArgumentParser()
    parser.add_argument('_', nargs='*')
    parser.add_argument('-s', '--spec',
                        help='path to specl spec .yaml file',
                        type=str)
    parser.add_argument('-l', '--log',
                        help='set to INFO for basic dataframe shape info at each step. set to DEBUG to write intermediate dataframes to disk.')
    args = parser.parse_args()

    if args.spec:
        if args.log:
            _set_log_level(args.log)
        specl.main(args.spec)
        return 0
    else:
        parser.print_help(sys.stderr)
        return 1

    return 0


if __name__ == "__main__":

    sys.exit(main())  # pragma: no cover
