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

import psMat
import logging
import collections

import generator
import project as p
from builder import font

SYMBOL_COLOR = 0xdede59

# returns names of glyphs not file paths
def block(x: str):
    '''Transforms a string into list of base glyph names'''
    blocks = []

    top = x[:3]
    middle = x[4:6]
    bottom = x[7:]

    for i in range(3):
        if top[i] != ' ':
            blocks.append(1 + i)

    if middle == '||':
        blocks.append(0)
    else:
        for i in range(2):
            if middle[i] != ' ':
                blocks.append(4 + i)

    for i in range(3):
        if bottom[i] != ' ':
            blocks.append(6 + i)

    return [ g.BBLOCK + str(x) for x in blocks ]

def defaults(glyph: font.GlyphBuilder):
    '''Sets defaults for each glyph, run with GlyphBuilder.do(..)'''
    glyph.set_unlink_overlap_on_save() \
        .comment('AUTOGENERATED DO NOT EDIT')

    glyph.glyph.removeOverlap()

def static_gen(font: font.Font):
    '''Modifies the font'''

    for i in range(g.BLOCK_COUNT + 1):
        font.glyph().name(g.BBLOCK + str(i)) \
                    .clear() \
                    .outline(g.OUTPUT_DIR / g.NAME_FORMAT.format(index=i)) \
                    .width(0) \
                    .color(0xf22929)

    ## LETTERS ##
    LETTERS = {}

    LETTERS['A'] = '  # ||    '
    LETTERS['B'] = '  # || #  '
    LETTERS['C'] = '    || ## '
    LETTERS['D'] = '    ||  # '
    LETTERS['E'] = ' #  ||    '
    LETTERS['F'] = '# # ||    '
    LETTERS['G'] = '    || #  '
    LETTERS['H'] = ' ## || #  '
    LETTERS['I'] = '### || ###'
    LETTERS['J'] = '### || ## '
    LETTERS['K'] = ' #  ||  # '
    LETTERS['L'] = ' ## || ## '
    LETTERS['M'] = '  # || ###'
    LETTERS['N'] = '  # || # #'
    LETTERS['O'] = '#   ||    '
    LETTERS['P'] = '##  ||    '
    LETTERS['Q'] = '#   ||   #'
    LETTERS['R'] = '### ||    '
    LETTERS['S'] = ' ## ||    '
    LETTERS['T'] = '    ||   #'
    LETTERS['U'] = '##  ||  ##'
    LETTERS['V'] = '    ||  ##'
    LETTERS['W'] = '    || ###'
    LETTERS['X'] = '# # || # #'
    LETTERS['Y'] = '# # || ###'
    LETTERS['Z'] = '#   || ###'

    # NOTE: add extra letters here

    # check if there are any duplicate keys just in case
    duplicates = [item for item, count in collections.Counter(LETTERS.values()).items() if count > 1]
    if duplicates:
        logging.warning(f"Duplicate letters found ({len(duplicates)})")

    # uppercase and lowercase letters are gonna be the same
    for key, value in dict(LETTERS).items():
        LETTERS[key.lower()] = value

    for k, v in LETTERS.items():
        font.glyph().char(k) \
                    .clear() \
                    .width(g.BLOCK_WIDTH) \
                    .refs(block(v)) \
                    .do(defaults) \
                    .color(0xd97dfa)

    ## NUMBERS ##
    NUMBERS = {}

    # TODO this is broken multiple digits are the same looking
    # TODO add calt that will change hex string 0xFF to this
    # generate numbers as it were binary
    for i in range(2 ** 8):
        binary = [' '] * 8
        for bit in range(8):
            if i & (1 << bit):
                binary[7 - bit] = '#'

        binary = '#' + ''.join(binary) + '#'
        NUMBERS[str(i)] = binary

    for k, v in NUMBERS.items():
        glyph = font.glyph()
        if len(k) == 1:
            glyph = glyph.char(k)
        else:
            glyph = glyph.name('dec' + k)

        glyph.clear() \
             .width(g.BLOCK_WIDTH) \
             .refs(block(v)) \
             .do(defaults) \
             .color(0x87dbfa)

    # these characters wont be rendered at all
    # TODO maybe add one small character that can indicate that there are
    # useless characters there
    ZERO_WIDTH = r';:-`—@#$%^&*~/\|_=+~`<>'

    for k in ZERO_WIDTH:
        font.glyph().char(k) \
                    .clear() \
                    .width(0) \
                    .do(defaults) \
                    .color(0x3b0f1e)

    ## SYMBOLS ##
    font.glyph().char(' ') \
                .clear() \
                .width(g.BLOCK_WIDTH * 2) \
                .do(defaults) \
                .color(SYMBOL_COLOR)

    font.glyph().char('.') \
                .clear() \
                .refs(block('         #')) \
                .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                .width(g.BLOCK_WIDTH * 5) \
                .do(defaults) \
                .color(SYMBOL_COLOR)

    font.glyph().char(',') \
                .clear() \
                .refs(block('        ##')) \
                .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                .width(g.BLOCK_WIDTH * 3) \
                .do(defaults) \
                .color(SYMBOL_COLOR)

    font.glyph().char('!') \
                .clear() \
                .refs(block('### ## # #')) \
                .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                .width(g.BLOCK_WIDTH * 3) \
                .do(defaults) \
                .color(SYMBOL_COLOR)

    font.glyph().char('?') \
                .clear() \
                .refs(block('# # ## ###')) \
                .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                .width(g.BLOCK_WIDTH * 3) \
                .do(defaults) \
                .color(SYMBOL_COLOR)

    for i in '“”"‘’\'':
        font.glyph().char(i) \
                    .clear() \
                    .refs(block('##         ')) \
                    .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                    .width(g.BLOCK_WIDTH * 3) \
                    .do(defaults) \
                    .color(SYMBOL_COLOR)

    for i in '({[':
        font.glyph().char(i) \
                    .clear() \
                    .refs(block('#         ')) \
                    .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                    .refs(block('### ## ###')) \
                    .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                    .width(g.BLOCK_WIDTH * 4) \
                    .do(defaults) \
                    .color(SYMBOL_COLOR)

    for i in ')]}':
        font.glyph().char(i) \
                    .clear() \
                    .refs(block('### ## ###')) \
                    .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                    .refs(block('         #')) \
                    .transform(psMat.translate(g.BLOCK_WIDTH, 0)) \
                    .width(g.BLOCK_WIDTH * 4) \
                    .do(defaults) \
                    .color(SYMBOL_COLOR)

def gen(font: font.Font, options):
    '''Modifies the font depending on the options provided'''

    # remove the line outline to make it invisible in variants
    if Options.NOLINE in options:
        font.glyph().name(g.BBLOCK + '0') \
                    .clear() \
                    .width(0) \
                    .do(defaults) \
                    .color(0xf22929)

    if Options.BLOCKSPACE in options:
        # this is the glyph that replaces space in variants with BLOCKSPACE
        font.glyph().name('blockspace') \
                    .clear() \
                    .refs(block('    ||    ')) \
                    .transform(psMat.scale(2, 1)) \
                    .width(g.BLOCK_WIDTH * 2) \
                    .do(defaults) \
                    .color(SYMBOL_COLOR)

        font.merge_feature(PROJECT_ROOT / p.FEATURES_DIR / p.FEATURE_BLOCKSPACE)

