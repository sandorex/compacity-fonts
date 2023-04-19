#!/usr/bin/env python3
# compacity-fonts
#
# Copyright 2023 Aleksandar Radivojevic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from builder.font import Font
from . import PROJECT_FILE, PROJECT_ROOT, ROOT

# setup basic logger
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

# TODO: add option to package font into zip for easier CI
def main():
    font = Font.open(PROJECT_ROOT / PROJECT_FILE)
    logging.info(f'Exporting font {font.name} {font.version} as ttf')
    font.export(ROOT / 'build')
