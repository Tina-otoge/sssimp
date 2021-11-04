from pathlib import Path

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


def path_strip(path, parent = APP_DIR):
    """Strips `parent` from `path`"""
    path = str(path)
    path = path.removeprefix(str(parent))
    path = path.removeprefix('/')
    return path
