# Path from where to find files
INPUT_PATH = "./input"

# Folder inside input that holds non-template files
CONTENT_DIR_NAME = "content"

# Folder in which to output files
OUTPUT_PATH = "./output"

# List of css files to bundle, order counts, use None for all css files in css folder
CSS_FILES = None

# Removes current output folder before generating
CLEAN_OUTPUT = True

# For log messages
import logging

LOG_FORMAT = "[%(levelname)s] %(message)s"
LOG_LEVEL = logging.DEBUG

# To enable escaping by default on Jinja2 prints
AUTOESCAPE = False

# Seconds to wait before scanning files for new changes
WATCH_WAIT_TIME = 0.5
