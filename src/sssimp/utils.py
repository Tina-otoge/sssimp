import os
import sys
import traceback
from pathlib import Path
from typing import Type

from sssimp import APP_DIR


def mkdir(path):
    """
    Creates a directory or the parent directory if `path` is not a directory.
    Safely ignores if already exists
    """
    path = Path(path)
    if not path.is_dir():
        path = path.parent
    path.mkdir(exist_ok=True, parents=True)


def path_strip(path, parent=APP_DIR):
    """Strips `parent` from `path`"""
    path = str(path)
    path = path.removeprefix(str(parent))
    path = path.removeprefix(os.path.sep)
    return path


def run_safely(f, exception_type: Type[Exception] = Exception, out=sys.stderr):
    try:
        f()
    except exception_type:
        print(traceback.format_exc(), file=out)
