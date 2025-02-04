import pytest

import yaml


@pytest.mark.python_only
def test_dump():
    assert yaml.dump(['foo'])


@pytest.mark.python_only
def test_load_no_loader():
    with pytest.raises(TypeError):
        yaml.load("- foo\n")


@pytest.mark.python_only
def test_load_safeloader():
    assert yaml.load("- foo\n", Loader=yaml.SafeLoader)
