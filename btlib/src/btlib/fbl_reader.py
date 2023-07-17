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

from btlib.common import NODE_CAT, NODE_STATE
from btlib.Serialization.BehaviorTree import BehaviorTree
from btlib.Serialization.NodeStatus import NodeStatus
import networkx as nx


def state_from_status(s: NodeStatus) -> NODE_STATE:
    if s == NodeStatus.IDLE:
        return NODE_STATE.IDLE
    if s == NodeStatus.RUNNING:
        return NODE_STATE.RUNNING
    if s == NodeStatus.SUCCESS:
        return NODE_STATE.SUCCESS
    if s == NodeStatus.FAILURE:
        return NODE_STATE.FAILURE
    raise ValueError('Unknown state')


def read_bt(buffer) -> nx.Graph:
    g = nx.DiGraph()
    bt = BehaviorTree.GetRootAsBehaviorTree(buffer, 4)
    root = bt.RootUid()
    n_nodes = bt.NodesLength()
    print(f'{n_nodes=}')
    nodes = [
        bt.Nodes(i) for i in range(n_nodes)
    ]
    for node in nodes:
        g.add_node(
            node.Uid(),
            NAME=node.InstanceName().decode())
    g.nodes()[root]['category'] = NODE_CAT.ROOT
    for node in nodes:
        for n, child in enumerate(
            [node.ChildrenUid(i)
             for i in range(node.ChildrenUidLength())]):
            g.add_edge(node.Uid(), child, label=n)
    return g


def read_log(buffer):
    ENDIAN = 'little'
    header_size = int.from_bytes(buffer[:2], byteorder=ENDIAN)
    index = header_size + 4
    # all offsets are defined in https://github.com/BehaviorTree/BehaviorTree.\
    # CPP/blob/9f0a969eb929a86e754498d1a1cde8037b2b6f13/tools/bt_log_cat.cpp#L99
    log = []
    while index < len(buffer):
        uid = int.from_bytes(buffer[index + 8:index + 10], ENDIAN)
        # TODO: Can we also interpret the `state_1`?
        # status_1 = int.from_bytes(buffer[index + 10:index + 11], ENDIAN)
        status_2 = int.from_bytes(buffer[index + 11:index + 12], ENDIAN)
        # TODO: Implementation of timing analysis
        log.append((
            uid,
            state_from_status(status_2)
        ))
        index += 12
    return log
