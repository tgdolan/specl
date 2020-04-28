"""Console script for specl."""
import argparse
import sys
from specl import specl


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
    print(args)
    foo = len(sys.argv)
    bar = sys.argv
    if args.spec:
        specl.execute(args.spec)
        return 0
    else:
        parser.print_help(sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
