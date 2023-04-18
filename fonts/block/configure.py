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
sys.path.append(str(CURDIR.absolute().parent.parent))

from buildsystem.builder import new_glyph

import re
import buildsystem.logger as log
import buildsystem.macro as macro
import project as p

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
    log.info('Configuring base block glyphs')

    # names of the svgs for block pieces
    BLOCKS = [
        (B_U1, '1.svg'),
        (B_U2, '2.svg'),
        (B_U3, '3.svg'),

        (B_C1, '4.svg'),
        (B_LI, '0.svg'),
        (B_C2, '5.svg'),

        (B_D1, '6.svg'),
        (B_D2, '7.svg'),
        (B_D3, '8.svg'),
    ]

    for name, file in BLOCKS:
        try:
            new_glyph(font, None, name=name, width=0, color=0x69f08d,
                outline_path=CURDIR / p.OUTPUT_DIR / p.ASSETS_OUTPUT_DIR / file)
        except Exception as ex:
            log.warn(f"Error while configuring base glyph '{name}', the glyph may be corrupted!")
            raise

    # these dont seem to do anything
    # font.unlinkReferences()
    # font.removeOverlap()

    # i think this helps a lot
    font.round()

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
    macro.configure(CURDIR,
        p.PROJECT_FILE,
        p.USER_PROJECT_FILE,
        p.OUTPUT_DIR,
        p.ASSETS_OUTPUT_DIR,
        pre_configure=conf_blocks)

