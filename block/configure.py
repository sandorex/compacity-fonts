#!/usr/bin/env python3
# compacity-fonts block
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
# configure.py: Configures font project for fontforge

import fontforge, os, string, sys, glob, psMat, json

from generate import OUTPUT_DIR, GLYPH_OUTPUT_DIR
import config

PROJECT_FILE = 'block.sfd'
CHAR_WIDTH = 128

BLOCK_LINE = 'block-line'
BLOCK_U1 = 'block-u1'
BLOCK_U2 = 'block-u2'
BLOCK_U3 = 'block-u3'
BLOCK_C1 = 'block-c1'
BLOCK_C2 = 'block-c2'
BLOCK_D1 = 'block-d1'
BLOCK_D2 = 'block-d2'
BLOCK_D3 = 'block-d3'

# names of the svgs for block pieces
BLOCKS = [
    (BLOCK_LINE, '0.svg'),

    (BLOCK_U1, '1.svg'),
    (BLOCK_U2, '2.svg'),
    (BLOCK_U3, '3.svg'),

    (BLOCK_C1, '7.svg'),
    (BLOCK_C2, '8.svg'),

    (BLOCK_D1, '4.svg'),
    (BLOCK_D2, '5.svg'),
    (BLOCK_D3, '6.svg'),
]

# aliases
BLOCK_0 = BLOCK_LINE
BLOCK_1 = BLOCK_U1
BLOCK_2 = BLOCK_U2
BLOCK_3 = BLOCK_U3
BLOCK_4 = BLOCK_C1
BLOCK_5 = BLOCK_C2
BLOCK_6 = BLOCK_D1
BLOCK_7 = BLOCK_D2
BLOCK_8 = BLOCK_D3

def configure():
    font = fontforge.open(PROJECT_FILE)

    print("Configuring font '{} {}'".format(font.familyname, font.version))

    path = os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR)

    def glyph_path(index):
        return os.path.join(path, str(index) + '.svg')

    def new_char(ch=None, outline=None, *, name=None, width=CHAR_WIDTH, references=None):
        if ch is None:
            char = font.createChar(-1, name)
        else:
            # TODO: FIXME: this is a mess...
            if name is not None:
                char = font.createChar(ord(ch), name)
            else:
                char = font.createChar(ord(ch))

        char.clear() # without this it may put references over outlines.. ugh
        char.width = width

        if outline is not None:
            if os.path.exists(outline):
                char.importOutlines(outline)
            else:
                print('Error: glyph outline "{}" not found'.format(outline))
                sys.exit(1)

        if references is not None:
            for i in references:
                # TODO: check if references are valid
                if isinstance(i, tuple):
                    char.addReference(i[0], i[1])
                else:
                    char.addReference(i)

        # TODO: try char.unlinkRmOvrlpSave = True
        char.unlinkRmOvrlpSave = True
        # char.removeOverlap() # important

        return char

    # add all the base block glyphs
    for ch, filename in BLOCKS:
        new_char(name=ch, outline=os.path.join(path, filename))

    ### GLYPHS ###
    new_char(' ', width=CHAR_WIDTH*2)
    new_char(',', width=CHAR_WIDTH * 2)
    new_char('.', width=CHAR_WIDTH * 4)
    new_char('"', width=CHAR_WIDTH*3, references=[
        ('block-u1', psMat.translate(CHAR_WIDTH, 0)),
        ('block-d3', psMat.translate(CHAR_WIDTH, 0)),
    ])
    new_char('!', width=CHAR_WIDTH*3, references=[
        ('block-u1', psMat.translate(CHAR_WIDTH, 0)),
        ('block-u2', psMat.translate(CHAR_WIDTH, 0)),
        ('block-u3', psMat.translate(CHAR_WIDTH, 0)),
        ('block-c1', psMat.translate(CHAR_WIDTH, 0)),
        ('block-c2', psMat.translate(CHAR_WIDTH, 0)),
        ('block-d1', psMat.translate(CHAR_WIDTH, 0)),

        ('block-d3', psMat.translate(CHAR_WIDTH, 0)),
    ])

    ### SPECIAL GLYPHS ###
    new_char(name='blockspace', width=CHAR_WIDTH*2, references=[
        ('block-line', psMat.scale(2, 1))
    ])

    # load layout
    bindings, special = config.generate()

    for ch, refs in bindings.items():
        new_char(ch, references=refs)

    for name, refs in special.items():
        new_char(name=name, references=refs)

    # save to new project just in case it has fcked it up for some reason
    font.save('new.' + PROJECT_FILE)

if __name__ == '__main__':
    configure()

