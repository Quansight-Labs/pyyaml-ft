import pytest

import yaml
from .utils import filter_data_files, load_code


def myconstructor1(constructor, tag, node):
    seq = constructor.construct_sequence(node)
    return {tag: seq }

def myconstructor2(constructor, tag, node):
    seq = constructor.construct_sequence(node)
    string = ''
    try:
        i = tag.index('!') + 1
    except:
        try:
            i = tag.rindex(':') + 1
        except:
            pass
    if i >= 0:
        tag = tag[i:]
    return { tag: seq }

class Multi1(yaml.FullLoader):
    pass
class Multi2(yaml.FullLoader):
    pass


@pytest.mark.parametrize("input_filename,code_filename", filter_data_files(".multi", ".code"))
def test_multi_constructor(input_filename, code_filename):
    with open(input_filename, 'rb') as file:
        input = file.read().decode('utf-8')
    with open(code_filename, 'rb') as file:
        native = load_code(file.read(), globals(), locals())

    # default multi constructor for ! and !! tags
    Multi1.add_multi_constructor('!', myconstructor1)
    Multi1.add_multi_constructor('tag:yaml.org,2002:', myconstructor1)

    data = yaml.load(input, Loader=Multi1)
    assert(data == native)

    # default multi constructor for all tags
    Multi2.add_multi_constructor(None, myconstructor2)
    data = yaml.load(input, Loader=Multi2)
    assert(data == native)
