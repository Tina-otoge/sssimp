import logging
from pathlib import Path
import jinja2
from jinja2 import Environment, PackageLoader

from . import config

APP_DIR = Path(__file__).parent
INPUT_DIR = Path('./input')
CONTENT_DIR = INPUT_DIR / 'content'
OUTPUT_DIR = Path('./output')
IGNORE_ASSETS = {'__init__.py', '__pycache__'}

logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT)

jinja = Environment(
    loader=PackageLoader('input'),
    autoescape=jinja2.select_autoescape(),
)
