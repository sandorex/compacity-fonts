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
# config.py: Dynamic configuration file for the font

import configure as c

def generate():
    bindings = {
        "a": [c.BLOCK_LINE, c.BLOCK_U1, c.BLOCK_U2],
        "b": [c.BLOCK_LINE, c.BLOCK_U1, c.BLOCK_D1],
        "c": [c.BLOCK_LINE, c.BLOCK_D1],
        "e": [c.BLOCK_LINE, c.BLOCK_U1]
        # TODO: the rest
    }

    special = {}

    ### generate numbers ###
    blocklist = [
        c.BLOCK_2,
        c.BLOCK_3,
        c.BLOCK_4,
        c.BLOCK_5,
        c.BLOCK_6,
        c.BLOCK_7,
    ]

    # digits above 9 don't exist as glyphs so they would be unused (TODO)
    for i, b in enumerate(map(lambda x: format(x, 'b').zfill(6), range(10))):
        blocks = [ c.BLOCK_U1, c.BLOCK_D3 ]
        for j, ch in enumerate(reversed(b)):
            if ch == '1':
                blocks.append(blocklist[j])

        if i >= 10:
            special[str(i)] = blocks
        else:
            bindings[str(i)] = blocks

    return bindings, special
