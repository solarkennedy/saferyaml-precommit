import pytest

from saferyaml_precommit.main import make_yaml_file_safer
from saferyaml_precommit.main import YAMLSemanticChangeError


@pytest.mark.parametrize(
    ('input_yaml', 'expected_yaml'),
    (
        ('foo:         bar\n', 'foo: bar\n'),
    ),
)
def test_fixes_stuff(input_yaml, expected_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    assert make_yaml_file_safer(path.strpath) == 1
    assert path.read() == expected_yaml


@pytest.mark.parametrize(
    ('input_yaml', 'expected_yaml'),
    (
        ('foo: bar\n', 'foo: bar\n'),
    ),
)
def test_is_idempotent(input_yaml, expected_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    assert make_yaml_file_safer(path.strpath) == 0, path.read()
    assert path.read() == expected_yaml


@pytest.mark.parametrize(
    ('input_yaml', 'expected_yaml'),
    (
        ('foo: bar\nfoo: baz\n', 'foo: bar\n'),
    ),
)
@pytest.mark.filterwarnings('ignore:')
def test_raises_on_things_it_cant_handle(input_yaml, expected_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    with pytest.raises(YAMLSemanticChangeError):
        make_yaml_file_safer(path.strpath)
