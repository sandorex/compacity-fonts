#!/usr/bin/env python3
# compacity-fonts
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
"""Code for exporting FontForge fonts"""

try:
    import fontforge
except ImportError as ex:
    print('This module requires fontforge')
    raise

import os, errno, time

from pathlib import Path
from typing import Any, List, Optional, Tuple, Union

def export_font(font, output_dir, formats=['ttf'], name_format='{basename}'):
    """Exports font as `{basename}.{extension}` for each format selected

    Note that spaces are replaced by dashes `-`
    """

    # allows pathlib.Path
    output_dir = str(output_dir)

    # make sure the path exists
    os.makedirs(output_dir, exist_ok=True)

    for ext in formats:
        font.generate(os.path.join(output_dir, name_format.format(basename=font.default_base_filename, ext=ext) + '.' + ext))

def new_glyph(font,
              x: Union[int, str, None],
              *,
              name: Optional[str]=None,
              width: Optional[int]=None,
              outline_path: Union[str, Path, None]=None,
              refs: Optional[List[Union[str, Tuple[str, Any]]]]=None,
              color: Optional[int]=None) -> Any:
    """Creates a new glyph ... TODO"""

    if isinstance(x, int):
        glyph = font.createChar(x)
    elif isinstance(x, str) and x:
        if len(x) > 1:
            x = x[0] # just take the first character

        glyph = font.createChar(ord(x))
    elif x is None:
        if name is None:
            raise TypeError('Name must be provided when x is None')

        glyph = font.createChar(-1, name)
    else:
        raise TypeError('Invalid arguments provided')

    # test file path before modifying the gylph
    if outline_path is not None:
        outline_path = str(outline_path)

        if not os.path.exists(outline_path):
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), outline_path)

    glyph.clear()
    glyph.unlinkRmOvrlpSave = True

    if name:
        glyph.glyphname = name

    if width is not None:
        glyph.width = width

    if outline_path is not None:
        glyph.importOutlines(outline_path)

    if refs is not None and refs:
        # TODO check if ref exists / is valid
        for i in refs:
            if isinstance(i, tuple):
                glyph.addReference(i[0], i[1])
            else:
                glyph.addReference(i)

    if color is not None:
        glyph.color = color
    else:
        glyph.color = -1 # the default color

    glyph.changed = True
    glyph.comment = 'AUTO CONFIGURED GLYPH\nDO NOT EDIT'

    return glyph
