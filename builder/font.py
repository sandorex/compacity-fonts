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
import errno
import time

from typing import Any, Tuple, List, Union

class GlyphBuilder:
    def __init__(self, font):
        self.font = font.font
        self.glyph = None

    def _defaults(self):
        '''Sets defaults for glyph'''
        self.glyph.color = -1
        self.glyph.changed = True

    def char(self, ch):
        if self.glyph is None:
            if isinstance(ch, int):
                self.glyph = self.font.createChar(ch)
            elif isinstance(ch, str):
                # convert first char to int
                self.glyph = self.font.createChar(ord(ch[0]))

            self._defaults()

        return self

    def name(self, name):
        if self.glyph is None:
            self.glyph = self.font.createChar(-1, name)

            self._defaults()
        else:
            self.glyph.name = name

        return self

    def clear(self):
        self.glyph.clear()

        return self

    def width(self, width: int):
        self.glyph.width = width

        return self

    def outline(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        self.glyph.importOutlines(str(path))

        return self

    def ref(self, ref: Any, transformation: Any = None):
        if transformation is not None:
            self.glyph.addReference(ref, transformation)
        else:
            self.glyph.addReference(ref)

        return self

    def refs(self, ref: List[Union[Any, Tuple[Any, Any]]]):
        for i in ref:
            if isinstance(i, tuple):
                self.ref(*i)
            else:
                self.ref(i)

        return self

    def color(self, color: int):
        self.glyph.color = color

        return self

    def comment(self, comment: str):
        self.glyph.comment = comment

        return self

    def set_unlink_overlap_on_save(self):
        self.glyph.unlinkRmOvrlpSave = True

        return self

    def do(self, fn):
        '''Do something with glyph itself'''
        fn(self)

        return self

class Font:
    """Wrapper around fontforge Font object"""

    def __init__(self, font):
        self.font = font

    @staticmethod
    def open(path) -> 'Font':
        # str allows using pathlib.Path
        return Font(fontforge.open(str(path)))

    @property
    def name(self) -> str:
        return self.font.fullname

    @property
    def version(self) -> str:
        return self.font.version

    def export(self, output_dir, format_='ttf'):
        # allows pathlib.Path
        output_dir = str(output_dir)

        # make sure the path exists
        os.makedirs(output_dir, exist_ok=True)

        self.font.generate(os.path.join(output_dir, self.font.default_base_filename + '.' + format_))

    def save(self):
        # TODO: only update the last one to allow static comment
        self.font.comment = f'Last configured on {time.ctime()}'
        self.font.save()

    def glyph(self) -> GlyphBuilder:
        return GlyphBuilder(self)

    def round(self):
        self.font.round()
