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

# TODO: move versioning to python and update the project file

PROJECT_FILE = 'block.sfd'
FORMATS = [ 'ttf' ]

class Options(Flag):
    NONE = 0

    # there is no line separating top and bottom half, improves rendering in
    # many cases, unfortunate but needed fix when not used to render pdfs
    NOLINE = auto()

VARIANTS = [
    # this is the default with no suffix
    ('', Options.NONE),

    # add variants here
    ('NL', Options.NOLINE)
]
