FREE_THREADED_BUILD="$(python -c"import sysconfig; print(bool(sysconfig.get_config_var('Py_GIL_DISABLED')))")"
if [[ $FREE_THREADED_BUILD == "True" ]]; then
    python -m pip install -U pip
    python -m pip install cython==3.1.0b1 setuptools wheel
fi
