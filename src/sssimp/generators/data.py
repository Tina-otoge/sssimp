import json
import logging
import os
from pathlib import Path

import yaml

import sssimp
from sssimp import jinja
from sssimp.utils import path_strip

from .markdown import MarkdownPage

DATA_DIR = sssimp.INPUT_DIR / "data"


class Data:
    def __init__(self):
        self.dict = {}

    def handle_file(self, path: Path):
        def opener(func):
            def wrapped(path):
                with path.open() as f:
                    return func(f)

            return wrapped

        parents = [
            x.split(".")[0]
            for x in path_strip(path, DATA_DIR).split(os.path.sep)
        ]
        getter = {
            "md": read_markdown,
            "json": opener(json.load),
            "yaml": opener(yaml.safe_load),
            "yml": opener(yaml.safe_load),
        }.get(path.suffix[1:])
        if not getter:
            logging.warning(f"Unsupported data file {path}")
            return
        data = getter(path)
        logging.debug(f"Data: {path} -> {data}")
        target = self.dict
        for parent in parents[:-1]:
            target = target.setdefault(parent, {})
        target[parents[-1]] = data


def prepare():
    data = Data()
    for file in DATA_DIR.rglob("*.*"):
        logging.info(f"Handling data file {file}")
        data.handle_file(file)
    jinja.globals["data"] = data.dict


def read_markdown(path: Path):
    logging.info("read_markdown")
    return MarkdownPage(path, path)
