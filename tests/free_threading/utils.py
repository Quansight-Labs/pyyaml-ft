class MyTestClass1:
    def __init__(self, x, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        if isinstance(other, MyTestClass1):
            return self.__class__, self.__dict__ == other.__class__, other.__dict__
        else:
            return False

    def __repr__(self):
        return f"MyTestClass1(x={self.x}, y={self.y}, z={self.z})"


def represent1(representer, native):
    return representer.represent_mapping("!tag1", native.__dict__)


def construct1(constructor, node):
    mapping = constructor.construct_mapping(node)
    return MyTestClass1(**mapping)


class Dice(tuple):
    def __new__(cls, a, b):
        return tuple.__new__(cls, (a, b))

    def __repr__(self):
        return "Dice(%s,%s)" % self


def dice_constructor(loader, node):
    value = loader.construct_scalar(node)
    a, b = map(int, value.split('d'))
    return Dice(a, b)


def dice_representer(dumper, data):
    return dumper.represent_scalar("!dice", "%sd%s" % data)
