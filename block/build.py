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
# build.py: Builds the font into ttf and otf files

import fontforge, os, string, sys

from generate import OUTPUT_DIR
from configure import PROJECT_FILE

def build():
    font = fontforge.open(PROJECT_FILE)

    print("Building font '{} {}'".format(font.familyname, font.version))

    path = os.path.join(OUTPUT_DIR, font.familyname.lower().replace(' ', '-'))

    # export ttf
    font.generate(path + '.ttf')

    # woff doesn't export properly either..
    # font.generate(path + '.woff')

    # OTF is not looking quite right so it's disabled
    # font.generate(os.path.join(OUTPUT_DIR, font.fontname + '.otf')) # export otf

if __name__ == '__main__':
    build()

