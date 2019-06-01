#!/usr/bin/env python3
import argparse
import json
import hashlib
import sys

from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

import ruamel.yaml as yaml


class YAMLSemanticChangeError(Exception):
    pass


def md5_file(fd):
    fd.seek(0)
    h = hashlib.md5(fd.read().encode('utf8')).hexdigest()
    return h


def md5_yaml_data(fd):
    fd.seek(0)
    h =  hashlib.md5(
        json.dumps(load(fd, Loader=Loader), sort_keys=True).encode('utf8'),
    ).hexdigest()
    return h


def make_yaml_file_safer(filename):
    with open(filename, mode='r+') as fd:
        hash_file_before = md5_file(fd)
        hash_data_before = md5_yaml_data(fd)
        try:
            fd.seek(0)
            data = yaml.round_trip_load(fd, preserve_quotes=True)
        except Exception as e:
            print(f"Failure loading {filename}: {e}")
            return 2
    
        fd.seek(0)
        fd.truncate()
        yaml.round_trip_dump(data, fd, width=120, indent=2)

        hash_data_after = md5_yaml_data(fd)
        hash_file_after = md5_file(fd)
        if hash_data_before != hash_data_after:
            raise YAMLSemanticChangeError("The parsed yaml changed after rewriting it!!!")
        return int(hash_file_before != hash_file_after)


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
