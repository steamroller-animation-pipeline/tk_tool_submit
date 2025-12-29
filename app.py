# Copyright (c) 2025 Steamroller Studios
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
ShotGrid Desktop app wrapper for Steamroller Submit Tool.

This app provides a minimal wrapper that launches the existing Steamroller
Submit UI from ShotGrid Desktop. The actual UI and API code remain separate
in steamroller-ui-submit and steamroller-tools-submitter repositories.
"""

from sgtk.platform import Application
import os


class SubmitToolApp(Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """

    def init_app(self):
        """
        Called as the application is being initialized.
        """

        # First, we use the special import_module command to access the app module
        # that resides inside the python folder in the app. This is where the actual UI
        # and business logic of the app is kept. By using the import_module command,
        # toolkit's code reload mechanism will work properly.
        app_payload = self.import_module("app")

        # Now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and
        # whenever the user requests the command, it will call out to the callback.

        # First, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app
        menu_callback = lambda: app_payload.dialog.show_dialog(self)

        # Now register the command with the engine
        # This is the actual button/menu item that appears in ShotGrid Desktop
        # Get the icon path (256x256 PNG)
        icon_path = os.path.join(self.disk_location, "icon.png")
        
        self.engine.register_command(
            "Submit Tool",
            menu_callback,
            {
                "icon": icon_path,
                "description": "Launch the Steamroller Submission Tool UI"
            }
        )

