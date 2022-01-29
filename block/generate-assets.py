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
# configure.py: Configures fontforge project

import os, sys
from pathlib import Path
CURDIR = Path(os.path.dirname(__file__))
sys.path.append(str(CURDIR.absolute().parent))

from buildsystem.templater import template_svg

import buildsystem.logger as log
import project as p

try:
    import user_config # type: ignore
except ImportError:
    user_config = None

if __name__ == '__main__':
    output_dir = CURDIR / p.OUTPUT_DIR / p.ASSETS_OUTPUT_DIR

    log.info('Generating assets')
    log.info(f"Output directory is set to '{output_dir}'")

    if os.path.exists(CURDIR / p.OUTPUT_DIR / p.ASSETS_OUTPUT_DIR):
        log.warn('Output directory already exists, existing files will not be deleted but may be overwritten!')

    # ensure the output dir exists
    os.makedirs(CURDIR / p.OUTPUT_DIR / p.ASSETS_OUTPUT_DIR, exist_ok=True)

    log.info('Generating assets from template file')

    template_svg(CURDIR / p.ASSETS_DIR / 'template.svg', output_dir)

    if user_config is not None:
        log.info('Generating user assets')
        user_config.generate(str(CURDIR), str(output_dir))
