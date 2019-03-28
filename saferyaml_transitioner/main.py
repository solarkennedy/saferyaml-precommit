#!/usr/bin/env python3
import sys
from ruamel.yaml import YAML
from yaml import safe_load as classic_yaml_load
from yaml import safe_dump as classic_yaml_dump

import argparse
import io


def yaml_sanitize(i):
    if isinstance(i, str):
        o = classic_yaml_dump(classic_yaml_load(str(i))).replace('\n...\n', '')
        print(f"{i} -> {o}")
    else:
        o = i
    return o


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
    stream = io.BytesIO()
    yaml=YAML()
    parsed = yaml.load(contents)
    for p in parsed:
        print(repr(parsed[p]))
        parsed[p] = yaml_sanitize(parsed[p])
        print(repr(parsed[p]))
    yaml.default_flow_style = False
    yaml.dump(parsed, stream)
    stream.seek(0)
    return stream.read()


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
            print(f"Exception while parsing {filename}: {exc}")
            retval = 1
    return retval



if __name__ == '__main__':
    sys.exit(main())
