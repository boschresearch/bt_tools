#!/usr/bin/env python3
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

import argparse
import datetime
import os
import random
import sys

try:
    from bt_view import draw_pygraphviz_w_history  # type: ignore
    from bt_view import draw_pygraphviz_w_returnstates  # type: ignore
    from bt_view import draw_pygraphviz_w_valuemod  # type: ignore
except ImportError:
    from .bt_view import draw_pygraphviz_w_history
    from .bt_view import draw_pygraphviz_w_returnstates
    from .bt_view import draw_pygraphviz_w_valuemod
from btlib.analysis import get_coverage
from btlib.bts import fbl_to_networkx
from btlib.bts import xml_to_networkx
from btlib.common import NODE_STATE
from btlib.logs import merge_values
from btlib.logs import read_log_fbl


def main(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--demo',
        help='Use demo values to color nodes',
        action='store_true')
    parser.add_argument(
        '--assemble-subtrees',
        help='If set, subtrees are attached to the main tree',
        action='store_true')
    parser.add_argument(
        '--bt_xml_fname',
        help='Path to behavior tree XML file',
        nargs='?')
    parser.add_argument(
        '--bt_log_json_fname',
        help='Path to behavior tree log JSON file',
        nargs='?')
    parser.add_argument(
        '--bt_log_fbl_fnames',
        help='Path to behavior tree log FBL files. Multiple logs of the same '
        'tree can be provided. The logs will be merged as if they '
        'happened in one run.',
        nargs='*')
    parser.add_argument(
        '--coverage-threshold',
        help='If set, the script will return with exit code 1 if the '
        'coverage is below the threshold. Example: 0.9',
        default=0.0,
        type=float)

    arguments = parser.parse_args(args)
    if not any([
            arguments.bt_xml_fname,
            arguments.bt_log_json_fname,
            arguments.bt_log_fbl_fnames,
            arguments.demo]):
        print('You must provide at least one file to read')
        parser.print_help()
        sys.exit(1)

    if arguments.bt_xml_fname and arguments.bt_log_fbl_fname:
        print('When reading FBL log file, XML file is not needed '
              'and will be ignored')
        arguments.bt_xml_fname = None

    g = None

    # read xml bt definition file
    if arguments.bt_xml_fname:
        bt_xml_fname = arguments.bt_xml_fname
        assert bt_xml_fname.endswith(
            '.xml'), f'Must be a xml file: {bt_xml_fname}'
        assert os.path.isfile(bt_xml_fname), f'File must exist: {bt_xml_fname}'
        # read xml file
        g, _ = xml_to_networkx(bt_xml_fname)
        # if arguments.assemble_subtrees:
        #     g, xpi = assemble_subtrees(g, xpi)

    # read fbl log file
    if arguments.bt_log_fbl_fnames:
        previous_g = None
        value_count = None
        value_states = None
        name_wo_ext = ''.join([
            os.path.splitext(os.path.basename(f))[0]
            for f in arguments.bt_log_fbl_fnames])
        path_wo_ext = os.path.join(
            os.path.dirname(arguments.bt_log_fbl_fnames[0]),
            name_wo_ext)
        for bt_log_fbl_fname in arguments.bt_log_fbl_fnames:
            g = fbl_to_networkx(bt_log_fbl_fname)
            try:
                if previous_g is not None:
                    assert str(g.adj) == str(previous_g.adj), \
                        'Graphs must have the same structure'
                    f' {g.adj} != {previous_g.adj}'
                    for n in g.nodes:
                        assert str(g.nodes()[n]) == str(
                            previous_g.nodes()[n]), \
                            'Graphs must have the node attributes'
                        f' {g.nodes()[n]} != {previous_g.nodes()[n]}'
            except AssertionError as e:
                print(e)
                sys.exit(1)
            previous_g = g
            vc, vs = read_log_fbl(bt_log_fbl_fname, g)
            value_count = merge_values(value_count, vc)
            value_states = merge_values(value_states, vs)
        draw_pygraphviz_w_valuemod(
            g,
            path_wo_ext + '_fbl_log_count',
            value_mod=value_count,
        )
        draw_pygraphviz_w_returnstates(
            g,
            path_wo_ext + '_fbl_log_states',
            value_states=value_states,
        )

    # calculate coverage
    if arguments.coverage_threshold > 0.0:
        assert arguments.bt_log_fbl_fnames, 'Must provide log file'
        coverage = get_coverage(value_states)
        print(f'Coverage: {coverage}')
        if coverage < arguments.coverage_threshold:
            print(
                f'Coverage is below threshold {arguments.coverage_threshold}')
            sys.exit(1)

    # draw graph with demo values
    if arguments.demo:
        assert g is not None, 'Must provide a behavior tree'
        # demo_value_mod = make_demo_value(g)
        random.seed(0)
        demo_history = {
            k: list(
                random.choices(
                    [None] + [state.value for state in NODE_STATE],
                    k=10
                )
            ) for k in g.nodes
        }
        start_time = datetime.datetime.now()
        draw_pygraphviz_w_history(
            g,
            path_wo_ext + '_demo',
            value_history=demo_history
        )
        runtime = datetime.datetime.now() - start_time
        print(f'Runtime: {runtime}')


if __name__ == '__main__':
    main()
