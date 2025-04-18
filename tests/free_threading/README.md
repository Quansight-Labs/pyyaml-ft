# Free-threaded tests

This directory aims to collect some tests around free-threading that are
to be run with [`pytest-run-parallel`](https://github.com/Quansight-Labs/pytest-run-parallel).

Because `Constructor`, `Representer` and `Resolver` classes have been
adjusted to include thread-local registries, the respective tests make sure
that the registries are indeed thread-local and thread-safe when changing
from multiple threads.

`test_stress` aims to add an integration stress test that tests parsing/dumping
yaml strings and adds some randomness to the process.

`test_real_world` presents a use-case closer to how PyYAML will be used
in the real world. It creates a directory with a lot of different YAML files
that resemble those of Github Actions and tries to parse them all in a thread pool.
