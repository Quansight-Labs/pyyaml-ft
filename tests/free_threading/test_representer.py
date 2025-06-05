import yaml_ft as yaml

from .utils import MyTestClass1, represent1

try:
    from yaml_ft import CDumper as Dumper
except ImportError:
    from yaml_ft import Dumper


class MyDumper(Dumper):
    pass


def test_default_representers_registered():
    obj = [("hello", "world")]

    yamlcode = yaml.dump(obj, Dumper=Dumper)
    assert yamlcode == """\
- !!python/tuple
  - hello
  - world
"""


def test_representer_registration():
    yaml.add_representer(MyTestClass1, represent1, Dumper=MyDumper)

    obj = [MyTestClass1(x=1), MyTestClass1(x=1, y=2, z=3)]

    yamlcode = yaml.dump(obj, Dumper=MyDumper)
    assert yamlcode == """\
- !tag1
  x: 1
  y: 0
  z: 0
- !tag1
  x: 1
  y: 2
  z: 3
"""
    del MyDumper.yaml_representers()[MyTestClass1]
