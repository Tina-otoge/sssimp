import logging
import sssimp
from sssimp import jinja
from sssimp.utils import mkdir, path_strip


def generate(from_file, to):
    out_path = sssimp.OUTPUT_DIR / to
    mkdir(out_path)
    with open(from_file) as f:
        template = jinja.from_string(f.read())
    with open(out_path, 'w') as f:
        logging.info(f'Generating {to}')
        f.write(template.render())


def main():
    for file in sssimp.CONTENT_DIR.glob('**/*.html'):
        generate(file, path_strip(file, sssimp.CONTENT_DIR))
        sssimp.IGNORE_ASSETS.add(str(file))
