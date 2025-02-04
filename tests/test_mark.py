import pytest

import yaml
from .utils import filter_data_files


@pytest.mark.parametrize("marks_filename", filter_data_files(".marks"))
def test_marks(marks_filename):
    with open(marks_filename, 'r') as file:
        inputs = file.read().split('---\n')[1:]
    for input in inputs:
        index = 0
        line = 0
        column = 0
        while input[index] != '*':
            if input[index] == '\n':
                line += 1
                column = 0
            else:
                column += 1
            index += 1
        mark = yaml.Mark(marks_filename, index, line, column, input, index)
        snippet = mark.get_snippet(indent=2, max_length=79)
        assert isinstance(snippet, str), type(snippet)
        assert snippet.count('\n') == 1, snippet.count('\n')
        data, pointer = snippet.split('\n')
        assert len(data) < 82, len(data)
        assert data[len(pointer)-1] == '*', data[len(pointer)-1]
