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

from bt_view.bt_view import draw_pygraphviz_w_colorvalues
from btlib.bts import fbl_to_networkx
from btlib.common import NODE_STATE
from nav2_msgs.msg import BehaviorTreeLog
from nav2_msgs.msg import BehaviorTreeStatusChange
from rcl_interfaces.msg import ParameterDescriptor
import rclpy
from rclpy.node import Node


def _has_uid(bt_status_change: BehaviorTreeStatusChange) -> bool:
    """
    Check if the uid field is present in the message.

    This is a workaround for the fact that the uid field was added
    later.
    """
    return '_uid' in bt_status_change.__slots__


class Listener(Node):

    def __init__(self):
        super().__init__('bt_live')
        self.subscription = self.create_subscription(
            BehaviorTreeLog,
            '/behavior_tree_log',
            self.listener_callback,
            10)

        self.param_fbl_file = self.declare_parameter(
            'fbl_file',
            '',
            ParameterDescriptor(
                description='File to read the BT from.'))
        self.fbl_path = self.param_fbl_file.value
        self.get_logger().info(f'fbl_path: {self.fbl_path}')

        self.param_img_path = self.declare_parameter(
            'img_path',
            '',
            ParameterDescriptor(
                description='Path to save the image to.'))
        self.img_path = self.param_img_path.value
        self.get_logger().info(f'img_path: {self.img_path}')

        self.g = fbl_to_networkx(self.fbl_path)
        # gray by default
        self.empty_valuemap = {n: '#DDDDDD' for n in self.g.nodes}
        self.get_logger().info(f'{self.empty_valuemap=}')

    def listener_callback(self, msg: BehaviorTreeLog):
        event_log = msg.event_log
        self.get_logger().info(
            f'Received an BT log message with {len(event_log)} events')
        value_map = self.empty_valuemap.copy()
        changed = False
        for event in event_log:
            assert isinstance(event, BehaviorTreeStatusChange)
            if _has_uid(event):
                self.get_logger().info(
                    f'  Node {event.node_name} '
                    f'(No {event.uid}) '
                    f'changed status to {event.current_status}.')
                if event.current_status == NODE_STATE.SUCCESS.name:
                    value_map[event.uid] = '#00FF00'
                elif event.current_status == NODE_STATE.FAILURE.name:
                    value_map[event.uid] = '#FF0000'
                elif event.current_status == NODE_STATE.RUNNING.name:
                    value_map[event.uid] = '#FFFF00'
                changed = True
            else:
                self.get_logger().info(
                    f'  Node {event.node_name} '
                    f'changed status to {event.current_status}.')
        if changed:
            draw_pygraphviz_w_colorvalues(
                self.g,
                self.img_path,
                value_map)
        self.get_logger().info(f'{value_map=}')


def main(args=None):
    rclpy.init(args=args)
    bt_live = Listener()

    try:
        rclpy.spin(bt_live)
    except KeyboardInterrupt:
        bt_live.get_logger().info('Bye')
        bt_live.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
