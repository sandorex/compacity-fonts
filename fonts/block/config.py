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

import psMat, math
import configure as c

# this is a magic number but i do not want to spend too much time on this until
# i rework whole build system
#
# it makes the characters overlap a bit so it renders better, this may work
# even better if done in the actual template of blocks
CH_VECTOR = psMat.compose(psMat.scale(1.03125), psMat.translate(4))

def letters(font):
    LETTERS = {
        "a": b(r'  # ||    ', CH_VECTOR),
        "b": b(r'  # || #  ', CH_VECTOR),
        "c": b(r'    || ## ', CH_VECTOR),
        "d": b(r' ## ||    ', CH_VECTOR),
        "e": b(r' #  ||    ', CH_VECTOR),
        "f": b(r'### ||    ', CH_VECTOR),
        "g": b(r'    || #  ', CH_VECTOR),
        "h": b(r' ## || #  ', CH_VECTOR),
        "i": b(r'# # ||    ', CH_VECTOR),
        "j": b(r'# # || ## ', CH_VECTOR),
        "k": b(r' #  ||  # ', CH_VECTOR),
        "l": b(r' ## || ## ', CH_VECTOR),
        "m": b(r'  # || ###', CH_VECTOR),
        "n": b(r'  # || # #', CH_VECTOR),
        "o": b(r'#   ||    ', CH_VECTOR),
        "p": b(r'##  ||    ', CH_VECTOR),
        "q": b(r' ## || ###', CH_VECTOR),
        "r": b(r'    ||  # ', CH_VECTOR),
        "s": b(r'    ||  ##', CH_VECTOR),
        "t": b(r'    || ###', CH_VECTOR),
        "u": b(r'##  ||  ##', CH_VECTOR),
        "v": b(r'##  || ## ', CH_VECTOR),
        "w": b(r'##  || ###', CH_VECTOR),
        "x": b(r'### || ## ', CH_VECTOR),
        "y": b(r' ## || ###', CH_VECTOR),
        "z": b(r'# # || ###', CH_VECTOR),
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

    # TODO this should also use CH_VECTOR but it requires too much code and im
    # lazy as im gonna rework it anyways

    # add the glyphs
    for k, v in NUMBERS.items():
        new_glyph(font, k, width=CHAR_WIDTH, refs=v)

def special(font):
    """Configures special characters, that have varying width and function"""
    ## ZERO WIDTH ##
    # TODO: add almost all symbols here until they are recreated to fit
    for i in list(r';:-`—@#$%^&*~/\\|_=+~`<>'):
        new_glyph(font, i, width=0, color=0xb3b3b3)

    ## OTHER ##
    space_width = CHAR_WIDTH * 2

    new_glyph(font, None, name='one-width-space', width=CHAR_WIDTH)
    new_glyph(font, ' ', width=space_width)
    new_glyph(font, '.', refs=b('         #', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*5)

    new_glyph(font, ',', refs=b('        ##', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)
    new_glyph(font, '!', refs=b('### ## # #', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)
    new_glyph(font, '?', refs=b('# # ## ###', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)

    # make all quotes the same
    for i in '“”"‘’\'':
        new_glyph(font, i, refs=b('##        ', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*3)

    for i in '({[':
        new_glyph(font, i, refs=b('### ## ###', psMat.translate(CHAR_WIDTH, 0))
                            +   b('#         ', psMat.translate(CHAR_WIDTH * 2, 0)), width=CHAR_WIDTH*4)

    for i in ')]}':
        new_glyph(font, i, refs=b('### ## ###', psMat.translate(CHAR_WIDTH*2, 0))
                            +   b('#         ', psMat.translate(CHAR_WIDTH, 0)), width=CHAR_WIDTH*4)

    new_glyph(font, None, refs=b('    ||    ', psMat.scale(2, 1)), name='blockspace', width=space_width)

def configure(font):
    """The function ran by configure script"""
    letters(font)
    numbers(font)
    special(font)

