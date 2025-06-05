import pytest
import yaml_ft


def test_dump():
    assert yaml_ft.dump(['foo'])


def test_load_no_loader():
    with pytest.raises(TypeError):
        yaml_ft.load("- foo\n")


def test_load_safeloader():
    assert yaml_ft.load("- foo\n", Loader=yaml_ft.SafeLoader)
