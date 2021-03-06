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
"""Really simple logging code for convenience"""

def info(msg, *args, **kwargs):
    print(msg, *args, **kwargs)

def warn(msg, *args, **kwargs):
    print(':: ' + msg, *args, **kwargs)

def erro(msg, *args, **kwargs):
    print('!! ' + msg, *args, **kwargs)
