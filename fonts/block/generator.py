#!/usr/bin/env python3
# compacity-fonts
#
# Copyright 2023 Aleksandar Radivojevic
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# generator.py: generator script for outlines for block font
# requires drawsvg

import pathlib
_CURR_DIR = pathlib.Path(__file__).parent.resolve()

ASSETS_DIR = _CURR_DIR / 'out'
NAME_FORMAT = '{index}.svg'

# name prefix for the block segments
BBLOCK = 'bblock.'
BLOCK_COUNT = 8
BLOCK_WIDTH = 100
BLOCK_HEIGHT = 100
LINE_W = BLOCK_WIDTH
LINE_H = BLOCK_HEIGHT / 2

# add overlap
OVERLAP_W = 4
OVERLAP_H = 0

def _generate_assets():
    # drawsvg is intentionally here cause everything else uses fontforge python
    # and dependencies cannot be installed there
    # this does not need to be called all the time anyways
    try:
        import drawsvg as dsvg
    except ImportError:
        print("Error: generator requires 'drawsvg' package")

        import sys
        sys.exit(1)

    import os

    # make the directories ignore existing
    os.makedirs(ASSETS_DIR, exist_ok=True)

    for i in range(BLOCK_COUNT):
        d = dsvg.Drawing(BLOCK_WIDTH, 1000) # TODO da fuck is this???
        #d = dsvg.Drawing(BLOCK_WIDTH, BLOCK_HEIGHT * BLOCK_COUNT)
        d.append(dsvg.Rectangle(0, BLOCK_HEIGHT * i, BLOCK_WIDTH + OVERLAP_W, BLOCK_HEIGHT + OVERLAP_H, fill='#000000'))
        d.save_svg(os.path.join(ASSETS_DIR, NAME_FORMAT.format(index=i + 1)))

    # generate the line
    d = dsvg.Drawing(BLOCK_WIDTH, BLOCK_HEIGHT * BLOCK_COUNT)
    d.append(dsvg.Rectangle(0, (BLOCK_HEIGHT * 4) - LINE_H / 2, LINE_W + OVERLAP_W, LINE_H, fill='#000000'))
    d.save_svg(os.path.join(ASSETS_DIR, NAME_FORMAT.format(index=0)))

if __name__ == '__main__':
    _generate_assets()
