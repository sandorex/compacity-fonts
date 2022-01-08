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

import fontforge, os, string, sys, glob, psMat

from generate import OUTPUT_DIR, GLYPH_OUTPUT_DIR

PROJECT_FILE = 'block.sfd'
CHAR_WIDTH = 128

def configure():
    font = fontforge.open(PROJECT_FILE)

    print("Configuring font '{} {}'".format(font.familyname, font.version))

    def glyph_path(index):
        return os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR, str(index) + '.svg')

    def new_char(ch=None, outline=None, *, name=None, width=CHAR_WIDTH):
        if name is not None:
            char = font.createChar(-1, name)
        else:
            char = font.createChar(ord(ch))

        char.width = width

        if outline is not None:
            if os.path.exists(outline):
                char.importOutlines(outline)
            else:
                print('Error: glyph outline "{}" not found'.format(outline))
                sys.exit(1)

        char.removeOverlap() # important

        return char

    # add all the glyphs
    # for file in glob.glob(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR, '*.svg')):
    #     filename = os.path.splitext(os.path.basename(file))[0]
    #     new_char(name='blockx' + filename, outline=file)

    # TODO: optionally read from external file the values for characters
    # NOTE: for testing only! proper layout will be done at later date
    for i, c in enumerate(string.ascii_uppercase, 2):
        new_char(c, glyph_path(i))

    for i, c in enumerate(string.ascii_lowercase, 2 + len(string.ascii_uppercase)):
        new_char(c, glyph_path(i))

    # special characters

    # space is going to be double width for visibility
    new_char(' ', width=CHAR_WIDTH*2)
    new_char(name='blockspace', width=CHAR_WIDTH*2)

    # this is 2 times the width space
    new_char(',', width=CHAR_WIDTH * 2)

    # this is 4 times the width space
    new_char('.', width=CHAR_WIDTH * 4)

    # save to new project just in case it has fcked it up for some reason
    font.save('new.' + PROJECT_FILE)

if __name__ == '__main__':
    configure()

