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

from ament_index_python.packages import get_package_share_directory
from python_qt_binding import loadUi
from python_qt_binding.QtGui import QPixmap
from python_qt_binding.QtWidgets import QWidget


class RqtBtLiveWidget(QWidget):
    """A widget to visualize the behavior tree status."""

    def __init__(self, serial_number):  # pragma no cover
        """
        Initialize the widget and loads the ui file.

        Widget content will be loaded from `rqt_bt_live.ui`.

        :param serial_number: A serial number to differentiate multiple
                              instances of the same widget.
        """
        super(RqtBtLiveWidget, self).__init__()
        ui_file = os.path.join(
            get_package_share_directory('rqt_bt_live'),
            'resource',
            'rqt_bt_live.ui')
        loadUi(ui_file, self)
        # Checking if widget is loaded correctly from ui file
        assert self.imageLabel, 'Label must be loaded from ui file'
        self.setObjectName('rqt_bt_liveUi')
        # Show windowTitle on left-top of each plugin.
        if serial_number > 1:
            self.setWindowTitle(
                self.windowTitle() + (' (%d)' % serial_number))

    def set_image(self, _path):
        """Set the image of the widget."""
        image_path = _path + '.png'
        self.imageLabel.setPixmap(QPixmap(image_path))
