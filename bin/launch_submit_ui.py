#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Launcher script for Steamroller Submit UI.

This script is executed by Rez to launch the UI with all dependencies resolved.
Rez should have already set up PYTHONPATH with steamroller.ui.submit and all its dependencies.
"""

import sys
import os

# Debug: Print PYTHONPATH to see what Rez set up
print("PYTHONPATH:", os.environ.get("PYTHONPATH", "Not set"))
print("sys.path (first 10):", sys.path[:10])

# Verify steamroller.core is available (required by steamroller/__init__.py)
try:
    import steamroller.core
    print("[OK] steamroller.core found")
except ImportError as e:
    print(f"[ERROR] steamroller.core not found: {e}")
    print("Available steamroller paths in sys.path:")
    for p in sys.path:
        if "steamroller" in p.lower():
            print(f"  - {p}")
    raise

# Import the UI (Rez should have set up all dependencies in PYTHONPATH)
try:
    from steamroller.ui.submit import main
    print("[OK] steamroller.ui.submit imported successfully")
except ImportError as e:
    print(f"[ERROR] Failed to import steamroller.ui.submit: {e}")
    import traceback
    traceback.print_exc()
    raise

# Get project context from environment variables (set by dialog.py)
project_id = os.environ.get("SG_PROJECT_ID")
project_name = os.environ.get("SG_PROJECT_NAME")

# Set project in QSettings so the UI will load it automatically
if project_id:
    try:
        from Qt import QtCore
        from steamroller.ui.submit import constants
        
        # Set the project ID in QSettings (same way the UI saves it)
        settings = QtCore.QSettings(constants.ORGANIZATION_NAME, "SubmitUI")
        settings.setValue("task/project", int(project_id))
        settings.sync()
        print(f"[OK] Set project in settings: {project_name} (ID: {project_id})")
    except Exception as e:
        print(f"[WARNING] Could not set project in settings: {e}")

# Run the UI
print("Launching UI...")
main.run()

