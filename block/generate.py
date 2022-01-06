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
# generate.py: Script to generate the project files

from xml.dom.minidom import parse, Node
import os, sys, string
import fontforge, psMat

# === OPTIONS === #

FONT_VERSION = '0.1'
FONT_NAME = 'Block'
FONT_FAMILY = 'Compacity'
TEMPLATE_FILE = 'template.svg'
OUTPUT_DIR = 'build'
GLYPH_OUTPUT_DIR = 'generated-glyphs'
OUTPUT_FILE_FORMAT = '{}' # '.svg' is appended, parameter is the number
DIGITS_GROUP_ID = 'digits'
DEBUG_GROUP_ID = 'debug'
FONT_EM = 1024
CHAR_WIDTH = 128

# === THE CODE === #

os.makedirs(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR), exist_ok=True)

def generate_assets():
    template = parse(TEMPLATE_FILE)
    groups = template.getElementsByTagName('g')

    def template_digit(x, n):
        doc = template.cloneNode(True)
        digit_group = None
        groups = doc.getElementsByTagName('g')
        for i in groups:
            if i.getAttribute('name') == DIGITS_GROUP_ID:
                digit_group = list(i.childNodes)
                break
        else:
            print('Error: could not find the digits group "{}"'.format(DIGITS_GROUP_ID))
            sys.exit(1)

        binary = format(x % pow(2, n), 'b').zfill(n)
        for i, b in enumerate(binary):
            if b == '0' or b == None:
                digit_group[i].parentNode.removeChild(digit_group[i])

        return doc

    digits = None

    # remove the debug group
    for g in groups:
        name = g.getAttribute('name')
        if (name == DEBUG_GROUP_ID):
            g.parentNode.removeChild(g)
        elif (name == DIGITS_GROUP_ID):
            digits = g

    # remove comments and newlines, they are evil
    def walk_n_filter(parent):
        if parent.childNodes:
            for child in list(parent.childNodes):
                if child.nodeType in [Node.TEXT_NODE, Node.COMMENT_NODE]:
                    child.parentNode.removeChild(child)
                    continue
                walk_n_filter(child)
    walk_n_filter(template)

    # TODO: FIXME: this could probably be nicer
    num_of_digits = len([i for i in digits.childNodes if i.nodeType != Node.TEXT_NODE])
    maximum_value = pow(2, num_of_digits) - 1

    del digits

    print('digits:', num_of_digits)
    print('maximum value:', maximum_value)
    print('outputting to: "{}"'.format(os.path.join(os.curdir, OUTPUT_DIR)))

    for i in range(maximum_value + 1):
        with open(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR, OUTPUT_FILE_FORMAT.format(i) + '.svg'), 'w') as file:
            file.write(template_digit(i, num_of_digits).toxml())

def generate_project():
    font = fontforge.font()
    font.version = FONT_VERSION
    font.fontname = FONT_NAME
    font.familyname = FONT_FAMILY
    font.fullname = FONT_FAMILY + ' ' + FONT_NAME
    font.copyright = 'Copyright 2022 Aleksandar Radivojević'
    font.fontlog = 'Compact font made to save space and for fun.. mostly fun'
    font.em = FONT_EM

    def new_char(ch, outline=None, width=CHAR_WIDTH):
        char = font.createChar(ord(ch))
        char.width = width
        if outline is not None: # TODO: check if file exists
            char.importOutlines(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR, str(outline) + '.svg'))

        char.removeOverlap() # important

        return char

    # NOTE: for testing only! proper layout will be done at later date
    for i, c in enumerate(string.ascii_uppercase, 2):
        new_char(c, i)

    for i, c in enumerate(string.ascii_lowercase, 2 + len(string.ascii_uppercase)):
        new_char(c, i)

    # special characters
    space = new_char(' ', 0)
    space.transform(psMat.scale(2, 1)) # double the width of space

    new_char(',', width=CHAR_WIDTH * 2)

    font.save(os.path.join(OUTPUT_DIR, FONT_NAME + '.sfd')) # create project
    font.generate(os.path.join(OUTPUT_DIR, FONT_NAME + '.ttf')) # export ttf

# TODO: process some arguments or use some kind of build system..
if __name__ == '__main__':
    generate_assets()
    generate_project()
