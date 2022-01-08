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
# generate.py: Script that generates the glyphs

from xml.dom.minidom import parse, Node
import os, sys, string

TEMPLATE_FILE = 'template.svg'
OUTPUT_DIR = 'build'
GLYPH_OUTPUT_DIR = 'glyphs'
DIGITS_GROUP_ID = 'digits'

def generate_assets():
    # TODO: remove the built glyphs or just check if there are any so there arent
    # any issues introduced by old generated glyphs
    os.makedirs(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR))

    print('Generating glyphs')

    template = parse(TEMPLATE_FILE)

    # remove comments and newlines, they are evil
    def walk_n_filter(parent):
        if parent.childNodes:
            for child in list(parent.childNodes):
                if child.nodeType in [Node.TEXT_NODE, Node.COMMENT_NODE]:
                    child.parentNode.removeChild(child)
                    continue
                walk_n_filter(child)
    walk_n_filter(template)

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

        for i, child in enumerate(digit_group):
            if i != x:
                digit_group[i].parentNode.removeChild(digit_group[i])

        return doc

    digits = None

    # find the digits group
    for g in groups:
        name = g.getAttribute('name')
        if (name == DIGITS_GROUP_ID):
            digits = g
            break
    else:
        print('Error: digits group not found')

    num_of_digits = len(digits.childNodes)

    for i in range(num_of_digits):
        with open(os.path.join(OUTPUT_DIR, GLYPH_OUTPUT_DIR, str(i) + '.svg'), 'w') as file:
            file.write(template_digit(i, num_of_digits).toxml())

if __name__ == '__main__':
    generate_assets()
