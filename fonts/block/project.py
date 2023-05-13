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

PROJECT_FILE = 'block.sfd'
PROJECT_FAMILY_NAME = 'Compacity Block'
PROJECT_VERSION = '0.2'

FEATURES_DIR = 'features'
FEATURE_BLOCKSPACE = 'blockspace.fea'

# which formats to build
FORMATS = ['ttf']

# flags used to change the font but be able to mix and match features
class Options(Flag):
    NONE = 0

    # makes the separator line invisible, may be harder to read
    NOLINE = auto()

    # makes the separator line continue between letters so sentences are one,
    # continuous block
    BLOCKSPACE = auto()

Variant = namedtuple('Variant', ['suffix', 'options', 'description'])

VARIANTS = [
    Variant(
        '',
        Options.BLOCKSPACE,
        'Original Compacity Block with words being attached together using the separator line'),
    Variant(
        'Separated',
        Options.NONE,
        'Variant with words being separated in a sentence'),
    Variant(
        'No Line',
        Options.NOLINE,
        'Variant without the separator line')
]
