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

from bt_view.bt_view import draw_pygraphviz_w_history
from btlib.bts import fbl_to_networkx
from btlib.common import NODE_STATE
from nav2_msgs.msg import BehaviorTreeLog, BehaviorTreeStatusChange
from rcl_interfaces.msg import ParameterDescriptor
from rqt_bt_live.rqt_bt_live_widget import RqtBtLiveWidget
from rqt_gui_py.plugin import Plugin


def _has_uid(bt_status_change: BehaviorTreeStatusChange) -> bool:
    """
    Check if the uid field is present in the message.

    This is a workaround for the fact that the uid field was added
    later.
    """
    return '_uid' in bt_status_change.__slots__


class RqtBtLivePlugin(Plugin):
    """A plugin to visualize the behavior tree status."""

    def __init__(self, context):
        """Instantiate the plugin within its context with its initial state."""
        super(RqtBtLivePlugin, self).__init__(context)
        self.setObjectName('RqtBtLivePlugin')
        self._widget = RqtBtLiveWidget(context.serial_number())
        context.add_widget(self._widget)

        # Subscribing to all informations we want to display
        self._node = context.node
        self._node.create_subscription(
            BehaviorTreeLog, '/behavior_tree_log', self.bt_log_callback, 10)

        self.param_fbl_file = self._node.declare_parameter(
            'fbl_file',
            '',
            ParameterDescriptor(
                description='File to read the BT from.'))
        self.fbl_path = self.param_fbl_file.value
        self._node.get_logger().info(f'fbl_path: {self.fbl_path}')

        # read params
        self.img_path = os.path.join('/tmp', 'bt_trace')
        self._node.get_logger().info(f'{self.img_path=}')
        self.param_history_length = self._node.declare_parameter(
            'history_length',
            10,
            ParameterDescriptor(
                description='Length of the history to show per node.'))
        self.history_length = self.param_history_length.value
        self._node.get_logger().info(f'{self.history_length=}')

        self.g = fbl_to_networkx(self.fbl_path)
        # gray by default
        self.current_history = {
            n: [None] * self.history_length
            for n in self.g.nodes}
        self._node.get_logger().debug(f'{self.current_history=}')

        # make first image with gray nodes
        draw_pygraphviz_w_history(
            self.g,
            self.img_path,
            self.current_history)
        self._widget.set_image(self.img_path)

    def bt_log_callback(self, msg):
        """
        Call for the behavior tree log message.

        It will forward the message to the widget.

        :param msg: The message to be processed.
        """
        event_log = msg.event_log
        self._node.get_logger().debug(
            f'Received an BT log message with {len(event_log)} events')
        # roll history
        for node in self.current_history:
            self.current_history[node] = (
                self.current_history[node][1:] + [None])
        changed = False
        for event in event_log:
            assert isinstance(event, BehaviorTreeStatusChange)
            if _has_uid(event):
                self._node.get_logger().debug(
                    f'  Node {event.node_name} '
                    f'(No {event.uid}) '
                    f'changed status to {event.current_status}.')
                found_state = next(
                    (state for state in NODE_STATE
                     if state.name == event.current_status),
                    None,
                )
                self.current_history[event.uid][-1] = found_state.value
                changed = True
            else:
                self._node.get_logger().debug(
                    f'  Node {event.node_name} '
                    f'changed status to {event.current_status}.')
        if changed:
            draw_pygraphviz_w_history(
                self.g,
                self.img_path,
                self.current_history)
        self._node.get_logger().debug(f'{self.current_history=}')
        self._widget.set_image(self.img_path)


def main():
    import sys

    from rqt_gui.main import Main
    plugin = 'rqt_bt_live.rqt_bt_live.RqtBtLivePlugin'
    sys.exit(Main().main(
        sys.argv,
        standalone=plugin))
