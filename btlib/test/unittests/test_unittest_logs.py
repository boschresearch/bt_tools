"""Tests for the btlib.logs module."""
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

import unittest

from btlib.logs import (_get_id_and_state_from_line)

import networkx as nx


def _make_demo_graph():
    g = nx.DiGraph()
    g.add_node(1, name='SequenceStar')
    g.add_node(2, name='HaveFun')
    g.add_edge(1, 2)
    g.add_node(3, name='Fallback')
    g.add_edge(1, 3)
    g.add_node(4, name='SetBlackboard', ID='SetBlackboard01')
    g.add_edge(3, 4)
    g.add_node(5, name='SetBlackboard', ID='SetBlackboard02')
    g.add_edge(3, 5)
    return g


class UnittestLogs(unittest.TestCase):
    """Tests for the btlib.logs module."""

    def test_get_id_and_state_from_line_error(self):
        """Testing error cases."""
        # test with empty line
        self.assertRaises(
            ValueError,
            _get_id_and_state_from_line, '')

        # test with line without id
        self.assertRaises(
            ValueError,
            _get_id_and_state_from_line, '[] (): SequenceStar')

        # test with line with wrong return state
        line = '[1674644299.406561] (  1): SequenceStar              '\
            '\x1b[36mIDLE   \x1b[0m -> \x1b[33mRUNNINK\x1b[0m'
        self.assertRaises(
            ValueError,
            _get_id_and_state_from_line, line)

    def test_get_id_and_state_from_line_normal(self):
        """Test with normal lines."""
        # test with normal id and return state
        line = '[1674644299.406561] (  1): SequenceStar              '\
            '\x1b[36mIDLE   \x1b[0m -> \x1b[33mRUNNING\x1b[0m'
        id_, rs = _get_id_and_state_from_line(line)
        self.assertEqual(id_, 1)
        self.assertEqual(rs, rs.RUNNING)

        # test with different id and return state
        line2 = '[1674644299.407965] (  9):          Inverter         '\
            '\x1b[33mRUNNING\x1b[0m -> \x1b[32mSUCCESS\x1b[0m'
        id2, rs2 = _get_id_and_state_from_line(line2)
        self.assertEqual(id2, 9)
        self.assertEqual(rs2, rs2.SUCCESS)

        # test with very high id and failure
        line3 = '[1674644299.408000] (999):   AnotherNode         '\
            '\x1b[32mSUCCESS\x1b[0m -> \x1b[31mFAILURE\x1b[0m'
        id3, rs3 = _get_id_and_state_from_line(line3)
        self.assertEqual(id3, 999)
        self.assertEqual(rs3, rs3.FAILURE)

    # def test_read_log_fbl(self):
    #     path = '/tmp/test.fbl'
    #     g = _make_demo_graph()

    #     with patch(
    #             'btlib.logs.read_fbl_file',  # how it is imported
    #             return_value=_mock_read_fbl_file()) as mock:
    #         v_cnt, v_states = read_log_fbl(path, g)
    #         mock.assert_called_once_with(path)

    #     for values in [v_cnt, v_states]:
    #         self.assertEqual(len(values), g.number_of_nodes())
    #         for node in g.nodes:
    #             self.assertIn(node, values)

    #     self.assertEqual(v_cnt[1], 2)
    #     self.assertEqual(v_cnt[2], 1)
    #     self.assertEqual(v_cnt[3], 1)
    #     self.assertEqual(v_cnt[4], None)
    #     self.assertEqual(v_cnt[5], None)

    #     self.assertEqual(v_states[1][state.SUCCESS.value - 1], 0)
    #     self.assertEqual(v_states[1][state.FAILURE.value - 1], 1)
    #     self.assertEqual(v_states[1][state.RUNNING.value - 1], 1)
    #     self.assertEqual(v_states[1][state.IDLE.value - 1], 0)

    #     self.assertEqual(v_states[2][state.SUCCESS.value - 1], 0)
    #     self.assertEqual(v_states[2][state.FAILURE.value - 1], 0)
    #     self.assertEqual(v_states[2][state.RUNNING.value - 1], 1)
    #     self.assertEqual(v_states[2][state.IDLE.value - 1], 0)

    #     self.assertEqual(v_states[3][state.SUCCESS.value - 1], 0)
    #     self.assertEqual(v_states[3][state.FAILURE.value - 1], 1)
    #     self.assertEqual(v_states[3][state.RUNNING.value - 1], 0)
    #     self.assertEqual(v_states[3][state.IDLE.value - 1], 0)

    #     self.assertEqual(v_states[4], None)
    #     self.assertEqual(v_states[5], None)
