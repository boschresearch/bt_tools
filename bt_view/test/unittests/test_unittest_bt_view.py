"""Tests for the bt_view.bt_view module."""
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

from bt_view.bt_view import _log_normalize


class TestBtView(unittest.TestCase):

    def test_log_normalize(self):
        """Make sure that _log_normalize works as expected."""
        # mapping from [-1, 1] to [0, 1]
        values_between_minus_1_and_1 = {
            0: -1.0,
            1: 0.0,
            2: 1.0,
        }
        values_between_minus_1_and_1_normalized = _log_normalize(
            values_between_minus_1_and_1)
        self.assertEqual(values_between_minus_1_and_1_normalized, {
            0: 0.0,
            1: 0.5,
            2: 1.0,
        })

        # mapping from [0, 1] to [0, 1] (which should be [0.5, 1.0])
        values_between_0_and_1 = {
            0: 0.0,
            2: 1.0,
        }
        values_between_0_and_1_normalized = _log_normalize(
            values_between_0_and_1)
        self.assertEqual(values_between_0_and_1_normalized, {
            0: 0.5,
            2: 1.0,
        })

        # mapping from [-1, 1] to [-50, 100]
        values_between_minus_1_and_1_normalized = _log_normalize(
            values_between_minus_1_and_1, vmin=-50, vmax=100)
        self.assertEqual(values_between_minus_1_and_1_normalized, {
            0: -50.0,
            1: 25.0,
            2: 100.0,
        })

        # for the log range, all we care about is that big values are
        # not to far apart from small values
        a = 1
        b = 10
        c = 100
        input_values = {
            0: a,
            1: b,
            2: c,
        }
        output_values = _log_normalize(input_values)
        self.assertLess(output_values[2] - output_values[1], c - b)
        self.assertLess(output_values[1] - output_values[0], b - a)

        # test that None values are not changed
        input_values = {
            0: 0,
            1: None,
            2: 1,
        }
        output_values = _log_normalize(input_values)
        self.assertEqual(output_values, {
            0: 0.5,
            1: None,
            2: 1.0,
        })

        # test that it also works for with lists
        input_values = {
            0: [0, 0],
            1: [1, -1],
            2: [-1, 1],
        }
        output_values = _log_normalize(input_values)
        self.assertEqual(output_values, {
            0: [0.5, 0.5],
            1: [1.0, 0.0],
            2: [0.0, 1.0],
        })

        # test that a ValueError is raised if the input is of the wrong type
        with self.assertRaises(ValueError):
            _log_normalize({0: 'a'})
