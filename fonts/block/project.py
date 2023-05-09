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

from enum import Flag, auto
from collections import namedtuple

# TODO: move versioning to python and update the project file

PROJECT_FILE = 'block.sfd'
FORMATS = [ 'ttf' ]

# flags used to change the font but be able to mix and match features
class Options(Flag):
    NONE = 0

    # makes the separator line invisible, may be harder to read
    NOLINE = auto()

    # separates all the characters in X axis, it's more cool than usueable tho
    SEPARATED = auto()

    # makes the separator line continue between letters so sentences are one,
    # continuous block
    SENTENCE_LINE = auto()

Variant = namedtuple('Variant', ['suffix', 'human_name', 'options', 'description'])

VARIANTS = [
    Variant(
        '',
        '',
        Options.SENTENCE_LINE,
        'Original Compacity Block with words being attached together using the separator line'),
    Variant(
        'WS',
        'Word Separated',
        Options.NONE,
        'Variant with words being separated in a sentence'),
    Variant(
        'NL',
        'No Separator Line',
        Options.NOLINE,
        'Variant without the separator line'),
    Variant(
        'S',
        'Sparse',
        Options.SEPARATED,
        'Variant with all characters being spaced out'),
    Variant(
        'S NL',
        'Sparse & No Separator Line',
        Options.SEPARATED | Options.NOLINE,
        'Variant with all characters being spaced out without separator line')
]
