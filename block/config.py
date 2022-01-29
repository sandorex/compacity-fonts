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
# config.py: Dynamic configuration file for the font

import sys

if __name__ == '__main__':
    print('Please run configure.py script instead')
    sys.exit(1)

from buildsystem.builder import new_glyph
from configure import to_block as b
from project import CHAR_WIDTH

import psMat
import configure as c

def letters(font):
    LETTERS = {
        "a": b(r'  # ||    '),
        "b": b(r'  # || #  '),
        "c": b(r'    || ## '),
        "d": b(r' ## ||    '),
        "e": b(r' #  ||    '),
        "f": b(r'### ||    '),
        "g": b(r'    || #  '),
        "h": b(r' ## || #  '),
        "i": b(r'# # ||    '),
        "j": b(r'# # || ## '),
        "k": b(r' #  ||  # '),
        "l": b(r' ## || ## '),
        "m": b(r'  # || ###'),
        "n": b(r'  # || # #'),
        "o": b(r'#   ||    '),
        "p": b(r'##  ||    '),
        "q": b(r' ## || ###'),
        "r": b(r'    ||  # '),
        "s": b(r'    ||  ##'),
        "t": b(r'    || ###'),
        "u": b(r'##  ||  ##'),
        "v": b(r'##  || ## '),
        "w": b(r'##  || ###'),
        "x": b(r'### || ## '),
        "y": b(r' ## || ###'),
        "z": b(r'# # || ###'),
    }

    # clone layout for uppercase letters
    for k, v in dict(LETTERS).items():
        LETTERS[k.upper()] = v

    # add the glyphs
    for k, v in LETTERS.items():
        new_glyph(font, k, width=CHAR_WIDTH, refs=v)

def numbers(font):
    NUMBERS = {}

    blocklist = [
        c.B_U2,
        c.B_U3,
        c.B_C1,
        c.B_C2,
        c.B_D1,
        c.B_D2,
    ]

    # generates 0 to 9 glyphs as if the blocks defined above were binary digits
    for i, b in enumerate(map(lambda x: format(x, 'b').zfill(6), range(10))):
        blocks = [ c.B_U1, c.B_D3 ]
        for j, ch in enumerate(reversed(b)):
            if ch == '1':
                blocks.append(blocklist[j])

        NUMBERS[str(i)] = blocks

    # add the glyphs
    for k, v in NUMBERS.items():
        new_glyph(font, k, width=CHAR_WIDTH, refs=v)

def special(font):
    """Configures special characters, that have varying width and function"""
    ## ZERO WIDTH ##
    # TODO: add almost all symbols here until they are recreated to fit
    for i in list(r';-`—'):
        new_glyph(font, i, width=0, color=0xb3b3b3)

    ## OTHER ##
    space_width = CHAR_WIDTH * 2

    new_glyph(font, None, name='one-width-space', width=CHAR_WIDTH)
    new_glyph(font, ' ', width=space_width)
    new_glyph(font, '.', refs=b('         #', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*5)

    new_glyph(font, ',', refs=b('        ##', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)
    new_glyph(font, '"', refs=b('##        ', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)
    new_glyph(font, '!', refs=b('### ## # #', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)

    new_glyph(font, '(', refs=b('### ## ###', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)
    new_glyph(font, ')', refs=b('### ## ###', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)

    new_glyph(font, None, refs=b('    ||    ', psMat.scale(2, 1)), name='blockspace', width=space_width)

def configure(font):
    """The function ran by configure script"""
    letters(font)
    numbers(font)
    special(font)
