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

import fontforge
import project as p

if __name__ == '__main__':
    # TODO: log some info
    font = fontforge.open(str(CURDIR / p.PROJECT_FILE))

    print(f"Exporting font '{font.familyname}' version {font.version} using FontForge {fontforge.version()}")
    export_font(font, CURDIR / p.OUTPUT_DIR, p.FORMATS)

    if os.path.exists(CURDIR / p.USER_PROJECT_FILE):
        user_font = fontforge.open(str(CURDIR / p.USER_PROJECT_FILE))
        print(f"Also exporting user modified version")
        export_font(user_font, CURDIR / p.OUTPUT_DIR, p.FORMATS)

