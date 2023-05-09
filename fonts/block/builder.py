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
from . import config, PROJECT_FILE, PROJECT_ROOT, BUILD_DIR, FORMATS, VARIANTS

def main():
    # TODO when the file is generated from scratch just use globals from project.py
    font = Font.open(PROJECT_ROOT / PROJECT_FILE)
    logging.info(f"Building font '{font.family_name}' version {font.version}")
    font.close()

    for variant in VARIANTS:
        font = Font.open(PROJECT_ROOT / PROJECT_FILE)
        font.computer_name = 'CompacityBlock'
        font.family_name = 'Compacity Block'
        if variant.suffix:
            font.computer_name += '-' + variant.suffix.replace(' ', '')
            font.family_name += '-' + variant.suffix.replace(' ', '')
            font.human_name += ' ' + variant.suffix

        font.export_filename = font.computer_name

        config.gen(font, variant.options)

        for format_ in FORMATS:
            font.export(BUILD_DIR, format_=format_)

        font.close()
