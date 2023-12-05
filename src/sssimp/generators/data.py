import json
import logging
import os
from pathlib import Path

import yaml

import sssimp
from sssimp import jinja
from sssimp.utils import path_strip

DATA_DIR = sssimp.INPUT_DIR / "data"


class Data:
    def __init__(self):
        self.dict = {}

    def handle_file(self, path: Path):
        parents = [
            x.split(".")[0] for x in path_strip(path, DATA_DIR).split(os.path.sep)
        ]
        getter = {
            "yml": yaml.safe_load,
            "yaml": yaml.safe_load,
            "json": json.load,
        }.get(path.suffix[1:])
        if not getter:
            return
        with open(path) as f:
            data = getter(f)
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
