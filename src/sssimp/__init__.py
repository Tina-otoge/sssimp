import functools
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from . import config

__version__ = "0.0.16"

APP_DIR = Path(__file__).parent
INPUT_DIR = Path(config.INPUT_PATH)
OUTPUT_DIR = Path(config.OUTPUT_PATH)
IGNORE_ASSETS = set()

CONTENT_DIR = None

jinja = Environment(
    autoescape=config.AUTOESCAPE,
    trim_blocks=True,
    lstrip_blocks=True,
    extensions=["jinja2.ext.do"],
)


def resolve():
    global CONTENT_DIR
    CONTENT_DIR = INPUT_DIR / config.CONTENT_DIR_NAME
    loader = FileSystemLoader(INPUT_DIR / "templates", followlinks=True)
    jinja.loader = loader


def filter(f):
    jinja.filters[f.__name__] = f

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)

    return wrapper


from . import filters
