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

# First, verify steamroller.core is available (required by steamroller/__init__.py)
# This must be done BEFORE adding dev paths, as dev paths might interfere with namespace package resolution
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

# IMPORTANT: Add dev paths AFTER steamroller.core is imported
# This allows dev code to take precedence for UI/submitter while keeping core dependencies from Rez
ui_dev_python_path = os.path.join(
    r"D:\Steamroller\dev\steamroller-ui-submit",
    "python"
)
submitter_dev_python_path = os.path.join(
    r"D:\Steamroller\dev\steamroller-tools-submitter",
    "python"
)

# Insert dev paths at the beginning of sys.path to take precedence over Rez-installed packages
# But only add the specific steamroller sub-paths, not the root steamroller namespace
if ui_dev_python_path not in sys.path:
    sys.path.insert(0, ui_dev_python_path)
    print(f"[DEV] Added UI dev path: {ui_dev_python_path}")
if submitter_dev_python_path not in sys.path:
    sys.path.insert(0, submitter_dev_python_path)
    print(f"[DEV] Added submitter dev path: {submitter_dev_python_path}")

# Also update steamroller namespace package __path__ to include dev paths
# This ensures Python finds dev modules within the steamroller namespace
try:
    import steamroller
    if hasattr(steamroller, '__path__'):
        ui_steamroller_path = os.path.join(ui_dev_python_path, "steamroller")
        submitter_steamroller_path = os.path.join(submitter_dev_python_path, "steamroller")
        
        if ui_steamroller_path not in steamroller.__path__:
            steamroller.__path__.insert(0, ui_steamroller_path)
            print(f"[DEV] Added UI path to steamroller.__path__: {ui_steamroller_path}")
        if submitter_steamroller_path not in steamroller.__path__:
            steamroller.__path__.insert(0, submitter_steamroller_path)
            print(f"[DEV] Added submitter path to steamroller.__path__: {submitter_steamroller_path}")
except Exception as e:
    print(f"[WARNING] Could not update steamroller.__path__: {e}")

# Now try to import the UI (will use dev code since we added it first)
try:
    from steamroller.ui.submit import main
    print("[OK] steamroller.ui.submit imported successfully")
    # Verify we're using dev code
    import steamroller.ui.submit.main as main_module
    main_file = main_module.__file__
    if "dev" in main_file.lower():
        print(f"[DEV] Using dev code from: {main_file}")
    else:
        print(f"[WARNING] Using installed code from: {main_file}")
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

