import pytest

import yaml
from . import canonical
from .utils import filter_data_files


@pytest.mark.parametrize("canonical_filename", filter_data_files(".canonical"))
def test_canonical_scanner(canonical_filename):
    with open(canonical_filename, 'rb') as file:
        data = file.read()
    tokens = list(yaml.canonical_scan(data))
    assert tokens, tokens


@pytest.mark.parametrize("canonical_filename", filter_data_files(".canonical"))
def test_canonical_parser(canonical_filename):
    with open(canonical_filename, 'rb') as file:
        data = file.read()
    events = list(yaml.canonical_parse(data))
    assert events, events


@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical", skips=".empty"))
def test_canonical_error(data_filename, canonical_filename):
    with open(data_filename, 'rb') as file:
        data = file.read()
    with pytest.raises(yaml.YAMLError):
        list(yaml.canonical_load_all(data))
