import logging
import sssimp
from sssimp import jinja
from sssimp.utils import mkdir, path_strip

def write_template(to, template, *args, src=None, **kwargs):
    kwargs.setdefault('path', to)
    if src:
        kwargs.setdefault('src', src)
        stat = src.stat()
        kwargs.setdefault('last_modified', stat.st_mtime)
        kwargs.setdefault('created_at', stat.st_ctime)
    result = template.render(*args, **kwargs)
    mkdir(to)
    with open(to, 'w') as f:
        logging.info(f'Generating {to}')
        f.write(result)
    return result


def generate(from_file, to):
    out_path = sssimp.OUTPUT_DIR / to
    mkdir(out_path)
    with open(from_file) as f:
        template = jinja.from_string(f.read())
    write_template(out_path, template, src=from_file)


def main():
    for file in sssimp.CONTENT_DIR.glob('**/*.html'):
        generate(file, path_strip(file, sssimp.CONTENT_DIR))
        sssimp.IGNORE_ASSETS.add(str(file))
