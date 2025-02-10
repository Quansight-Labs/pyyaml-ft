import pytest

import yaml
from . import test_emitter
from .utils import filter_data_files

@pytest.mark.parametrize("error_filename", filter_data_files(".loader-error"))
def test_loader_error(error_filename):
    with pytest.raises(yaml.YAMLError):
        with open(error_filename, 'rb') as file:
            list(yaml.load_all(file, yaml.FullLoader))


@pytest.mark.parametrize("error_filename", filter_data_files(".loader-error"))
def test_loader_error_string(error_filename):
    with pytest.raises(yaml.YAMLError):
        with open(error_filename, 'rb') as file:
            list(yaml.load_all(file.read(), yaml.FullLoader))


@pytest.mark.parametrize("error_filename", filter_data_files(".single-loader-error"))
def test_loader_error_single(error_filename):
    with pytest.raises(yaml.YAMLError):
        with open(error_filename, 'rb') as file:
            yaml.load(file.read(), yaml.FullLoader)


@pytest.mark.parametrize("error_filename", filter_data_files(".emitter-error"))
def test_emitter_error(error_filename):
    with open(error_filename, 'rb') as file:
        events = list(yaml.load(file, Loader=test_emitter.EventsLoader))
    with pytest.raises(yaml.YAMLError):
        yaml.emit(events)


@pytest.mark.parametrize("error_filename", filter_data_files(".dumper-error"))
def test_dumper_error(error_filename):
    from io import StringIO
    import yaml

    with open(error_filename, 'rb') as file:
        code = file.read()
    with pytest.raises(yaml.YAMLError):
        exec(code)
