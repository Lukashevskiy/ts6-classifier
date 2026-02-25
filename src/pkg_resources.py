"""Minimal compatibility shim for propy on environments without setuptools.

Only `resource_filename` is implemented because propy uses that API to load
its bundled data files.
"""

from importlib import import_module
from pathlib import Path


def resource_filename(package_or_requirement: str, resource_name: str) -> str:
    module = import_module(package_or_requirement)
    module_file = getattr(module, "__file__", None)
    if module_file is None:
        raise FileNotFoundError(f"Cannot resolve package path for {package_or_requirement!r}")
    base = Path(module_file).resolve().parent
    return str((base / resource_name).resolve())

