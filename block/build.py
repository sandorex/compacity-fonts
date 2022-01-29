#!/usr/bin/env python3
# compacity-fonts
#
# Copyright 2022 Aleksandar Radivojevic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# 	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# build.py: Exports the font

import os, sys
from pathlib import Path
CURDIR = Path(os.path.dirname(__file__))
sys.path.append(str(CURDIR.absolute().parent))

from buildsystem.builder import export_font
import buildsystem.logger as log

import fontforge
import project as p

if __name__ == '__main__':
    log.info(f"Using FontForge {fontforge.version()}")
    log.info('Formats enabled:')
    for i in p.FORMATS:
        print(f'- {i}')
    print()

    font = fontforge.open(str(CURDIR / p.PROJECT_FILE))

    log.info(f"Exporting font '{font.fullname}' version {font.version}")
    export_font(font, CURDIR / p.OUTPUT_DIR, p.FORMATS)

    if os.path.exists(CURDIR / p.USER_PROJECT_FILE):
        user_font = fontforge.open(str(CURDIR / p.USER_PROJECT_FILE))
        log.info('Exporting user modified font')
        export_font(user_font, CURDIR / p.OUTPUT_DIR, p.FORMATS)

