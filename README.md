PyYAML-ft
=========

A full-featured YAML processing framework for Python with support for free-threading

## Why a fork?

[PEP 703](https://peps.python.org/pep-0703/) introduced free-threaded Python as a
separate build of CPython 3.13. Thread-safety issues that might have otherwise gone
unnoticed are now much easier to trigger because of the absence of protection from
the GIL. Also, because the free-threaded build is ABI-incompatible, extension
modules need to be separate, free-threaded wheels and declare support for
it.

The PyYAML maintainers
[decided to not port PyYAML to the free-threaded build](https://github.com/yaml/pyyaml/pull/830#issuecomment-2342475334)
before the latter, along with Cython support for it, has been tested more extensively
in real-world applications. Our rationale with this fork is to implement support for
the free-threaded build, so that PyYAML can be tested with it by its users, even before
the port is merged upstream.

### Differences compared with upstream

- This fork uses Cython 3.1.0b1 which supports the free-threaded build, but is still in
  beta. Its support for the free-threaded build is also still experimental.
- `add_constructor`, `add_representer` and `add_*resolver` now all use thread-local
  registries, so you will have to explicitly register your custom constrcutors,
  representers and resolvers in each thread. Here's a small test showcasing that:

  ```python3
  import io
  import threading
  import yaml


  class Dice:
      def __init__(self, first, second):
          self.first = first
          self.second = second
      def __repr__(self):
          return f"Dice({self.first}, {self.second})"


  def construct_dice(constructor, node):
      mapping = constructor.construct_mapping(node)
      return Dice(**mapping)


  def load_dice():
      yamlcode = io.StringIO("""\
  - !dice
    first: 1
    second: 6
  - !dice
    first: 4
    second: 4
  """)
      print(f"Thread {threading.current_thread().name}")
      try:
          objs = yaml.load(yamlcode, Loader=yaml.CLoader)
          print(f"\t{objs=}")
      except Exception as e:
          print(f"\tException occurred: {e!s}")

  yaml.add_constructor("!dice", construct_dice, Loader=yaml.CLoader)
  load_dice()

  t = threading.Thread(target=load_dice)
  t.start()
  t.join()
  ```

  Running the above script gives the following:

  ```bash
  ❯ python3.13t tmp/t.py
  Thread MainThread
          objs=[Dice(1, 6), Dice(4, 4)]
  Thread Thread-1 (load_dice)
          Exception occurred: could not determine a constructor for the tag '!dice'
    in "<file>", line 1, column 3
  ```

  If you see new errors in multithreaded programs using `PyYAML-ft` that work with
  `PyYAML`, you may need to add calls to `yaml.add_constructor`, `yaml.add_representer`
  `yaml.add_implicit_resolver` or `yaml.add_path_resolver` in your thread worker
  function or worker initialization function.

### Python versions support

Because PyYAML-ft is only aiming to exist for as long as upstream PyYAML
does not support the free-threaded build, we recommend that users only
conditionally switch to PyYAML-ft.

At this time, PyYAML-ft **only supports Python 3.13 and 3.13t (i.e. the
free-threaded build of 3.13)**. To switch to it, you can do the following
in your `requirements.txt` file:

```requirements.txt
...
PyYAML; python_version < '3.13'
PyYAML-ft; python_version >= '3.13'
```

If you're developing a library that depends on PyYAML and you're using
`pyproject.toml` to specify your dependencies, you can do the following:

```toml
dependencies = [
  ...,
  "PyYAML; python_version<'3.13'",
  "PyYAML-ft; python_version>='3.13'",
]
```


## Installation

To install, type `python setup.py install`.

By default, the `setup.py` script checks whether LibYAML is installed and if
so, builds and installs LibYAML bindings.
To skip the check and force installation of LibYAML bindings, use the option
`--with-libyaml`: `python setup.py --with-libyaml install`.
To disable the check and skip building and installing LibYAML bindings, use
`--without-libyaml`: `python setup.py --without-libyaml install`.

When LibYAML bindings are installed, you may use fast LibYAML-based parser and
emitter as follows:

    >>> yaml.load(stream, Loader=yaml.CLoader)
    >>> yaml.dump(data, Dumper=yaml.CDumper)

If you don't trust the input YAML stream, you should use:

    >>> yaml.safe_load(stream)

## Testing

PyYAML includes a comprehensive test suite.
To run the tests, type `python setup.py test`.

## Further Information

* For more information, check the
  [PyYAML homepage](https://github.com/yaml/pyyaml).

* [PyYAML tutorial and reference](http://pyyaml.org/wiki/PyYAMLDocumentation).

* Discuss PyYAML with the maintainers on
  Matrix at https://matrix.to/#/#pyyaml:yaml.io or
  IRC #pyyaml irc.libera.chat

* Submit bug reports and feature requests to the
  [PyYAML-ft bug tracker](https://github.com/Quansight-Labs/pyyaml/issues).

## License

The PyYAML module was written by Kirill Simonov <xi@resolvent.net>.
It is currently maintained by the YAML and Python communities.

PyYAML-ft is released under the MIT license.

See the file LICENSE for more details.
