import logging
import functools
from pathlib import Path
import jinja2
from jinja2 import Environment, FileSystemLoader

from . import config

__version__ = '0.0.3'

APP_DIR = Path(__file__).parent
INPUT_DIR = Path(config.INPUT_PATH)
CONTENT_DIR = INPUT_DIR / config.CONTENT_DIR_NAME
OUTPUT_DIR = Path(config.OUTPUT_PATH)
IGNORE_ASSETS = set()

jinja = Environment(
    loader=FileSystemLoader('input/templates', followlinks=True),
    autoescape=jinja2.select_autoescape(),
)

def filter(f):
    jinja.filters[f.__name__] = f
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return f(*args, **kwargs)
    return wrapper

from . import filters
