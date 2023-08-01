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

from rqt_bt_live.rqt_bt_live_widget import RqtBtLiveWidget
from rqt_gui_py.plugin import Plugin
import threading


class RqtBtLivePlugin(Plugin):
    """A plugin to visualize the behavior tree status."""

    def __init__(self, context):
        """Instantiate the plugin within its context with its initial state."""
        super(RqtBtLivePlugin, self).__init__(context)
        self.setObjectName('RqtBtLivePlugin')
        self._widget = RqtBtLiveWidget(context.serial_number())
        context.add_widget(self._widget)


def main():
    import sys

    from rqt_gui.main import Main as rqt_Main

    from bt_live_django.manage import main as django_main

    # threading.Thread(target=django_main).start()

    plugin = 'rqt_bt_live.rqt_bt_live.RqtBtLivePlugin'
    sys.exit(rqt_Main().main(
        sys.argv,
        standalone=plugin))
