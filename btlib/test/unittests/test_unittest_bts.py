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

import os
import unittest
from unittest.mock import patch

from bs4 import BeautifulSoup

from btlib.bts import (assemble_subtrees, xml_to_networkx)


def _mock_read_xml_file():
    return BeautifulSoup(
        '<?xml version="1.0"?>'
        '<root main_tree_to_execute="MainTree">'
        '<BehaviorTree ID="MainTree">'
        '<Control ID="Sequence" name="NavigateWithReplanning">'
        '<Action ID="ComputePath" name="ComputePath"/>'
        '<Action ID="FollowPath" name="FollowPath"/>'
        '</Control>'
        '</BehaviorTree>'
        '</root>',
        'xml'
    )


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '_test_data')


class UnittestBTs(unittest.TestCase):
    """Tests for the btlib.bts module."""

    def test_xml_to_networkx(self):
        path = '/tmp/test.xml'

        with patch(
            'btlib.bts.BeautifulSoup',  # how it is imported
            return_value=_mock_read_xml_file()
        ) as mock_bs, patch(
            'btlib.bts.open',  # how it is imported
            return_value=None
        ) as _, patch(
            'btlib.bts.os.path.isfile',  # how it is imported
            return_value=True
        ) as mock_isfile:
            g, xpi = xml_to_networkx(path)
            mock_bs.assert_called_once_with(None, 'xml')
            mock_isfile.assert_called_once_with(path)

        # all nodes are in the graph and the xpi
        self.assertEqual(g.number_of_nodes(), 4)
        self.assertEqual(len(xpi), 4)
        for x in [10, 100, 1000, 1001]:
            self.assertIn(x, g.nodes)
            self.assertIn(x, xpi.keys())

        # all edges point down
        for a, b in g.edges:
            self.assertLess(a, b)

    # def test_fbl_to_networkx(self):
    #     path = '/tmp/test.fbl'

    #     with patch(
    #             'btlib.bts.read_fbl_file',  # how it is imported
    #             return_value=_mock_read_fbl_file()) as mock:
    #         g = fbl_to_networkx(path)
    #         mock.assert_called_once_with(path)

    #     self.assertEqual(g.number_of_nodes(), 5)

    def test_assemble_subtrees(self):
        """Testing assemble_subtrees."""
        self.assertRaises(NotImplementedError, assemble_subtrees, None, None)
