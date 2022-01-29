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
"""Code for templating SVGs"""

from typing import List
from xml.dom.minidom import parse, Node, Document, Element

import os, errno

def _clean_dom(dom: Document):
    """Cleans a XML DOM of comments, empty lines, newlines"""
    def recursive_filter(parent):
        if parent.childNodes:
            for child in list(parent.childNodes):
                if child.nodeType in [Node.TEXT_NODE, Node.COMMENT_NODE] or child.getAttribute('name') == '@remove':
                    child.parentNode.removeChild(child)
                    continue

                recursive_filter(child)

    recursive_filter(dom)

def template_svg(template_file, output_dir, output_format=r'{}', *, prettyxml=False):
    """Templates the SVG file

    Group functions:
        `@unique`:
            exports SVGs with each containing ONLY one of children in this group

        `@combination`:
            exports SVGs with each combination of children in this group

    Other functions (used as name of any element):
        `@remove`:
            this element and it's children will be removed at start of processing

    ONLY ONE GROUP FUNCTION WILL BE PROCESSED

    Output format:
        format for the name of svgs, first parameter passed is index of the svg,

    Adding name to children in the group will make it the output file name

    WARNING: the function will not clear the output directly but will only overwrite files
    """

    # support pathlib.Path
    template_file = str(template_file)
    output_dir = str(output_dir)

    # ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(template_file):
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), template_file)

    orig_root: Document = parse(template_file)
    orig_dom: Element = orig_root.firstChild

    _clean_dom(orig_dom)

    svgs: List[Document] = []

    for g in orig_dom.getElementsByTagName('g'):
        name = g.getAttribute('name')
        length = len(g.childNodes)

        # unique, export a file for each element in the group
        if name == '@unique':
            for i in range(length):
                # copy the root
                copy_root: Document = orig_root.cloneNode(True)
                svgs.append(copy_root)

                copy_dom: Element = copy_root.firstChild

                # find the original group in the copy
                group_elem: Element = None
                for g in copy_dom.getElementsByTagName('g'):
                    if g.getAttribute('name') == '@unique':
                        group_elem = g
                        break
                else:
                    break
                    # print('error') # TODO

                children: List[Element] = list(group_elem.childNodes)

                for j in range(length):
                    # skip the one element
                    if j == i:
                        if children[j].hasAttribute('name'):
                            copy_dom.setAttribute('name', children[j].getAttribute('name'))
                            children[j].removeAttribute('name')

                        continue

                    # remove rest
                    group_elem.removeChild(children[j])
            break

        # binary exports each combination of elements in group in sequence like
        # the elements are binary digits with the first one being LSB
        elif name == '@binary':
            for i in range(pow(2, length) - 1):
                # copy the root
                copy_root: Document = orig_root.cloneNode(True)
                svgs.append(copy_root)

                copy_dom: Element = copy_root.firstChild

                # find the original group in the copy
                group_elem: Element = None
                for g in copy_dom.getElementsByTagName('g'):
                    if g.getAttribute('name') == '@binary':
                        group_elem = g
                        break
                else:
                    print('error') # TODO

                children: List[Element] = list(group_elem.childNodes)

                binary = format(i, 'b').zfill(length)
                for j, b in enumerate(binary):
                    if b == '0' or b == None:
                        group_elem.removeChild(children[j])
            break

    # export the svgs
    for i, svg in enumerate(svgs):
        # use the name if the body was named
        if svg.firstChild.hasAttribute('name'):
            svg_name = svg.firstChild.getAttribute('name')
            svg.firstChild.removeAttribute('name')
            name = output_format.format(svg_name, name=svg_name, index=i)
        else:
            name = output_format.format(i, name='', index=i)

        with open(os.path.join(output_dir, name + '.svg'), 'w') as file:
            if prettyxml:
                file.write(svg.toprettyxml())
            else:
                file.write(svg.toxml())

