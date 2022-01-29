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
# configure.py: Configures fontforge project

import os, sys
from pathlib import Path
CURDIR = Path(os.path.dirname(__file__))
sys.path.append(str(CURDIR.absolute().parent))

from typing import Any, Dict, List, Tuple, Union
from buildsystem.builder import new_glyph

import re, fontforge, time
import project as p
import config

try:
    import user_config # type: ignore
    USER_CONFIG = True
except ImportError:
    USER_CONFIG = False

B_LI = 'bblock.0'
B_U1 = 'bblock.1'
B_U2 = 'bblock.2'
B_U3 = 'bblock.3'
B_C1 = 'bblock.4'
B_C2 = 'bblock.5'
B_D1 = 'bblock.6'
B_D2 = 'bblock.7'
B_D3 = 'bblock.8'

def conf_blocks(font):
    # names of the svgs for block pieces
    BLOCKS = [
        (B_U1, '1.svg'),
        (B_U2, '2.svg'),
        (B_U3, '3.svg'),

        (B_C1, '7.svg'),
        (B_LI, '0.svg'),
        (B_C2, '8.svg'),

        (B_D1, '4.svg'),
        (B_D2, '5.svg'),
        (B_D3, '6.svg'),
    ]

    for name, file in BLOCKS:
        new_glyph(font, None, name=name, width=0, color=0x69f08d,
            outline_path=CURDIR / p.OUTPUT_DIR / p.ASSETS_OUTPUT_DIR / file)

def to_block(pattern, matrix=None):
    """Converts a string to blocks for easier changes to layout

    `matrix` is matrix that is applied to all parts
    """
    blocks = []
    char = '#'

    # i just gave up and gone for regex, probably a nicer solution but im tired
    # of this thing..
    result = re.match(r'(...) ([# ]{2}|\|\|) (...)', pattern)
    if result is None:
        print('error') # TODO
        return []

    l, c, r = result.groups()

    # middle and line
    if c == '||':
        blocks.append(B_LI)
    else:
        for i in range(len(c)):
            if c[i] == char:
                blocks.append([B_C1, B_C2][i])

    # upper part
    for i in range(len(l)):
        if l[i] == char:
            blocks.append([B_U1, B_U2, B_U3][i])

    # lower part
    for i in range(len(r)):
        if r[i] == char:
            blocks.append([B_D1, B_D2, B_D3][i])

    # apply matrix to all blocks
    if matrix is not None:
        return [ (i, matrix) for i in blocks ]

    return blocks

if __name__ == '__main__':
    font = fontforge.open(str(CURDIR / p.PROJECT_FILE))
    # conf_blocks(font) # TODO: genereator script
    config.configure(font)

    font.comment = f'Last configured on {time.ctime()}'
    font.save()

    if USER_CONFIG:
        # set font name and such only when first making the project to allow
        # the user to change anything without it being overwritten
        if not os.path.exists(CURDIR / p.USER_PROJECT_FILE):
            user_font = font

            # used as font name when picking fonts
            user_font.familyname = user_font.familyname + ' (M)'

            # human readable name, but i do not know the difference compared to familyname
            user_font.fullname = user_font.fullname + ' (M)'

            # used when exporting the font
            user_font.default_base_filename = user_font.default_base_filename + '-user-mod'
        else:
            user_font = fontforge.open(str(CURDIR / p.USER_PROJECT_FILE))

        user_config.configure(user_font)

        # only visible in the fontforge i think
        user_font.comment = f'USER MODIFIED\nLast configured on {time.ctime()}'

        user_font.save(str(CURDIR / p.USER_PROJECT_FILE))
