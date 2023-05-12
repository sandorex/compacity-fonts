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

from typing import Any, List

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

    def outline(self, path, verbatim=True, **kwargs):
        if not os.path.exists(path):
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

        # i spent 3 weeks trying to fix the importing of SVGs and it kept
        # giving me weird values and moving things around like it's scaling and
        # i finally found that the culprit is this damn scale option that is ON
        # BY FUCKING DEFAULT AND I SPENT FUCKING THREE WEEKS DEBUGGING IT AND
        # ALMOST SCRAPPED THE WHOLE DAMN PROJECT JUST CAUSE SOMEONE THOUGHT IT
        # WAS A GOOD IDEA TO SCALE SVGS BY DEFAULT
        #
        # relevant docs page: https://fontforge.org/docs/scripting/python/fontforge.html#fontforge.glyph.importOutlines
        self.glyph.importOutlines(str(path), scale=not verbatim, simplify=not verbatim, **kwargs)

        return self

    def ref(self, ref: Any):
        self.glyph.addReference(ref)

        return self

    def refs(self, ref: List[Any]):
        for i in ref:
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

    def transform(self, matrix, round_=False):
        flags = ()

        if round_:
            flags = ('round')

        self.glyph.transform(matrix, flags)

        return self

class Font:
    """Wrapper around fontforge Font object"""

    def __init__(self, font=None):
        if font:
            self.font = font
        else:
            self.font = fontforge.font()

    @staticmethod
    def open(path) -> 'Font':
        # str allows using pathlib.Path
        return Font(fontforge.open(str(path)))

    @property
    def computer_name(self):
        return self.font.fontname

    @computer_name.setter
    def computer_name(self, value):
        self.font.fontname = value

    @property
    def family_name(self):
        return self.font.familyname

    @family_name.setter
    def family_name(self, value):
        self.font.familyname = value

    @property
    def human_name(self):
        return self.font.fullname

    @human_name.setter
    def human_name(self, value):
        self.font.fullname = value

    @property
    def comment(self):
        return self.font.comment

    @comment.setter
    def comment(self, value):
        self.font.comment = value

    @property
    def version(self) -> str:
        return self.font.version

    @version.setter
    def version(self, value) -> str:
        self.font.version = value

    def export(self, output_dir, format_='ttf'):
        # allows pathlib.Path
        output_dir = str(output_dir)

        # make sure the path exists
        os.makedirs(output_dir, exist_ok=True)

        self.font.generate(os.path.join(output_dir, self.font.default_base_filename + '.' + format_))

    @property
    def export_filename(self) -> str:
        return self.font.default_base_filename

    @export_filename.setter
    def export_filename(self, value):
        self.font.default_base_filename = value

    def save(self):
        # TODO: only update the last one to allow static comment
        self.font.comment = f'Last configured on {time.ctime()}'
        self.font.save()

    def close(self):
        self.font.close()

    def glyph(self) -> GlyphBuilder:
        return GlyphBuilder(self)

    def merge_feature(self, path, ignore_missing_glyphs=False):
        """Merges adobe features file into the font"""
        self.font.mergeFeature(str(path), ignore_missing_glyphs)
