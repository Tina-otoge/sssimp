import logging
import sssimp
from sssimp import config, jinja
from sssimp.utils import mkdir, path_strip


BUNDLE_FILE = 'bundle.css'
OUT_FILE = sssimp.OUTPUT_DIR / BUNDLE_FILE
CSS_DIR = sssimp.INPUT_DIR / 'css'

def main():
    files = (
        [CSS_DIR / file for file in config.CSS_FILES]
        if config.CSS_FILES else
        CSS_DIR.glob('**/*.css')
    )
    time = 0
    mkdir(OUT_FILE)
    with open(OUT_FILE, 'w') as out:
        for file in files:
            relative_path = path_strip(file, CSS_DIR)
            logging.info(f'Bundling {relative_path}')
            print(f'/** bundle:{relative_path} **/', file=out)
            with open(file) as css_file:
                out.write(css_file.read())
            print(file=out)
            time = max(time, file.stat().st_mtime)
    jinja.globals['BUNDLE_TIME'] = time
    jinja.globals['BUNDLE_FILE'] = BUNDLE_FILE
