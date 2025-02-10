import pytest

import yaml
from .utils import filter_data_files

@pytest.mark.parametrize("input_filename,sorted_filename", filter_data_files(".sort", ".sorted"))
def test_sort_keys(input_filename, sorted_filename):
    with open(input_filename, 'rb') as file:
        input = file.read().decode('utf-8')
    with open(sorted_filename, 'rb') as file:
        sorted = file.read().decode('utf-8')
    data = yaml.load(input, Loader=yaml.FullLoader)
    dump_sorted = yaml.dump(data, default_flow_style=False, sort_keys=True)
    dump_unsorted = yaml.dump(data, default_flow_style=False, sort_keys=False)
    dump_unsorted_safe = yaml.dump(data, default_flow_style=False, sort_keys=False, Dumper=yaml.SafeDumper)
    assert dump_sorted == sorted
    assert dump_unsorted == input
    assert dump_unsorted_safe == input
