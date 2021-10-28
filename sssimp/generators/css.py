import logging
import sssimp
from sssimp import config
from sssimp.utils import path_strip


OUT_FILE = sssimp.OUTPUT_DIR / 'bundle.css'
CSS_DIR = sssimp.CONTENT_DIR / 'css'

def main():
    sssimp.IGNORE_ASSETS.add(str(CSS_DIR))
    files = (
        [CSS_DIR / file for file in config.CSS_FILES]
        if config.CSS_FILES else
        CSS_DIR.glob('**/*.css')
    )
    with open(OUT_FILE, 'w') as out:
        for file in files:
            relative_path = path_strip(file, CSS_DIR)
            logging.info(f'Bundling {relative_path}')
            print(f'/** bundle:{relative_path} **/', file=out)
            with open(file) as css_file:
                out.write(css_file.read())
            print(file=out)
