import pathlib
PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()

import sys
sys.path.append(PROJECT_ROOT)

import logging

# setup basic logger
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# from .project import PROJECT_FILE, FORMATS, Options, VARIANTS
from .generator import *

BUILD_DIR = ROOT / 'build'
