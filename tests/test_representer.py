import pytest

from .utils import filter_data_files, load_code, serialize_value


@pytest.mark.needs_constructor_helpers
@pytest.mark.parametrize("code_filename", filter_data_files(".code"))
def test_representer_types(code_filename):
    import yaml
    import datetime
    import signal

    from .constructor_helpers import (
        MyDumper, MyLoader, FixedOffset, AnObject, AnInstance, AState, today, MyTestClass1,
        ACustomState, MyTestClass2, InitArgs, MyTestClass3, InitArgsWithState, YAMLObject1,
        NewArgs, NewArgsWithState, Reduce, ReduceWithState, Slots, MyInt, MyList, MyDict
    )

    for allow_unicode in [False, True]:
        for encoding in ['utf-8', 'utf-16-be', 'utf-16-le']:
            with open(code_filename, 'rb') as file:
                native1 = load_code(file.read(), globals(), locals())
            native2 = None
            # Globals contain MyDumper and MyLoader from calling make_constructor_helpers
            output = yaml.dump(native1, Dumper=MyDumper,
                        allow_unicode=allow_unicode, encoding=encoding)
            native2 = yaml.load(output, Loader=MyLoader)
            try:
                if native1 == native2:
                    continue
            except TypeError:
                pass
            value1 = serialize_value(native1)
            value2 = serialize_value(native2)
            assert value1 == value2, (native1, native2)
