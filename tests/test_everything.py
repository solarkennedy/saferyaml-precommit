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
    assert expected_yaml == path.read()
    assert ret == 1


@pytest.mark.parametrize(
    'input_yaml',
    [
        'foo: bar\n',
        'foo: false\n',
        'a__________: 1\nb: false\ncc: false\n',
    ],
)
def test_is_idempotent_and_returns_0(input_yaml, tmpdir):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    ret = make_yaml_file_safer(path.strpath)
    assert input_yaml == path.read()
    assert ret == 0


@pytest.mark.parametrize(
    'input_yaml',
    [
    ],
)
@pytest.mark.filterwarnings('ignore:')
def test_raises_on_things_that_pytest_things_will_change(input_yaml, tmpdir, capsys):
    path = tmpdir.join('input.yaml')
    path.write(input_yaml)
    with pytest.raises(YAMLSemanticChangeError):
        make_yaml_file_safer(path.strpath)
