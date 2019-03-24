#!/usr/bin/env python3
from saferyaml_transitioner.main import round_trip_lint

def test_round_trip_passes_through():
    i = "foo: true"
    assert round_trip_lint(i) == "foo: true\n"
