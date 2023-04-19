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
"""Everything that has to do with the font"""

import fontforge
import os

from typing import Union, Any

class Font:
    """Wrapper around fontforge Font object"""

    def __init__(self, font):
        self.font = font

    @staticmethod
    def open(path) -> 'Font':
        return fontforge.open(path)

    def export(self, output_dir, format_='ttf'):
        # allows pathlib.Path
        output_dir = str(output_dir)

        # make sure the path exists
        os.makedirs(output_dir, exist_ok=True)

        font.generate(os.path.join(output_dir, font.default_base_filename + '.' + format_))

    def new_glyph(self, x: Union[int, str]) -> Any:
        if isinstance(x, int):
            glyph = self.font.createChar(x)
        elif isinstance(x, str):
            if len(x) > 1:
                glyph = self.font.createChar(-1, x)
            else:
                # convert first char to int
                glyph = self.font.createChar(ord(x[0]))
        else:
            raise RuntimeError('Invalid arguments')

        glyph.changed = True

        return glyph


