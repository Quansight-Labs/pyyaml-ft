import pathlib
import pytest

from . import setup_modules
from . import utils


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "needs_constructor_helpers: generate constructor helpers"
    )
    config.addinivalue_line(
        "markers", "needs_structure_helpers: generate structure helpers"
    )
    config.addinivalue_line(
        "markers", "needs_resolver_helpers: generate resolver helpers"
    )
    config.addinivalue_line(
        "markers", "python_only: tests that run with the Python extension only"
    )
    config.addinivalue_line(
        "markers", "c_only: tests that run with the C extension only"
    )


@pytest.fixture(
    params=[
        (setup_modules.setup_pyext, setup_modules.teardown_pyext),
        (setup_modules.setup_cext, setup_modules.teardown_cext),
    ],
    ids=["pyext", "cext"],
    autouse=True
)
def _ext(request):
    setup, teardown = request.param

    constructor_helpers = False
    if request.node.get_closest_marker("needs_constructor_helpers") is not None:
        constructor_helpers = True
    structure_helpers = False
    if request.node.get_closest_marker("needs_structure_helpers") is not None:
        structure_helpers = True
    resolver_helpers = False
    if request.node.get_closest_marker("needs_resolver_helpers") is not None:
        resolver_helpers = True

    setup(constructor_helpers, structure_helpers, resolver_helpers)
    yield
    teardown(constructor_helpers, structure_helpers, resolver_helpers)


@pytest.fixture(autouse=True)
def filter_python_only_tests(request, _ext):
    node = request.node
    if setup_modules.RUNNING_C_EXT and node.get_closest_marker("python_only") is not None:
        pytest.skip("Skipping python-only when running cext")

    if not setup_modules.RUNNING_C_EXT and node.get_closest_marker("c_only") is not None:
        pytest.skip("Skipping c-only when running pyext")

    if not setup_modules.RUNNING_C_EXT:
        return

    try:
        callspec = node.callspec
    except AttributeError:
        return

    file = None
    for v in callspec.params.values():
        if isinstance(v, pathlib.Path):
            file = v
            break
    else:
        return
    data_files = utils.all_data_files()
    if ".skip-ext" in data_files[file.stem]:
        pytest.skip("Skipping .skip-ext when running cext")
