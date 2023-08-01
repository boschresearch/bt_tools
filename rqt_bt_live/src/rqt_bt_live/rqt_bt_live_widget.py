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

import logging

from python_qt_binding import QT_BINDING_MODULES, QT_BINDING_VERSION
from python_qt_binding.QtCore import QUrl
from python_qt_binding.QtWebKitWidgets import QWebView
from python_qt_binding.QtWidgets import QWidget

logger = logging.getLogger(__name__)


class MyQWebView(QWebView):

    def __init__(self, parent):  # pragma no cover
        super(MyQWebView, self).__init__(parent)


class RqtBtLiveWidget(QWidget):
    """A widget to visualize the behavior tree status."""

    def __init__(self, serial_number):  # pragma no cover
        """
        Initialize the widget and loads the ui file.

        Widget content will be loaded from `rqt_bt_live.ui`.

        :param serial_number: A serial number to differentiate multiple
                              instances of the same widget.
        """
        logger.debug(f'{QT_BINDING_VERSION=}')
        logger.debug(f'{QT_BINDING_MODULES=}')
        super(RqtBtLiveWidget, self).__init__()
        logger.debug(f'{self.size()=}')

        self.qwv = MyQWebView(self)
        self.qwv.setGeometry(0, 0, 1000, 1000)
        self.qwv.load(QUrl('http://localhost:8000'))

        # Show windowTitle on left-top of each plugin.
        if serial_number > 1:
            self.setWindowTitle(
                self.windowTitle() + (' (%d)' % serial_number))
