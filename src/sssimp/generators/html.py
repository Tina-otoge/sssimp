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
        stat = src.stat()
        self.vars = {
            'path': target,
            'last_modified': stat.st_mtime,
            'created_at': stat.st_ctime,
        }

    def __str__(self):
        return str(self.target)

    @property
    def href(self):
        return path_strip(self.target, sssimp.OUTPUT_DIR)

    @property
    def name(self):
        return self.target.name

    @property
    def parent(self):
        return self.target.parent


    @functools.cache
    def render(self):
        with open(self.src) as f:
            content = f.read()
        template = jinja.from_string(content)
        return template.render(**self.vars)

    def write(self):
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
    for page in PAGES:
        page.vars['pages'] = PAGES
        page.write()
