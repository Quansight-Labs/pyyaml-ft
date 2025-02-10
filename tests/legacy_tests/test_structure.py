import pytest

import yaml
from .utils import filter_data_files


def _convert_structure(loader):
    if loader.check_event(yaml.ScalarEvent):
        event = loader.get_event()
        if event.tag or event.anchor or event.value:
            return True
        else:
            return None
    elif loader.check_event(yaml.SequenceStartEvent):
        loader.get_event()
        sequence = []
        while not loader.check_event(yaml.SequenceEndEvent):
            sequence.append(_convert_structure(loader))
        loader.get_event()
        return sequence
    elif loader.check_event(yaml.MappingStartEvent):
        loader.get_event()
        mapping = []
        while not loader.check_event(yaml.MappingEndEvent):
            key = _convert_structure(loader)
            value = _convert_structure(loader)
            mapping.append((key, value))
        loader.get_event()
        return mapping
    elif loader.check_event(yaml.AliasEvent):
        loader.get_event()
        return '*'
    else:
        loader.get_event()
        return '?'


@pytest.mark.parametrize("data_filename,structure_filename", filter_data_files(".data", ".structure"))
def test_structure(data_filename, structure_filename):
    nodes1 = []
    with open(structure_filename, 'r') as file:
        nodes2 = eval(file.read())
    with open(data_filename, 'rb') as file:
        loader = yaml.Loader(file)
        while loader.check_event():
            if loader.check_event(
                yaml.StreamStartEvent, yaml.StreamEndEvent,
                yaml.DocumentStartEvent, yaml.DocumentEndEvent
            ):
                loader.get_event()
                continue
            nodes1.append(_convert_structure(loader))
    if len(nodes1) == 1:
        nodes1 = nodes1[0]
    assert nodes1 == nodes2, (nodes1, nodes2)


def _compare_events(events1, events2, full=False):
    assert len(events1) == len(events2), (len(events1), len(events2))
    for event1, event2 in zip(events1, events2):
        assert event1.__class__ == event2.__class__, (event1, event2)
        if isinstance(event1, yaml.AliasEvent) and full:
            assert event1.anchor == event2.anchor, (event1, event2)
        if isinstance(event1, (yaml.ScalarEvent, yaml.CollectionStartEvent)):
            if (event1.tag not in [None, '!'] and event2.tag not in [None, '!']) or full:
                assert event1.tag == event2.tag, (event1, event2)
        if isinstance(event1, yaml.ScalarEvent):
            assert event1.value == event2.value, (event1, event2)


@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_parser(data_filename, canonical_filename):
    events1 = None
    events2 = None
    with open(data_filename, 'rb') as file:
        events1 = list(yaml.parse(file))
    with open(canonical_filename, 'rb') as file:
        events2 = list(yaml.canonical_parse(file))
    _compare_events(events1, events2)


@pytest.mark.parametrize("canonical_filename", filter_data_files(".canonical"))
def test_parser_on_canonical(canonical_filename):
    events1 = None
    events2 = None
    with open(canonical_filename, 'rb') as file:
        events1 = list(yaml.parse(file))
    with open(canonical_filename, 'rb') as file:
        events2 = list(yaml.canonical_parse(file))
    _compare_events(events1, events2, full=True)


def _compare_nodes(node1, node2):
    assert node1.__class__ == node2.__class__, (node1, node2)
    assert node1.tag == node2.tag, (node1, node2)
    if isinstance(node1, yaml.ScalarNode):
        assert node1.value == node2.value, (node1, node2)
    else:
        assert len(node1.value) == len(node2.value), (node1, node2)
        for item1, item2 in zip(node1.value, node2.value):
            if not isinstance(item1, tuple):
                item1 = (item1,)
                item2 = (item2,)
            for subnode1, subnode2 in zip(item1, item2):
                _compare_nodes(subnode1, subnode2)


@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files(".data", ".canonical"))
def test_composer(data_filename, canonical_filename):
    nodes1 = None
    nodes2 = None
    with open(data_filename, 'rb') as file:
        nodes1 = list(yaml.compose_all(file))
    with open(canonical_filename, 'rb') as file:
        nodes2 = list(yaml.canonical_compose_all(file))
    assert len(nodes1) == len(nodes2), (len(nodes1), len(nodes2))
    for node1, node2 in zip(nodes1, nodes2):
        _compare_nodes(node1, node2)


@pytest.mark.needs_structure_helpers
@pytest.mark.parametrize("data_filename,canonical_filename", filter_data_files('.data', '.canonical'))
def test_constructor(data_filename, canonical_filename):
    from .structure_helpers import MyLoader, MyCanonicalLoader

    native1 = None
    native2 = None
    with open(data_filename, 'rb') as file:
        native1 = list(yaml.load_all(file, Loader=MyLoader))
    with open(canonical_filename, 'rb') as file:
        native2 = list(yaml.load_all(file, Loader=MyCanonicalLoader))
    assert native1 == native2, (native1, native2)
