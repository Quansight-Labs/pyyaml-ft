import pytest

import yaml
from .utils import filter_data_files

class AnInstance:

    def __init__(self, foo, bar):
        self.foo = foo
        self.bar = bar

    def __repr__(self):
        try:
            return "%s(foo=%r, bar=%r)" % (self.__class__.__name__,
                    self.foo, self.bar)
        except RuntimeError:
            return "%s(foo=..., bar=...)" % self.__class__.__name__

class AnInstanceWithState(AnInstance):

    def __getstate__(self):
        return {'attributes': [self.foo, self.bar]}

    def __setstate__(self, state):
        self.foo, self.bar = state['attributes']


@pytest.mark.parametrize("recursive_filename", filter_data_files(".recursive"))
def test_recursive(recursive_filename):
    context = globals().copy()
    with open(recursive_filename, 'rb') as file:
        exec(file.read(), context)
    value1 = context['value']
    output1 = yaml.dump(value1)
    value2 = yaml.unsafe_load(output1)
    output2 = yaml.dump(value2)
    assert output1 == output2, (output1, output2)
