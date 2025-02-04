import pytest

import yaml
import yaml.tokens
from .utils import filter_data_files, load_code, serialize_value


@pytest.mark.needs_constructor_helpers
@pytest.mark.parametrize("data_filename,code_filename", filter_data_files(".data", ".code"))
def test_constructor_types(data_filename, code_filename):
    import datetime
    import signal

    from .constructor_helpers import (
        MyLoader, MyTestClass1, FixedOffset, MyTestClass2, MyTestClass3, YAMLObject1, AnObject,
        AnInstance, AState, ACustomState, InitArgs, InitArgsWithState, NewArgs, NewArgsWithState,
        Reduce, ReduceWithState, Slots, MyInt, MyList, MyDict,
    )

    native1 = None
    native2 = None
    with open(data_filename, 'rb') as file:
        native1 = list(yaml.load_all(file, Loader=MyLoader))
    if len(native1) == 1:
        native1 = native1[0]
    with open(code_filename, 'rb') as file:
        native2 = load_code(file.read(), globals(), locals())
    try:
        if native1 == native2:
            return
    except TypeError:
        pass
    assert serialize_value(native1) == serialize_value(native2), (native1, native2)


@pytest.mark.needs_constructor_helpers
@pytest.mark.parametrize("data_filename", filter_data_files(".subclass_blacklist"))
def test_subclass_blacklist_types(data_filename):
    from .constructor_helpers import MyFullLoader

    with pytest.raises(yaml.YAMLError):
        with open(data_filename, 'rb') as file:
            yaml.load(file.read(), MyFullLoader)
