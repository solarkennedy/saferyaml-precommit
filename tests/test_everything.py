#!/usr/bin/env python3
from saferyaml_transitioner.main import round_trip_lint

def test_round_trip_passes_through():
    i = "foo: true"
    assert round_trip_lint(i) == b"foo: true\n"


def test_round_trip_passes_through_multiline():
    i = """foo: true
bar: baz
"""
    assert round_trip_lint(i) == i.encode('utf-8')
