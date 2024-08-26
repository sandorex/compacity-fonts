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
import copy

from builder.font import Font
import config
import project as p
#from . import config, PROJECT_FILE, PROJECT_ROOT, BUILD_DIR, FORMATS, VARIANTS, project as p

def main():
    # TODO when the file is generated from scratch just use globals from project.py
    # font = Font.open(PROJECT_ROOT / PROJECT_FILE)
    logging.info(f"Building font '{p.PROJECT_FAMILY_NAME}' version {p.PROJECT_VERSION}")

    # font = Font()
    # TODO maybe save the common file here? but do not push to git
    # config.static_gen(font)
    # font.save('test.sfd')
    # font.close()

    for variant in p.VARIANTS:
        # font = Font.open('test.sfd')
        # font = Font.open(PROJECT_ROOT / PROJECT_FILE)
        font = Font()
        font.version = p.PROJECT_VERSION
        # TODO use data from project.py
        # TODO set font.copyright
        font.computer_name = 'CompacityBlock'
        font.family_name = 'Compacity Block'
        font.human_name = font.family_name
        if variant.suffix:
            font.computer_name += '-' + variant.suffix.replace(' ', '')
            font.family_name += '-' + variant.suffix.replace(' ', '')
            font.human_name += ' ' + variant.suffix

        logging.info(f"Building variant '{font.human_name}'")

        font.export_filename = font.computer_name

        config.static_gen(font) # TODO temp execute only once before and save it
        config.gen(font, variant.options)
        # font.font.unlinkReferences() # TODO?

        for format_ in FORMATS:
            font.export(BUILD_DIR, format_=format_)

        font.close()
