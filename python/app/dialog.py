# Copyright (c) 2025 Steamroller Studios
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

"""
Dialog launcher for Steamroller Submit Tool.

This module launches the Steamroller Submit UI as an external application
using Rez, similar to how tk-multi-launchapp launches DCC applications.
"""

import sgtk
import subprocess
import os
import sys

# Standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Launch the Steamroller Submit Tool UI as an external application using Rez.
    
    This function uses Rez to resolve the ui_submit package and
    all its dependencies, then launches the UI in that environment.
    
    Args:
        app_instance: The ShotGrid Toolkit app instance that provides context.
    """
    try:
        logger.info("Launching Steamroller Submit Tool from ShotGrid Desktop")
        
        # Get ShotGrid context if available
        context = app_instance.context
        project = context.project if context.project else None
        user = context.user if context.user else None
        
        if project:
            logger.info("Project context: %s (ID: %s)", project.get('name'), project.get('id'))
        if user:
            logger.info("User context: %s (ID: %s)", user.get('name'), user.get('id'))
        
        # Path to the launcher script
        launcher_script = os.path.join(
            app_instance.disk_location,
            "bin",
            "launch_submit_ui.py"
        )
        
        if not os.path.exists(launcher_script):
            error_msg = f"Launcher script not found at: {launcher_script}"
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        # Prepare project context to pass to the UI
        project_id = None
        project_name = None
        if project:
            project_id = project.get('id')
            project_name = project.get('name')
        
        # Launch using Rez: rez-env ui_submit yaml -- python launch_submit_ui.py
        # This will resolve all dependencies (steamroller.core, steamroller.qt, Qt.py, etc.)
        # Also include yaml (PyYAML) which is needed by steamroller.tools.submitter
        # Use 'python' instead of full path - Rez will provide Python in the environment
        # Pass project context via environment variables
        env = os.environ.copy()
        if project_id:
            env['SG_PROJECT_ID'] = str(project_id)
        if project_name:
            env['SG_PROJECT_NAME'] = project_name
        
        # Create a log file for debugging (temporary)
        log_file = os.path.join(os.environ.get('TEMP', os.path.expanduser('~')), 'steamroller_submit_ui.log')
        
        # Redirect output to log file in the command itself (works better with shell=True)
        if sys.platform == "win32":
            # On Windows, redirect both stdout and stderr to log file, and hide console window
            rez_command = f'powershell.exe -executionpolicy bypass rez-env ui_submit yaml -- python "{launcher_script}" > "{log_file}" 2>&1'
        else:
            # On Unix-like systems, redirect to log file
            rez_command = f'rez-env ui_submit yaml -- python "{launcher_script}" > "{log_file}" 2>&1'
        
        logger.info("Launching UI with Rez command: %s", rez_command)
        if project_id:
            logger.info("Passing project context: %s (ID: %s)", project_name, project_id)
        logger.info("Output will be logged to: %s", log_file)
        
        # Launch as a detached process directly using Rez
        # For GUI applications, launch without showing a console window
        # On Windows, use CREATE_NO_WINDOW flag to prevent console window
        if sys.platform == "win32":
            # Use CREATE_NO_WINDOW to prevent console window
            process = subprocess.Popen(
                rez_command,
                shell=True,
                stdout=subprocess.DEVNULL,  # Already redirected in command
                stderr=subprocess.DEVNULL,  # Already redirected in command
                stdin=subprocess.DEVNULL,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            # On Unix-like systems, run directly
            process = subprocess.Popen(
                rez_command,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                env=env
            )
        
        logger.info("Steamroller Submit Tool launched successfully (PID: %s)", process.pid)
        
    except FileNotFoundError as e:
        error_msg = f"Failed to launch Steamroller Submit Tool: {str(e)}"
        logger.error(error_msg)
        
        # Show error dialog
        try:
            from sgtk.platform.qt import QtWidgets
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowTitle("Launch Error")
            msg_box.setText(error_msg)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec_()
        except Exception:
            print("\n" + "="*60)
            print("ERROR: " + error_msg)
            print("="*60 + "\n")
    
    except Exception as e:
        error_msg = f"Failed to launch Steamroller Submit Tool: {str(e)}"
        logger.error(error_msg, exc_info=True)
        
        # Show error dialog
        try:
            from sgtk.platform.qt import QtWidgets
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Critical)
            msg_box.setWindowTitle("Launch Error")
            msg_box.setText(error_msg)
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msg_box.exec_()
        except Exception:
            print("\n" + "="*60)
            print("ERROR: " + error_msg)
            print("="*60 + "\n")
