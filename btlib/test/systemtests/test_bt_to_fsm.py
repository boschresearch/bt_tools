"""Tests for the btlib.analysis module."""
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

import os
import unittest

from btlib.bt_to_fsm.bt_to_fsm import Bt2FSM
from btlib.bts import xml_to_networkx


class TestBt2FSM(unittest.TestCase):

    def test_inverter(self):
        """Test that the conversion from a Behavior Tree to a FSM works."""
        bt, _ = xml_to_networkx(os.path.join(
            os.path.dirname(__file__), '..', '_test_data',
            'bt2fsm', 'inverter_bt.xml'))
        bt2fsm = Bt2FSM(bt)
        fsm = bt2fsm.convert()
        # should have 1 node for the condition
        # and 4 nodes from the ports
        self.assertEqual(fsm.number_of_nodes(), 1 + 4)
        # should have 1 edge for the tick port
        # and 3 per leaf node
        self.assertEqual(fsm.number_of_edges(), 1 + 3 * 1)

        # check the existence of the edges
        for port in ['success', 'failure', 'running']:
            self.assertTrue(fsm.has_edge('1000_ServiceBtCondition', port))
        self.assertTrue(fsm.has_edge('tick', '1000_ServiceBtCondition'))

        # check the labels of the edges
        self.assertEqual(fsm.edges['1000_ServiceBtCondition', 'success']['label'], 'on_failure')
        self.assertEqual(fsm.edges['1000_ServiceBtCondition', 'failure']['label'], 'on_success')
        self.assertEqual(fsm.edges['1000_ServiceBtCondition', 'running']['label'], 'on_running')
        self.assertEqual(fsm.edges['tick', '1000_ServiceBtCondition']['label'], 'on_tick')

    def test_simple(self):
        """Test that the conversion from a Behavior Tree to a FSM works."""
        bt, _ = xml_to_networkx(os.path.join(
            os.path.dirname(__file__), '..', '_test_data',
            'bt2fsm', 'simple_bt.xml'))
        bt2fsm = Bt2FSM(bt)
        fsm = bt2fsm.convert()
        # should have 3 nodes from the leaf nodes
        # and 4 nodes from the ports
        self.assertEqual(fsm.number_of_nodes(), 3 + 4)
        # should have 1 edge for the tick port
        # and 3 per leaf node
        self.assertEqual(fsm.number_of_edges(), 1 + 3 * 3)


if __name__ == '__main__':
    unittest.main()
