#!/usr/bin/env python3
from saferyaml_transitioner.main import round_trip_lint

def parse(i):
    return round_trip_lint(i).decode('utf8').strip()

def test_round_trip_passes_through():
    i = "foo: true"
    assert parse(i) == "foo: true"


def test_round_trip_passes_through_multiline():
    i = """foo: true
bar: baz"""
    assert parse(i) == i


def test_round_trip_replaces_bad_bools():
    i = "foo: NO"
    assert parse(i) == "foo: false"
