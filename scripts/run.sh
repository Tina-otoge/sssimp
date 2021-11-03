#!/bin/bash

python -m venv .venv
source .venv/bin/activate
pip install --upgrade .
python -m sssimp
