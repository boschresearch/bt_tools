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

from itertools import combinations
from itertools import product
import os
import unittest

from bt_view.main import main

TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '_test_data')


class TestBtViewMain(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestBtViewMain, self).__init__(*args, **kwargs)
        # number extensions of the different input files
        self.no_exts = ['1', '2', '_other']
        # data extensions of the different output files
        self.log_data_exts = ['count', 'states']
        # image extensions of the different output files
        self.img_exts = ['png', 'svg']

    def setUp(self):
        self._remove_old_images()

    def tearDown(self):
        self._remove_old_images()

    def _remove_old_images(self):
        """Remove old image files in test data directory."""
        for fname in os.listdir(TEST_DATA_DIR):
            for ext in self.img_exts:
                if fname.endswith(ext):
                    os.remove(os.path.join(TEST_DATA_DIR, fname))

    def _check_svg_for_nodenames(self, svg):
        """Check if the svg contains the node names."""
        for node_name in [
            'NavigateWithReplanning',
            'RateController',
            'FollowPath',
            'ComputePathToPose',
            'FollowPathRecoveryFallback',
            'ComputePathToPoseRecoveryFallback',
            'GoalUpdated',
            'ClearLocalCostmap',
            'ClearGlobalCostmap',
        ]:
            # check if node name is in svg file
            self.assertIn(node_name, svg)

    def test_bt_view_main_single_fbl(self):
        """Test bt_view.main.main() with single FBL file."""
        # there should not be any hashes stored yet
        svg_hashes_fbl = {}
        self.assertEqual(len(svg_hashes_fbl), 0)
        for no in self.no_exts:
            bt_log_fbl_fname = os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}.fbl')
            main(['--bt_log_fbl_fname', bt_log_fbl_fname])
            for data, ext in product(
                self.log_data_exts,
                    ['png', 'svg']):
                fname = os.path.join(
                    TEST_DATA_DIR, f'bt_trace{no}_fbl_log_{data}.{ext}')
                self.assertTrue(os.path.isfile(fname))
            for data in self.log_data_exts:
                fname = os.path.join(
                    TEST_DATA_DIR, f'bt_trace{no}_fbl_log_{data}.svg')
                # load svg file
                with open(fname, 'r') as f:
                    svg = f.read()
                svg_hashes_fbl[fname] = hash(svg)
                self._check_svg_for_nodenames(svg)

        # make sure that the svg files are not identical
        for data in self.log_data_exts:
            for a, b in combinations(self.no_exts, 2):
                self.assertNotEqual(
                    os.path.join(
                        TEST_DATA_DIR, f'bt_trace{a}_fbl_log_{data}.svg'),
                    os.path.join(
                        TEST_DATA_DIR, f'bt_trace{b}_fbl_log_{data}.svg'),
                    f'Files {a} and {b} are identical.'
                )

        # todo: can we also check if the svg files are correct with respect to
        #  the values?

    @unittest.skipIf(
        os.path.exists('/.dockerenv') and os.environ.get('ROS_DISTRO') == 'rolling',
        'Skipping test on ROS2 rolling, because there is some regression.')
    def test_bt_view_main_regression_log(self):
        """Test if images are identical to the reference for log data."""
        bt_log_fbl_fnames = [
            os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}.fbl') for no in self.no_exts]
        bt_log_img_fnames_out = [
            os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}_fbl_log_{data}.{ext}') for no, data, ext in
            product(self.no_exts, self.log_data_exts, self.img_exts)]
        bt_log_img_fnames_ref = [
            os.path.join(
                TEST_DATA_DIR,
                'reference',
                f'bt_trace{no}_fbl_log_{data}.{ext}') for no, data, ext in
            product(self.no_exts, self.log_data_exts, self.img_exts)]
        for bt_log_fbl_fname in bt_log_fbl_fnames:
            main(['--bt_log_fbl_fname', bt_log_fbl_fname])
        for bt_log_img_fname_out, bt_log_img_fname_ref in zip(
            bt_log_img_fnames_out,
                bt_log_img_fnames_ref):
            with open(bt_log_img_fname_out, 'rb') as f:
                out = f.read()
            with open(bt_log_img_fname_ref, 'rb') as f:
                ref = f.read()
            self.assertEqual(out, ref)

    @unittest.skipIf(
        os.path.exists('/.dockerenv'),
        'Skipping test in docker container, because I can not get the '
        'seeding to be consistent.')
    def test_bt_view_main_regression_static(self):
        """Test if images are identical to the reference for static data."""
        bt_fbl_fnames = [
            os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}.fbl') for no in self.no_exts]
        bt_img_fnames_out = [
            os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}_demo.{ext}') for no, ext in
            product(self.no_exts, self.img_exts)]
        bt_img_fnames_ref = [
            os.path.join(
                TEST_DATA_DIR,
                'reference',
                f'bt_trace{no}_demo.{ext}') for no, ext in
            product(self.no_exts, self.img_exts)]
        for bt_fbl_fname in bt_fbl_fnames:
            main(['--bt_log_fbl_fname', bt_fbl_fname, '--demo'])
        for bt_img_fname_out, bt_img_fname_ref in zip(
            bt_img_fnames_out,
                bt_img_fnames_ref):
            with open(bt_img_fname_out, 'rb') as f:
                out = f.read()
            with open(bt_img_fname_ref, 'rb') as f:
                ref = f.read()
            self.assertEqual(out, ref, f'Files {bt_img_fname_out} and '
                             f'{bt_img_fname_ref} must be identical.')

    def test_bt_view_main_multiple_fbl_files_error(self):
        """Raise error if FBL files from different BTs are given."""
        bt_log_fbl_fname1 = os.path.join(
            TEST_DATA_DIR,
            'bt_trace1.fbl')
        bt_log_fbl_fname_other = os.path.join(
            TEST_DATA_DIR,
            'bt_trace_other.fbl')

        with self.assertRaises(SystemExit) as cm:
            main(['--bt_log_fbl_fname',
                  bt_log_fbl_fname1,
                  bt_log_fbl_fname_other])
        self.assertEqual(cm.exception.code, 1)

    def test_bt_view_main_multiple_fbl_files_merge(self):
        """If multiple FBL files the output should be merged."""
        bt_log_fbl_fname1 = os.path.join(
            TEST_DATA_DIR,
            'bt_trace1.fbl')
        bt_log_fbl_fname2 = os.path.join(
            TEST_DATA_DIR,
            'bt_trace2.fbl')
        svg_hashes_fbl = {}

        main(['--bt_log_fbl_fname',
              bt_log_fbl_fname1,
              bt_log_fbl_fname2])
        fnames_combined_svg = [
            os.path.join(
                TEST_DATA_DIR, f'bt_trace1bt_trace2_fbl_log_{data}.svg')
            for data in self.log_data_exts]

        # the separate image files must not exist yet
        for n, data, img in product(
            self.no_exts,
            self.log_data_exts,
            self.img_exts
        ):
            fname = os.path.join(
                TEST_DATA_DIR, f'bt_trace{n}_fbl_log_{data}.{img}')
            self.assertFalse(os.path.isfile(fname))

        # the combined image files must exist
        for fname in fnames_combined_svg:
            self.assertTrue(os.path.isfile(fname), fname)

        # make the non-merged image files for comparison
        self.assertEqual(len(svg_hashes_fbl), 0)
        for no in self.no_exts:
            bt_log_fbl_fname = os.path.join(
                TEST_DATA_DIR,
                f'bt_trace{no}.fbl')
            main(['--bt_log_fbl_fname', bt_log_fbl_fname])
            for data, img in product(
                self.log_data_exts,
                self.img_exts
            ):
                fname = os.path.join(
                    TEST_DATA_DIR, f'bt_trace{no}_fbl_log_{data}.{img}')
                self.assertTrue(os.path.isfile(fname))
            for data in self.log_data_exts:
                fname = os.path.join(
                    TEST_DATA_DIR, f'bt_trace{no}_fbl_log_{data}.svg')
                # load svg file
                with open(fname, 'r') as f:
                    svg = f.read()
                svg_hashes_fbl[fname] = hash(svg)
                self._check_svg_for_nodenames(svg)

        # also hash the combined svg files
        for fname in fnames_combined_svg:
            with open(fname, 'r') as f:
                svg = f.read()
            svg_hashes_fbl[fname] = hash(svg)
            self._check_svg_for_nodenames(svg)

        # make sure that none of the svg files are identical
        for fname_a, fname_b in combinations(svg_hashes_fbl.keys(), 2):
            self.assertNotEqual(svg_hashes_fbl[fname_a],
                                svg_hashes_fbl[fname_b])

    def test_bt_view_main_coverage(self):
        """Test the calculation of the coverage."""
        # this file has 12 nodes and 6 are covered
        fname_1 = os.path.join(
            TEST_DATA_DIR,
            'bt_trace1.fbl')
        # this file has 12 nodes and 9 are covered
        fname_2 = os.path.join(
            TEST_DATA_DIR,
            'bt_trace2.fbl')

        main(['--bt_log_fbl_fname', fname_1,
              '--coverage-threshold', '0.5'])

        with self.assertRaises(SystemExit) as cm:
            main(['--bt_log_fbl_fname', fname_1,
                  '--coverage-threshold', '0.6'])
        self.assertEqual(cm.exception.code, 1)

        main(['--bt_log_fbl_fname', fname_2,
              '--coverage-threshold', '0.7'])

        with self.assertRaises(SystemExit) as cm:
            main(['--bt_log_fbl_fname', fname_2,
                  '--coverage-threshold', '0.8'])
        self.assertEqual(cm.exception.code, 1)
