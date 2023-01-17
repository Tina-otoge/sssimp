import logging

import sssimp
from sssimp import config, jinja
from sssimp.utils import mkdir, path_strip

BUNDLE_FILE = "bundle.css"
OUT_FILE = sssimp.OUTPUT_DIR / BUNDLE_FILE
CSS_DIR = sssimp.INPUT_DIR / "css"
css_files = None


def prepare():
    global css_files
    jinja.globals["BUNDLE_FILE"] = BUNDLE_FILE
    css_files = list(
        [CSS_DIR / file for file in config.CSS_FILES]
        if config.CSS_FILES
        else CSS_DIR.glob("**/*.css")
    )
    if css_files:
        jinja.globals["BUNDLE_TIME"] = max(x.stat().st_ctime for x in css_files)


def main():
    if not css_files:
        logging.debug("No CSS files found, skipping")
        return
    mkdir(OUT_FILE)
    with open(OUT_FILE, "w") as out:
        for file in css_files:
            relative_path = path_strip(file, CSS_DIR)
            logging.info(f"Bundling {relative_path}")
            print(f"/** bundle:{relative_path} **/", file=out)
            with open(file) as css_file:
                out.write(css_file.read())
            print(file=out)
