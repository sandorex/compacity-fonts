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
#
# config.py: dynamic configuration file for the font

import os

from . import generator as g
from builder import font

# TODO add translate to this function, maybe also scale...
def block(x: str):
    x = x.replace(' ', '')

    top = x[:3]
    middle = x[3:5]
    bottom = x[5:]

    blocks = []

    for i in range(3):
        if top[i] != ' ':
            blocks.append(i)

    if middle == '||':
        blocks.append(0)
    else:
        for i in range(2):
            if middle[i] != ' ':
                blocks.append(3 + i)

    for i in range(3):
        if bottom[i] != ' ':
            blocks.append(i)

    # TODO g.OUTPUT_DIR may need to be set to absolute path
    return [ os.path.join(g.OUTPUT_DIR, g.NAME_FORMAT.format(index=i)) for i in blocks ]

def gen(font: font.Font):
    ## LETTERS ##
    LETTERS = {}

    LETTERS['a'] = '  # ||    '
    LETTERS['b'] = '  # || #  '
    LETTERS['c'] = '    || ## '
    LETTERS['d'] = ' ## ||    '
    LETTERS['e'] = ' #  ||    '
    LETTERS['f'] = '### ||    '
    LETTERS['g'] = '    || #  '
    LETTERS['h'] = ' ## || #  '
    LETTERS['i'] = '# # ||    '
    LETTERS['j'] = '# # || ## '
    LETTERS['k'] = ' #  ||  # '
    LETTERS['l'] = ' ## || ## '
    LETTERS['m'] = '  # || ###'
    LETTERS['n'] = '  # || # #'
    LETTERS['o'] = '#   ||    '
    LETTERS['p'] = '##  ||    '
    LETTERS['q'] = ' ## || ###'
    LETTERS['r'] = '    ||  # '
    LETTERS['s'] = '    ||  ##'
    LETTERS['t'] = '    || ###'
    LETTERS['u'] = '##  ||  ##'
    LETTERS['v'] = '##  || ## '
    LETTERS['w'] = '##  || ###'
    LETTERS['x'] = '### || ## '
    LETTERS['y'] = ' ## || ###'
    LETTERS['z'] = '# # || ###'

    # NOTE: add extra letters here

    # uppercase letters are gonna be the same
    for key in dict(LETTERS).keys:
        LETTERS[key.upper()] = LETTERS[key]

    for k, v in LETTERS.items():
        font.glyph().char(k) \
                    .clear() \
                    .width(g.BLOCK_SIZE) \
                    .refs(block(v)) \
                    .color(0xd97dfa) \
                    .set_unlink_overlap_on_save()

    ## NUMBERS ##
    NUMBERS = {}

    NUMBERS['0'] = '#        #'
    NUMBERS['1'] = '#       ##'
    NUMBERS['2'] = '#       # '
    NUMBERS['3'] = '#       ##'
    NUMBERS['4'] = '#      #  '
    NUMBERS['5'] = '#      # #'
    NUMBERS['6'] = '#      ## '
    NUMBERS['7'] = '#      ###'
    NUMBERS['8'] = '#     #   '
    NUMBERS['9'] = '#     #  #'

    for k, v in LETTERS.items():
        font.glyph().char(k) \
                    .clear() \
                    .width(g.BLOCK_SIZE) \
                    .refs(block(v)) \
                    .color(0x87dbfa) \
                    .set_unlink_overlap_on_save()

    # these characters wont be rendered at all
    # TODO maybe add one small character that can indicate that there are useless
    # characters there
    ZERO_WIDTH = r';:-`—@#$%^&*~/\\|_=+~`<>'

    for k in ZERO_WIDTH:
        font.glyph().char(k) \
                    .clear() \
                    .width(0) \
                    .color(0x3b0f1e)

    ## SYMBOLS ##
    symbol_color = 0xdede59

    font.glyph().name('one-width-space') \
                .clear() \
                .width(g.BLOCK_SIZE) \
                .color(symbol_color)

    font.glyph().char(' ') \
                .clear() \
                .width(g.BLOCK_SIZE * 2) \
                .color(symbol_color)

    font.glyph().char('.') \
                .clear() \
                .refs(block('         #')) \
                .width(g.BLOCK_SIZE * 5) \
                .color(symbol_color)

    font.glyph().char(',') \
                .clear() \
                .refs(block('        ##')) \
                .width(g.BLOCK_SIZE * 3) \
                .color(symbol_color)

