import io

import yaml

from .utils import MyTestClass1, construct1

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class MyLoader(Loader):
    pass


def test_default_constructors_registered():
    yamlcode = io.StringIO("""\
- !!python/tuple [hello, world]
""")

    objs = yaml.load(yamlcode, Loader=Loader)
    assert objs == [("hello", "world")]


def test_constructor_registration():
    yaml.add_constructor("!tag1", construct1, Loader=MyLoader)

    yamlcode = io.StringIO("""\
- !tag1
  x: 1
- !tag1
  x: 1
  'y': 2
  z: 3
""")

    objs = yaml.load(yamlcode, Loader=MyLoader)
    assert objs == [MyTestClass1(x=1), MyTestClass1(x=1, y=2, z=3)]
    # deletions from the registry should not impact other threads
    del MyLoader.yaml_constructors()["!tag1"]
