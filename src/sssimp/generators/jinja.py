import logging

import sssimp
from sssimp.utils import path_strip

FILES = set()


def prepare():
    for file in sssimp.CONTENT_DIR.glob("**/*.j2"):
        logging.info(f"Handling Jinja2 template {file}")
        FILES.add(file)
        sssimp.IGNORE_ASSETS.add(str(file))


def main():
    for file in FILES:
        target = (
            sssimp.OUTPUT_DIR / path_strip(file, sssimp.CONTENT_DIR)
        ).with_suffix("")
        with file.open() as f:
            content = f.read()
        templated = sssimp.jinja.from_string(content)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("w") as f:
            f.write(templated.render() + "\n")
