import pytest

from saferyaml_precommit.main import make_yaml_file_safer
from saferyaml_precommit.main import YAMLSemanticChangeError


@pytest.mark.parametrize(
    ('input_yaml', 'expected_yaml'),
    (
        ('foo:         bar\n', 'foo: bar\n'),
        ('foo: False\n', 'foo: false\n'),
    ),
)
def test_fixes_stuff_and_returns_1(input_yaml, expected_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    ret = make_yaml_file_safer(path.strpath)
    assert path.read() == expected_yaml
    assert ret == 1


@pytest.mark.parametrize(
    ('input_yaml', 'expected_yaml'),
    (
        ('foo: bar\n', 'foo: bar\n'),
        ('foo: "no"\n', 'foo: "no"\n'),
        ('foo: false\n', 'foo: false\n'),
    ),
)
def test_is_idempotent_and_returns_0(input_yaml, expected_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    ret = make_yaml_file_safer(path.strpath)
    assert path.read() == expected_yaml
    assert ret == 0


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
