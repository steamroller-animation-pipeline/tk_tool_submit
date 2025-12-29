# -*- coding: utf-8 -*-
############
# Package for tk_tool_submit Toolkit app
# This package depends on steamroller.ui.submit which will pull in all required dependencies
############
name = "tk_tool_submit"
version = "1.0.0"
description = "ShotGrid Toolkit app wrapper for Steamroller Submit Tool"
authors = ["Steamroller Studios"]
requires = [
    "steamroller.ui.submit",  # This will pull in steamroller.core, steamroller.qt, Qt.py, steamroller.tools.submitter, etc.
]

def commands():
    env.PATH.append("{root}/bin")
    env.PYTHONPATH.append("{root}/python")

uuid = "tk_tool_submit"
format_version = 2
install_directory = "steamroller"

