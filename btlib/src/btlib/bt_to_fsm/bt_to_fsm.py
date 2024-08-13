# Copyright (c) 2024 - see the NOTICE file for details

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
import random
from typing import Tuple

from btlib.bts import NODE_CAT
import networkx as nx

CONTROL_TYPE = Enum('CONTROL_TYPE', 'SEQUENCE FALLBACK')
DECORATOR_TYPE = Enum('DECORATOR_TYPE', 'INVERTER')


class Bt2FSM:
    """Converts a Behavior Tree to a Finite State Machine."""

    def __init__(self, bt: nx.Graph):
        self.bt: nx.Graph = bt

    def convert(self) -> nx.DiGraph:
        """Convert the Behavior Tree to a Finite State Machine."""
        roots = [node for node in self.bt.nodes
                 if self.bt.nodes[node]['category'] == NODE_CAT.ROOT]
        assert len(roots) == 1, 'There must be exactly one root node.'
        root = roots[0]
        first_control = list(self.bt.successors(root))[0]
        fsm = self._convert_subtree(root)
        # relabel external ports
        fsm = nx.relabel_nodes(
            fsm,
            {
                'tick_' + str(first_control): 'tick',
                'success_' + str(first_control): 'success',
                'failure_' + str(first_control): 'failure',
                'running_' + str(first_control): 'running'
            })
        # remove intermediate ports
        for node in list(fsm.nodes):
            if node.startswith('tick_') or node.startswith('success_') or \
                    node.startswith('failure_') or node.startswith('running_'):
                out_edges = list(fsm.out_edges(node))
                in_edges = list(fsm.in_edges(node))
                if len(out_edges) == 0 or len(in_edges) == 0:
                    continue
                assert len(
                    out_edges) == 1, 'Port must have exactly one out edge.'
                for edge in in_edges:
                    fsm.add_edge(edge[0], out_edges[0][1],
                                 label=fsm.edges[edge]['label'])
                fsm.remove_node(node)
        return fsm

    def _add_ports(self, fsm: nx.DiGraph, node_id: int) -> Tuple[str, ...]:
        """
        Add ports to the Finite State Machine.

        These can then be used used to connect to
        the outside world during the conversion.
        """
        names = [port + '_' + str(node_id) for port in [
            'tick', 'success', 'failure', 'running']]
        for port in names:
            fsm.add_node(port)
        return tuple(names)

    def _wire_children_together(
            self, fsm: nx.DiGraph, children: list,
            port_names: Tuple[str, ...],
            control_type: CONTROL_TYPE):
        """
        Wire the children of a control node to its ports.

        This implements the logic of the control node.
        """
        children_names = [str(child.graph['NODE_ID']) for child in children]
        p_tick, p_succ, p_fail, p_runn = port_names
        # merge children into the FSM
        for child in children:
            for node in child.nodes():
                fsm.add_node(node)
            for edge in child.edges():
                fsm.add_edge(edge[0], edge[1],
                             label=child.edges[edge]['label'])
        # wire the children together
        for i in range(len(children) - 1):
            if control_type == CONTROL_TYPE.SEQUENCE:
                # on success, tick the next child
                fsm.add_edge(
                    'success_' + children_names[i],
                    'tick_' + children_names[i + 1],
                    label='on_success')
                # on failure, go to the failure port
                fsm.add_edge(
                    'failure_' + children_names[i],
                    p_fail, label='on_failure')
            elif control_type == CONTROL_TYPE.FALLBACK:
                # on success, go to the success port
                fsm.add_edge(
                    'success_' + children_names[i],
                    p_succ, label='on_success')
                # on failure, tick the next child
                fsm.add_edge(
                    'failure_' + children_names[i],
                    'tick_' + children_names[i + 1],
                    label='on_failure')
            else:
                raise NotImplementedError(
                    f'Control type {control_type} not implemented.')
            # on running, go to the running port
            fsm.add_edge(
                'running_' + children_names[i], p_runn, label='on_running')
        # tick the first child first
        fsm.add_edge(p_tick, 'tick_' + children_names[0], label='on_tick')
        # wire last child
        fsm.add_edge(
            'success_' + children_names[-1], p_succ, label='on_success')
        fsm.add_edge(
            'failure_' + children_names[-1], p_fail, label='on_failure')
        fsm.add_edge(
            'running_' + children_names[-1], p_runn, label='on_running')

    def _wire_child(
            self, fsm: nx.DiGraph, child: nx.DiGraph,
            port_names: Tuple[str, ...],
            decorator_type: DECORATOR_TYPE):
        """
        Wire the child of a decorator node to its ports.

        This implements the logic of the decorator node.
        """
        child_name = str(child.graph['NODE_ID'])
        p_tick, p_succ, p_fail, p_runn = port_names
        for node in child.nodes():
            fsm.add_node(node)
        for edge in child.edges():
            fsm.add_edge(edge[0], edge[1], label=child.edges[edge]['label'])
        # tick the child
        fsm.add_edge(p_tick, 'tick_' + child_name, label='on_tick')
        if decorator_type == DECORATOR_TYPE.INVERTER:
            # on success, go to failure port
            fsm.add_edge('success_' + child_name, p_fail, label='on_success')
            # on failure, go to success port
            fsm.add_edge('failure_' + child_name, p_succ, label='on_failure')
        else:
            raise NotImplementedError(
                f'Decorator {decorator_type} not implemented.')
        # on running, go to running port
        fsm.add_edge('running_' + child_name, p_runn, label='on_running')

    def _convert_subtree(self, node_id: int) -> nx.DiGraph:
        """Convert any subtree to a FSM by recursively calling this."""
        node = self.bt.nodes[node_id]
        if node['category'] == NODE_CAT.ROOT:
            assert len(list(self.bt.successors(node_id))) == 1, \
                'Root node must have exactly one child.'
            return self._convert_subtree(list(self.bt.successors(node_id))[0])
        fsm = nx.DiGraph()
        fsm.graph['NODE_ID'] = node_id
        port_names = self._add_ports(fsm, node_id)
        p_tick, p_succ, p_fail, p_runn = port_names
        if node['category'] == NODE_CAT.LEAF:
            if node.get('ID') is not None:
                assert node.get('NAME') in [
                    'Action', 'Condition'], \
                        'Only Action and Condition nodes can have an ID.'
                unique_name = f'{node_id}_{node["ID"]}'
            elif node.get('NAME') is not None:
                unique_name = f'{node_id}_{node["NAME"]}'
            else:
                raise ValueError('Leaf node must have an ID or a NAME.')
            fsm.add_node(unique_name, **node)
            fsm.add_edge(p_tick, unique_name, label='on_tick')
            fsm.add_edge(unique_name,
                         p_succ, label='on_success')
            fsm.add_edge(unique_name,
                         p_fail, label='on_failure')
            fsm.add_edge(unique_name,
                         p_runn, label='on_running')
        elif node['category'] == NODE_CAT.CONTROL:
            children = []
            for child in self.bt.successors(node_id):
                fsm_subtree = self._convert_subtree(child)
                children.append(fsm_subtree)
            if node['NAME'] == 'Sequence':
                ct = CONTROL_TYPE.SEQUENCE
            elif node['NAME'] == 'Fallback':
                ct = CONTROL_TYPE.FALLBACK
            else:
                raise NotImplementedError(
                    f'Control type {node["NAME"]} not implemented.')
            self._wire_children_together(
                fsm, children, port_names, ct)
        elif node['category'] == NODE_CAT.DECORATOR:
            assert len(list(self.bt.successors(node_id))) == 1, \
                'Decorator must have exactly one child.'
            child = list(self.bt.successors(node_id))[0]
            fsm_subtree = self._convert_subtree(child)
            if node['NAME'] == 'Inverter':
                dt = DECORATOR_TYPE.INVERTER
            else:
                raise NotImplementedError(
                    f'Decorator {node["NAME"]} not implemented.')
            self._wire_child(fsm, fsm_subtree, port_names, dt)
        else:
            raise NotImplementedError(
                f'Category {node["category"]} not implemented.')
        return fsm

    def plot_fsm(self, fsm: nx.DiGraph):
        """Plot the Finite State Machine."""
        import matplotlib.pyplot as plt
        fixed_pos = {
            'tick': (-2., 0.),
            'success': (2., 1.),
            'failure': (2., 0.),
            'running': (2., -1.)
        }
        initial_pos = {}
        initial_pos.update(fixed_pos)
        for node in fsm.nodes():
            if node not in fixed_pos:
                initial_pos[node] = (0, random.uniform(-1, 1))
        pos = nx.kamada_kawai_layout(
            fsm, pos=initial_pos)
        nx.draw(fsm, pos, with_labels=True)
        edge_labels = nx.get_edge_attributes(fsm, 'label')
        nx.draw_networkx_edge_labels(fsm, pos, edge_labels=edge_labels)
        plt.savefig('fsm.png')
