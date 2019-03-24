#!/usr/bin/env python3
import sys
from ruamel.yaml import YAML
import argparse

def round_trip_lint_a_file(f):
    contents = f.read()
    fixed_contents = round_trip_lint(contents)
    if contents != fixed_contents:
        f.seek(0)
        f.truncate()
        f.write(fixed_contents)
        return 0
    else:
        return 1

def round_trip_lint(contents):
    yaml=YAML()
    yaml.default_flow_style = False
    return yaml.dump({'a': [1, 2]}, s)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, 'r+b') as f:
                r = round_trip_lint_a_file(f)
                if r != 0:
                    retval = 1
        except Exception as exc:
            print(exc)
            retval = 1
    return retval



if __name__ == '__main__':
    sys.exit(main())
