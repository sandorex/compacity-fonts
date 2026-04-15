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

import logging
import copy
import tomllib

from builder.font import Font, GlyphBuilder
from . import BUILD_DIR, BBLOCK, BLOCK_COUNT, BLOCK_WIDTH, ASSETS_DIR, NAME_FORMAT, PROJECT_ROOT
from .config import Config, glyph_defaults, parse_block

PROJECT_FAMILY_NAME = 'Compacity Block'
PROJECT_VERSION = '0.2.1'

FEATURES_DIR = 'features'
FEATURE_BLOCKSPACE = PROJECT_ROOT / FEATURES_DIR / 'blockspace.fea'

logging.info(f"Building font '{PROJECT_FAMILY_NAME}' version {PROJECT_VERSION}")

for path in (PROJECT_ROOT / "variants").iterdir():
    if not path.is_file() or path.suffix != ".toml":
        continue

    try:
        with open(path, "rb") as fp:
            cfg = Config.load(fp)
    except Exception:
        print(f"Error loading the config '{path}'")
        raise

    font = Font()
    font.version = PROJECT_VERSION
    font.copyright = "?"

    font.computer_name = "CompacityBlock"
    font.family_name = "Compacity Block"
    font.human_name = font.family_name

    suffix = cfg.suffix
    if suffix:
        font.computer_name += '-' + suffix.replace(' ', '')
        font.family_name += '-' + suffix.replace(' ', '')
        font.human_name += ' ' + suffix

        logging.info(f"Building variant '{font.human_name}'")

    font.export_filename = font.computer_name

    # add base glyphs
    for i in range(BLOCK_COUNT + 1):
        font.glyph().name(BBLOCK + str(i)) \
                    .clear() \
                    .outline(ASSETS_DIR / NAME_FORMAT.format(index=i)) \
                    .width(0) \
                    .color(0xf22929)

    cfg.create_glyphs(font)

    line_separator = cfg.options["line_separator"]
    separate_words = cfg.options["separate_words"]

    # removes the line outline, making it invisible
    if not line_separator:
        font.glyph().name(BBLOCK + '0') \
                    .clear() \
                    .width(0) \
                    .color(0xf22929)

    # if enabled words will be connected with the line
    if not separate_words and line_separator:
        # this is the glyph that replaces space in variants with BLOCKSPACE
        font.glyph().name('blockspace') \
                    .clear() \
                    .refs(parse_block('    ||    ')) \
                    .transform(psMat.scale(2, 1)) \
                    .width(BLOCK_WIDTH * 2) \
                    .do(glyph_defaults) \
                    .color(0xf22929)

        font.merge_feature(FEATURE_BLOCKSPACE)

    # export each format defined
    for format_ in cfg.formats:
        font.export(BUILD_DIR, format_=format_)

    font.close()
