import pytest

import yaml.reader
from .utils import filter_data_files

def _run_reader(data):
    with pytest.raises(yaml.reader.ReaderError):
        stream = yaml.reader.Reader(data)
        while stream.peek() != '\0':
            stream.forward()


@pytest.mark.parametrize("error_filename", filter_data_files(".stream-error"))
def test_stream_error(error_filename):
    with open(error_filename, 'rb') as file:
        _run_reader(file)
    with open(error_filename, 'rb') as file:
        _run_reader(file.read())
    for encoding in ['utf-8', 'utf-16-le', 'utf-16-be']:
        try:
            with open(error_filename, 'rb') as file:
                data = file.read().decode(encoding)
            break
        except UnicodeDecodeError:
            pass
    else:
        return
    _run_reader(data)
    with open(error_filename, encoding=encoding) as file:
        _run_reader(file)
