#!/usr/bin/env python3
# compacity-fonts
#
# Copyright 2023 Aleksandar Radivojevic
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
# generator.py: generator script for outlines for block font
# requires drawsvg

OUTPUT_DIR = 'out'
NAME_FORMAT = '{index}.svg'

BLOCK_COUNT = 8
BLOCK_SIZE = 128
LINE_W = BLOCK_SIZE
LINE_H = BLOCK_SIZE / 2

# adds pixels to width and height so outlines overlap, renders better on most
# devices and applications
# should not cause blur on its own unlike psMat.scale()
OVERLAP = 2

def generate():
    import drawsvg as dsvg
    import os

    os.mkdir(OUTPUT_DIR)

    for i in range(BLOCK_COUNT):
        d = dsvg.Drawing(BLOCK_SIZE, BLOCK_SIZE * BLOCK_COUNT)
        d.append(dsvg.Rectangle(0, BLOCK_SIZE * i, BLOCK_SIZE + OVERLAP, BLOCK_SIZE + OVERLAP, fill='#000000'))
        d.save_svg(os.path.join(OUTPUT_DIR, NAME_FORMAT.format(index=i + 1)))

    # generate the line
    d = dsvg.Drawing(BLOCK_SIZE, BLOCK_SIZE * BLOCK_COUNT)
    d.append(dsvg.Rectangle(0, BLOCK_SIZE * 4, LINE_W + OVERLAP, LINE_H, fill='#000000'))
    d.save_svg(os.path.join(OUTPUT_DIR, NAME_FORMAT.format(index=0)))

if __name__ == '__main__':
    generate()
