"""Tests for the btlib.analysis module."""
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

from btlib.analysis import get_coverage


class TestAnalysis(unittest.TestCase):

    def test_get_coverage_empty(self):
        """Test that with no data, get_coverage works as expected."""
        data_empty = {}
        self.assertEqual(get_coverage(data_empty), 0.0)

    def test_get_coverage_0(self):
        """Test that with a coverage of 0, get_coverage works as expected."""
        data0 = {
            1: None,
            3: [None, None, None]
        }
        self.assertEqual(get_coverage(data0), 0.0)

    def test_get_coverage_50(self):
        """Test that with a coverage of 50%, get_coverage works as expected."""
        data50 = {
            0: 1,
            1: None,
        }
        self.assertEqual(get_coverage(data50), 0.5)

    def test_get_coverage_100(self):
        """Test that with a coverage of 100%, get_coverage works as expected."""
        data100 = {
            0: 1,
            1: [1, 2],
            2: 1,
            42: 1,
        }
        self.assertEqual(get_coverage(data100), 1.0)

    def test_get_coverage_value_error(self):
        """Test that get_coverage raises ValueError with invalid data."""
        data_invalid = {
            0: 1,
            1: [1, 2],
            2: 1,
            42: 'foo',
        }
        with self.assertRaises(ValueError):
            get_coverage(data_invalid)
