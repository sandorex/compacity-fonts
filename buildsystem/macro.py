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
"""Common logic for font build scripts"""

try:
    import fontforge
except ImportError as ex:
    print('This module requires fontforge')
    raise

from typing import List, Optional, Callable, Any
from . import builder, logger as log, templater

import os, time, importlib

def configure(curdir: Any, project_file: str, user_project_file: Optional[str], output_dir: str, assets_output_dir: str, *, use_config_file: bool=True, project_save_prefix: str='', pre_configure: Callable[[Any], None]=None, post_configure: Optional[Callable[[Any], None]]=None):
    """Configure script main macro"""

    font = fontforge.open(os.path.join(curdir, project_file))
    log.info(f'Configuring project {font.fullname} {font.version}')

    if pre_configure is not None:
        pre_configure(font)

    if use_config_file:
        # NOTE: intentionally not catching the possible exception
        config = importlib.import_module('config', package=None)
        config.configure(font)

    if post_configure is not None:
        post_configure(font)

    # TODO: remove the last line and update the configured on so the comment
    # can contain any information without being overwritten
    font.comment = f'Last configured on {time.ctime()}'
    font.save()

    if user_project_file:
        try:
            user_config = importlib.import_module('user_config', package=None)
        except ImportError:
            user_config = None

        if user_config is not None:
            log.info('Configuring user modified project')

            # set font name and such only when first making the project to allow
            # the user to change anything without it being overwritten
            if not os.path.exists(os.path.join(curdir, user_project_file)):
                log.info('User project file does not exist, creating it from the regular one')

                user_font = font

                # used as font name when picking fonts
                user_font.familyname = user_font.familyname + ' (M)'

                # human readable name, but i do not know the difference compared to familyname
                user_font.fullname = user_font.fullname + ' (M)'

                # used when exporting the font
                user_font.default_base_filename = user_font.default_base_filename + '-user-mod'
            else:
                # only configure if the project already exists
                user_font = fontforge.open(os.path.join(curdir, user_project_file))

                if pre_configure is not None:
                    pre_configure(user_font)

                user_config.configure(user_font)

                if post_configure is not None:
                    post_configure(user_font)

            # only visible in the fontforge i think
            user_font.comment = f'USER MODIFIED\nLast configured on {time.ctime()}'
            user_font.save()

def generate(curdir: Any, output_dir: str, assets_output_dir: str, assets_dir: str, *, process_user_config: bool=True, template_files=[], fn: Optional[Callable[[], None]]=None):
    """Generate script main macro"""

    output_dir = os.path.join(curdir, output_dir, assets_output_dir)

    log.info('Generating assets')
    log.info(f"Output directory is set to '{output_dir}'")

    if os.path.exists(output_dir):
        log.warn('Output directory already exists, existing files will not be deleted but may be overwritten!')

    # ensure the output dir exists
    os.makedirs(output_dir, exist_ok=True)

    if fn is not None:
        fn()

    if template_files:
        log.info('Generating assets from template files')

        for file in template_files:
            if file:
                templater.template_svg(os.path.join(curdir, assets_dir, file), output_dir)

    if process_user_config:
        try:
            user_config = importlib.import_module('user_config', package=None)
        except ImportError:
            user_config = None

        if user_config is not None:
            log.info('Generating user assets')
            user_config.generate(str(curdir), output_dir)

def build(curdir: Any, output_dir: str, project_file: str, user_project_file: Optional[str], formats: List[str]):
    """Build script main macro"""

    log.info(f"Using FontForge {fontforge.version()}")
    log.info('Formats enabled:')
    for i in formats:
        print(f'- {i}')
    print()

    font = fontforge.open(os.path.join(curdir, project_file))

    log.info(f"Exporting font '{font.fullname}' version {font.version}")
    builder.export_font(font, os.path.join(curdir, output_dir), formats)

    if user_project_file and os.path.exists(os.path.join(curdir, user_project_file)):
        user_font = fontforge.open(os.path.join(curdir, user_project_file))
        log.info('Exporting user modified font')
        builder.export_font(user_font, os.path.join(curdir, user_project_file), formats)
