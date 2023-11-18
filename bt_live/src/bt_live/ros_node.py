import os
import tempfile

from bt_view.bt_view import COLORS_PER_RETURN_STATE, draw_pygraphviz

from btlib.bts import fbl_to_networkx
from btlib.common import NODE_STATE

from nav2_msgs.msg import BehaviorTreeLog, BehaviorTreeStatusChange

from rcl_interfaces.msg import ParameterDescriptor

import rclpy
from rclpy.node import Node
from rclpy.time import Time


def _has_uid(bt_status_change: BehaviorTreeStatusChange) -> bool:
    """
    Check if the uid field is present in the message.

    This is a workaround for the fact that the uid field was added
    later.
    """
    return '_uid' in bt_status_change.__slots__


class SingletonBtLiveNode():
    _instance = None

    def __init__(self, args=None):
        if SingletonBtLiveNode._instance is None:
            SingletonBtLiveNode._instance = BtLiveNode(args=args)

    def __getattr__(self, name):
        return getattr(self._instance, name)

    def __call__(self, *args, **kwargs):
        return self._instance(*args, **kwargs)


class BtLiveNode(Node):

    def __init__(self, args=None):
        rclpy.init(args=args)
        super().__init__('bt_live_node')
        self.get_logger().info('Starting bt_live_node')
        self.data = {}
        self.sub = self.create_subscription(
            BehaviorTreeLog,
            '/behavior_tree_log',
            self.callback,
            10
        )

        # setting paths
        self.param_fbl_file = self.declare_parameter(
            'fbl_file',
            '',
            ParameterDescriptor(
                description='File to read the BT from.'))
        self.fbl_file = self.param_fbl_file.value
        if self.fbl_file == '':
            raise ValueError('No file specified. Please specify the file to'
                             'read the BT from under the parameter '
                             '`fbl_file`.')
        if not os.path.exists(self.fbl_file):
            raise FileNotFoundError(
                f'File under path fbl_file={self.fbl_file} does not exist.')
        self.img_path = os.path.join(tempfile.gettempdir(), 'bt_trace')
        self.get_logger().info(f'{self.img_path=}')

        self.g = fbl_to_networkx(self.fbl_file)

        # make first image with gray nodes
        draw_pygraphviz(
            self.g,
            self.img_path,
            lambda _: None,)

    def callback(self, msg: BehaviorTreeStatusChange):
        event_log = msg.event_log
        self.data = {'timestamp': Time().from_msg(msg.timestamp).nanoseconds}
        for event in event_log:
            assert isinstance(event, BehaviorTreeStatusChange)
            if _has_uid(event):
                # self.data[event.node_name] = event.current_status
                found_state = next(
                    (state for state in NODE_STATE
                     if state.name == event.current_status),
                    None,
                )
                self.data[event.uid] = COLORS_PER_RETURN_STATE[
                    found_state
                ]

    def spin_once(self):
        rclpy.spin_once(self)
        return self.data
