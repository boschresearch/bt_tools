"""Functions to read logs and convert them to values per bt node."""
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
from typing import Optional, Tuple, Union

from btlib import VALUE_MAP, VALUE_MAP_RETURN_STATES
from btlib.common import NODE_STATE
from btlib.fbl_reader import read_log
import networkx as nx


logger = logging.getLogger(__name__)


def _get_id_and_state_from_line(line: str) -> Tuple[int, NODE_STATE]:
    """Get id and return state from line."""
    try:
        line_after_timestamp = line.split(']')[1]
        line_wo_brackets = line_after_timestamp\
            .replace('(', '')\
            .replace(')', '')\
            .replace(']', '')\
            .replace('[', '')
        id_ = int(line_wo_brackets.split(':')[0])
        state_str = line_wo_brackets.split('->')[-1].strip()
        for rs in NODE_STATE:
            if rs.name in state_str:
                return id_, rs
        raise ValueError(f'Could not find return state in {state_str}')
    except (ValueError, IndexError) as e:
        raise ValueError(f'Could not parse line {line}') from e


def read_log_fbl(fname: str,
                 g: nx.Graph) -> Tuple[VALUE_MAP, VALUE_MAP_RETURN_STATES]:
    """
    Read log file and return values per node.

    :param fname: Log file name.
    :param g: Graph representing the behavior tree.

    :return: Tuple of
        `values_count`: How often a node was executed.
        `values_success`: How often a node was successful (positive value)
        vs failed (negative value).
    """
    with open(fname, 'rb') as file_b:
        buf = bytearray(file_b.read())
        log = read_log(buf)
    values_count: VALUE_MAP = {id_: None for id_ in g.nodes()}
    values_state_counts: VALUE_MAP_RETURN_STATES = {
        id_: None for id_ in g.nodes()
    }
    for id_, rs in log:
        assert id_ is not None, 'Id must not be None'
        if values_count[id_] is None:
            values_count[id_] = 0
        values_count[id_] += 1  # type: ignore
        if values_state_counts[id_] is None:
            values_state_counts[id_] = [0 for _ in NODE_STATE]
        values_state_counts[id_][rs.value - 1] += 1  # type: ignore
    return values_count, values_state_counts


def merge_values(
    values1: Optional[Union[VALUE_MAP, VALUE_MAP_RETURN_STATES]],
    values2: Optional[Union[VALUE_MAP, VALUE_MAP_RETURN_STATES]]) -> \
        Union[VALUE_MAP, VALUE_MAP_RETURN_STATES]:
    """
    Merge values of two value maps.

    On the lowest level this will add the two values if they are present.
    """
    if values1 is None:
        assert values2 is not None, 'At least one values must not be None'
        return values2
    if values2 is None:
        assert values1 is not None, 'At least one values must not be None'
        return values1
    assert len(values1) == len(values2), 'Values must have same length'
    values_out: Union[VALUE_MAP, VALUE_MAP_RETURN_STATES] = {}  # type: ignore
    for id_ in values1:
        if values1[id_] is None:
            values_out[id_] = values2[id_]  # type: ignore
        elif values2[id_] is None:
            values_out[id_] = values1[id_]  # type: ignore
        elif isinstance(values1[id_], list):
            assert isinstance(values2[id_], list), \
                'Values must be of same type'
            values_out[id_] = [
                sum(x) for x in zip(
                    values1[id_], values2[id_])]  # type: ignore
        elif isinstance(values1[id_], int):
            assert isinstance(values2[id_], int), \
                'Values must be of same type'
            values_out[id_] = values1[id_] + values2[id_]  # type: ignore
        else:
            raise ValueError(f'Unknown type {type(values1[id_])}')
    return values_out
