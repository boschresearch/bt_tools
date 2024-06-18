# Copyright (c) 2023 - see the NOTICE file for details

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from math import floor, log10
import os
from typing import Tuple

from bs4 import BeautifulSoup
from bs4.element import Tag
from btlib import VALUE_MAP, XML_PER_ID
from btlib.common import NODE_CAT
from btlib.fbl_reader import read_bt
import networkx as nx


logger = logging.getLogger(__name__)

NAME = 'NAME'


def _get_siblings(elm):
    return [ch for ch in elm.parent.children if isinstance(ch, Tag)]


def _get_unique_id(elm: BeautifulSoup, tree_id: int) -> int:
    if elm.name == 'BehaviorTree':
        # we need a one in at first position, because 00 evaluates to 0
        return tree_id + 10
    parents_ch_list = _get_siblings(elm)
    n_chars_of_nr = floor(log10(len(parents_ch_list)) + 1)
    return int(
        str(_get_unique_id(elm.parent, tree_id)) + str(
            parents_ch_list.index(elm)).zfill(n_chars_of_nr))


def _get_attrs(elm: BeautifulSoup) -> dict:
    attrs = {NAME: elm.name}
    for attr in elm.attrs:
        attrs[attr] = elm.attrs[attr]
    return attrs


def _get_node_category(node: BeautifulSoup) -> NODE_CAT:
    if node.name in ['BehaviorTree']:
        return NODE_CAT.ROOT
    if node.name in ['SubTree']:
        return NODE_CAT.SUBTREE
    elif len(node.find_all()) == 0:
        # leaf node
        return NODE_CAT.LEAF
    elif len(node.find_all()) == 1:
        # decorator
        return NODE_CAT.DECORATOR
    elif len(node.find_all()) > 1:
        # control node
        return NODE_CAT.CONTROL
    else:
        raise ValueError(f'Unknown node type: {node.name}')


def _add_node(g: nx.Graph, xml_per_id: XML_PER_ID, node: BeautifulSoup,
              tree_id: int) -> Tuple[nx.Graph, XML_PER_ID]:
    g.add_node(_get_unique_id(node, tree_id), **_get_attrs(node),
               category=_get_node_category(node))
    xml_per_id[_get_unique_id(node, tree_id)] = node
    return g, xml_per_id


def xml_to_networkx(fname: str) -> nx.Graph:
    """Read a BehaviorTree XML file into a networkx graph."""
    assert fname.endswith('.xml'), f'Must be an xml file, got {fname}'
    assert os.path.isfile(fname), f'File {fname} must exist'
    bs = BeautifulSoup(open(fname), 'xml')
    g = nx.DiGraph()
    xpi: XML_PER_ID = {}
    # print(f'{bs=}')

    bt_roots = bs.find_all('BehaviorTree')
    # print(f'{bt_roots=}')
    if len(bt_roots) > 1:
        logger.warning('More than one BehaviorTree found. ')
    for bt_root in bt_roots:
        tree_id = bt_roots.index(bt_root)
        g, xpi = _add_node(g, xpi, bt_root, tree_id)
        g.nodes[_get_unique_id(bt_root, tree_id)]['root'] = True
        for child in bt_root.recursiveChildGenerator():
            parents_ch_list = _get_siblings(child)
            if not isinstance(child, Tag):
                continue
            g, xpi = _add_node(g, xpi, child, tree_id)
            g.add_edge(_get_unique_id(child.parent, tree_id),
                       _get_unique_id(child, tree_id),
                       label=parents_ch_list.index(child))
    return g, xpi


def fbl_to_networkx(fname: str) -> nx.Graph:
    """Read a fbl file into a networkx graph."""
    with open(fname, 'rb') as file_b:
        buf = bytearray(file_b.read())
        g = read_bt(buf)
    assert g, 'Graph must exist'
    return g


def assemble_subtrees(g: nx.Graph, xpi: XML_PER_ID) -> nx.Graph:
    """Assemble subtrees into the one graph."""
    raise NotImplementedError


def make_demo_value(g: nx.Graph) -> VALUE_MAP:
    """Generate a value map for the demo graph."""
    colors: VALUE_MAP = {}
    for node in g.nodes:
        n = int(node)
        # last digit of node id
        c = int(str(n)[-1])
        colors[n] = c / 9.
    return colors
