import datetime
import pathlib
from functools import lru_cache

import pytest


DATA_DIR = pathlib.Path(__file__).parent / 'data'


@lru_cache()
def all_data_files():
    files = {}
    for file in DATA_DIR.iterdir():
        if not file.is_file() or file.stem.endswith('-py2'):
            continue
        files.setdefault(file.stem, []).append(file.suffix)
    return files


@lru_cache()
def filter_data_files(*suffixes, skips=None):
    if skips is None:
        skips = ()
    elif isinstance(skips, str):
        skips = (skips,)

    params = []
    files = all_data_files()
    for filename, exts in files.items():
        if all(suffix in exts for suffix in suffixes) and not any(skip in exts for skip in skips):
            params.append(
                pytest.param(
                    *[DATA_DIR / (filename + suffix) for suffix in suffixes],
                    id=filename,
                )
            )
    return params


def load_code(expression, globals, locals):
    return eval(expression, globals, locals)


def serialize_value(data):
    if isinstance(data, list):
        return '[%s]' % ', '.join(map(serialize_value, data))
    elif isinstance(data, dict):
        items = []
        for key, value in data.items():
            key = serialize_value(key)
            value = serialize_value(value)
            items.append("%s: %s" % (key, value))
        items.sort()
        return '{%s}' % ', '.join(items)
    elif isinstance(data, datetime.datetime):
        return repr(data.utctimetuple())
    elif isinstance(data, float) and data != data:
        return '?'
    else:
        return str(data)

