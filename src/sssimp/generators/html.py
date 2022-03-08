from datetime import datetime
import logging
import functools

import sssimp
from sssimp import jinja
from sssimp.utils import mkdir, path_strip


PAGES = set()


class Page:
    def __init__(self, src, target):
        self.src = src
        self.target = target
        self.vars = {
            'page': self,
        }
        self.meta = None

    def __str__(self):
        return str(self.target)

    @property
    def created_at(self):
        return datetime.fromtimestamp(self.stat.st_ctime)

    @property
    def updated_at(self):
        time = datetime.fromtimestamp(self.stat.st_mtime)
        if time == self.created_at:
            return None
        return time

    @property
    @functools.cache
    def stat(self):
        return self.src.stat()

    @property
    def href(self):
        return path_strip(self.target, sssimp.OUTPUT_DIR)

    @property
    def name(self):
        return self.target.name

    @property
    def parent(self):
        return self.target.parent

    def get_template(self):
        with open(self.src) as f:
            content = f.read()
        return jinja.from_string(content)

    @functools.cache
    def render(self):
        return self.get_template().render(**self.vars)

    def write(self, target=None):
        target = target or self.target
        mkdir(self.target)
        with open(self.target, 'w') as f:
            logging.info(f'Generating {self.target}')
            f.write(self.render())


def prepare():
    for file in sssimp.CONTENT_DIR.glob('**/*.html'):
        target = sssimp.OUTPUT_DIR / path_strip(file, sssimp.CONTENT_DIR)
        PAGES.add(Page(src=file, target=target))
        sssimp.IGNORE_ASSETS.add(str(file))


def main():
    jinja.globals['pages'] = PAGES
    for page in PAGES:
        page.write()
