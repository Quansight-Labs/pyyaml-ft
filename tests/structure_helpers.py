import yaml
from . import canonical  # Needed for CanonicalLoader


def make_structure_helpers():
    global MyLoader, MyCanonicalLoader

    class MyLoader(yaml.Loader):
        def construct_sequence(self, node):
            return tuple(yaml.Loader.construct_sequence(self, node))
        def construct_mapping(self, node):
            pairs = self.construct_pairs(node)
            pairs.sort(key=(lambda i: str(i)))
            return pairs
        def construct_undefined(self, node):
            return self.construct_scalar(node)

    MyLoader.add_constructor('tag:yaml.org,2002:map', MyLoader.construct_mapping)
    MyLoader.add_constructor(None, MyLoader.construct_undefined)

    class MyCanonicalLoader(yaml.CanonicalLoader):
        def construct_sequence(self, node):
            return tuple(yaml.CanonicalLoader.construct_sequence(self, node))
        def construct_mapping(self, node):
            pairs = self.construct_pairs(node)
            pairs.sort(key=(lambda i: str(i)))
            return pairs
        def construct_undefined(self, node):
            return self.construct_scalar(node)

    MyCanonicalLoader.add_constructor('tag:yaml.org,2002:map', MyCanonicalLoader.construct_mapping)
    MyCanonicalLoader.add_constructor(None, MyCanonicalLoader.construct_undefined)
