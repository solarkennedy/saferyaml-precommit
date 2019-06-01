#!/usr/bin/env python3
import argparse
import json
import hashlib
import sys
from pprint import pprint

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import ruamel.yaml as yaml


class YAMLSemanticChangeError(Exception):
    pass


def make_yaml_file_safer(filename):
    with open(filename, mode='r+') as fd:
        before_hash = hashlib.md5(fd.read().encode('utf8')).hexdigest()
        fd.seek(0)
        before = hashlib.md5(
            json.dumps(load(open(filename), Loader=Loader), sort_keys=True).encode('utf8'),
        ).hexdigest()
        try:
            data = yaml.round_trip_load(fd, preserve_quotes=True)
            pprint(data)
            fd.seek(0)
        except Exception as e:
            print(f"Failure loading {filename}: {e}")
            return 2
    
        fd.seek(0)
        fd.truncate()
        yaml.round_trip_dump(data, fd, width=120, indent=2)
        fd.seek(0)
        after = hashlib.md5(
            json.dumps(load(open(filename), Loader=Loader), sort_keys=True).encode('utf8'),
        ).hexdigest()
        after_hash = hashlib.md5(fd.read().encode('utf8')).hexdigest()
        if before != after:
            raise YAMLSemanticChangeError("The parsed yaml changed after rewriting it!!!")
        return int(before_hash != after_hash)



def main(argv=None):
    parser = argparse.ArgumentParser(description='Round-trip ruamel.yaml parser: ' +
        'read YAML from stdin and write to stdout')
    parser.add_argument('filenames', nargs='*', help='Yaml filenames to check.')
    args = parser.parse_args()
    exit_code = 0
    for filename in args.filenames:
        ret = make_yaml_file_safer(filename)
        if ret:
            print(f"Made {filename} safer")
        exit_code |= ret
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
