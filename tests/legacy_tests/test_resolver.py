import pprint

import pytest

import yaml
from .utils import filter_data_files


@pytest.mark.parametrize("data_filename,detect_filename", filter_data_files(".data", ".detect"))
def test_implicit_resolver(data_filename, detect_filename):
    correct_tag = None
    node = None
    with open(detect_filename, 'r') as file:
        correct_tag = file.read().strip()
    with open(data_filename, 'rb') as file:
        node = yaml.compose(file)
    assert isinstance(node, yaml.SequenceNode), node
    for scalar in node.value:
        assert isinstance(scalar, yaml.ScalarNode), scalar
        assert scalar.tag == correct_tag, (scalar.tag, correct_tag)


def _convert_node(node):
    if isinstance(node, yaml.ScalarNode):
        return (node.tag, node.value)
    elif isinstance(node, yaml.SequenceNode):
        value = []
        for item in node.value:
            value.append(_convert_node(item))
        return (node.tag, value)
    elif isinstance(node, yaml.MappingNode):
        value = []
        for key, item in node.value:
            value.append((_convert_node(key), _convert_node(item)))
        return (node.tag, value)


@pytest.mark.needs_resolver_helpers
@pytest.mark.parametrize("data_filename,path_filename", filter_data_files(".data", ".path"))
def test_path_resolver_loader(data_filename, path_filename):
    from .resolver_helpers import MyLoader

    with open(data_filename, 'rb') as file:
        nodes1 = list(yaml.compose_all(file.read(), Loader=MyLoader))
    with open(path_filename, 'rb') as file:
        nodes2 = list(yaml.compose_all(file.read()))
    for node1, node2 in zip(nodes1, nodes2):
        data1 = _convert_node(node1)
        data2 = _convert_node(node2)
        assert data1 == data2, (data1, data2)


@pytest.mark.needs_resolver_helpers
@pytest.mark.parametrize("data_filename,path_filename", filter_data_files(".data", ".path"))
def test_path_resolver_dumper(data_filename, path_filename):
    from .resolver_helpers import MyDumper

    for filename in [data_filename, path_filename]:
        with open(filename, 'rb') as file:
            output = yaml.serialize_all(yaml.compose_all(file), Dumper=MyDumper)
        nodes1 = yaml.compose_all(output)
        with open(data_filename, 'rb') as file:
            nodes2 = yaml.compose_all(file)
            for node1, node2 in zip(nodes1, nodes2):
                data1 = _convert_node(node1)
                data2 = _convert_node(node2)
                assert data1 == data2, (data1, data2)
