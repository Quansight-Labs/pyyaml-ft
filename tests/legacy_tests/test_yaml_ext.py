import tempfile, sys, os

import pytest

import yaml
from .utils import filter_data_files


@pytest.mark.c_only
def test_c_version():
    assert ("%s.%s.%s" % yaml._yaml.get_version()) == yaml._yaml.get_version_string(),    \
            (yaml._yaml.get_version(), yaml._yaml.get_version_string())


def _compare_scanners(py_data, c_data):
    py_tokens = list(yaml.scan(py_data, Loader=yaml.PyLoader))
    c_tokens = []
    for token in yaml.scan(c_data, Loader=yaml.CLoader):
        c_tokens.append(token)
    assert len(py_tokens) == len(c_tokens), (len(py_tokens), len(c_tokens))
    for py_token, c_token in zip(py_tokens, c_tokens):
        assert py_token.__class__ == c_token.__class__, (py_token, c_token)
        if hasattr(py_token, 'value'):
            assert py_token.value == c_token.value, (py_token, c_token)
        if isinstance(py_token, yaml.StreamEndToken):
            continue
        py_start = (py_token.start_mark.index, py_token.start_mark.line, py_token.start_mark.column)
        py_end = (py_token.end_mark.index, py_token.end_mark.line, py_token.end_mark.column)
        c_start = (c_token.start_mark.index, c_token.start_mark.line, c_token.start_mark.column)
        c_end = (c_token.end_mark.index, c_token.end_mark.line, c_token.end_mark.column)
        assert py_start == c_start, (py_start, c_start)
        assert py_end == c_end, (py_end, c_end)


@pytest.mark.c_only
@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_c_scanner(data_filename, canonical_filename):
    with open(data_filename, 'rb') as file1, open(data_filename, 'rb') as file2:
        _compare_scanners(file1, file2)
    with open(data_filename, 'rb') as file1, open(data_filename, 'rb') as file2:
        _compare_scanners(file1.read(), file2.read())
    with open(canonical_filename, 'rb') as file1, open(canonical_filename, 'rb') as file2:
        _compare_scanners(file1, file2)
    with open(canonical_filename, 'rb') as file1, open(canonical_filename, 'rb') as file2:
        _compare_scanners(file1.read(), file2.read())


def _compare_parsers(py_data, c_data):
    py_events = list(yaml.parse(py_data, Loader=yaml.PyLoader))
    c_events = []
    for event in yaml.parse(c_data, Loader=yaml.CLoader):
        c_events.append(event)
    assert len(py_events) == len(c_events), (len(py_events), len(c_events))
    for py_event, c_event in zip(py_events, c_events):
        for attribute in ['__class__', 'anchor', 'tag', 'implicit',
                            'value', 'explicit', 'version', 'tags']:
            py_value = getattr(py_event, attribute, None)
            c_value = getattr(c_event, attribute, None)
            assert py_value == c_value, (py_event, c_event, attribute)


@pytest.mark.c_only
@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_c_parser(data_filename, canonical_filename):
    with open(data_filename, 'rb') as file1, open(data_filename, 'rb') as file2:
        _compare_parsers(file1, file2)
    with open(data_filename, 'rb') as file1, open(data_filename, 'rb') as file2:
        _compare_parsers(file1.read(), file2.read())
    with open(canonical_filename, 'rb') as file1, open(canonical_filename, 'rb') as file2:
        _compare_parsers(file1, file2)
    with open(canonical_filename, 'rb') as file1, open(canonical_filename, 'rb') as file2:
        _compare_parsers(file1.read(), file2.read())


def _compare_emitters(data):
    events = list(yaml.parse(data, Loader=yaml.PyLoader))
    c_data = yaml.emit(events, Dumper=yaml.CDumper)
    py_events = list(yaml.parse(c_data, Loader=yaml.PyLoader))
    c_events = list(yaml.parse(c_data, Loader=yaml.CLoader))
    assert len(events) == len(py_events), (len(events), len(py_events))
    assert len(events) == len(c_events), (len(events), len(c_events))
    for event, py_event, c_event in zip(events, py_events, c_events):
        for attribute in ['__class__', 'anchor', 'tag', 'implicit',
                            'value', 'explicit', 'version', 'tags']:
            value = getattr(event, attribute, None)
            py_value = getattr(py_event, attribute, None)
            c_value = getattr(c_event, attribute, None)
            if attribute == 'tag' and value in [None, '!'] \
                    and py_value in [None, '!'] and c_value in [None, '!']:
                continue
            if attribute == 'explicit' and (py_value or c_value):
                continue
            assert value == py_value, (event, py_event, attribute)
            assert value == c_value, (event, c_event, attribute)


@pytest.mark.c_only
@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_c_emitter(data_filename, canonical_filename):
    with open(data_filename, 'rb') as file:
        _compare_emitters(file.read())
    with open(canonical_filename, 'rb') as file:
        _compare_emitters(file.read())


@pytest.mark.c_only
def test_large_file():
    SIZE_LINE = 24
    SIZE_ITERATION = 0
    SIZE_FILE = 31
    if sys.maxsize <= 2**32:
        return
    if os.environ.get('PYYAML_TEST_GROUP', '') != 'all':
        return
    with tempfile.TemporaryFile() as temp_file:
        for i in range(2**(SIZE_FILE-SIZE_ITERATION-SIZE_LINE) + 1):
            temp_file.write(bytes(('-' + (' ' * (2**SIZE_LINE-4))+ '{}\n')*(2**SIZE_ITERATION), 'utf-8'))
        temp_file.seek(0)
        yaml.load(temp_file, Loader=yaml.CLoader)
