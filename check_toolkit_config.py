#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to check if Toolkit can find and load the tk_tool_submit app.
Run this from ShotGrid Desktop Python console or standalone.
"""

import os
import sys

def check_app_structure():
    """Check if the app structure is correct."""
    print("=" * 60)
    print("Checking tk_tool_submit app structure...")
    print("=" * 60)
    
    app_path = r"D:\Steamroller\dev\tk_tool_submit"
    
    required_files = [
        "app.py",
        "info.yml",
        "python/__init__.py",
        "python/app/__init__.py",
        "python/app/dialog.py",
    ]
    
    all_good = True
    for file_path in required_files:
        full_path = os.path.join(app_path, file_path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_good = False
    
    return all_good

def check_config():
    """Check if config files reference the app correctly."""
    print("\n" + "=" * 60)
    print("Checking Toolkit configuration...")
    print("=" * 60)
    
    config_path = r"D:\Steamroller\dev\tk-config-steamroller\env\includes"
    
    # Check app_locations.yml
    app_locations_file = os.path.join(config_path, "app_locations.yml")
    if os.path.exists(app_locations_file):
        with open(app_locations_file, 'r') as f:
            content = f.read()
            if "tk_tool_submit" in content:
                print("✅ tk_tool_submit found in app_locations.yml")
            else:
                print("❌ tk_tool_submit NOT found in app_locations.yml")
    
    # Check tk-desktop.yml
    desktop_file = os.path.join(config_path, "settings", "tk-desktop.yml")
    if os.path.exists(desktop_file):
        with open(desktop_file, 'r') as f:
            content = f.read()
            if "tk-tool-submit.yml" in content:
                print("✅ tk-tool-submit.yml included in tk-desktop.yml")
            else:
                print("❌ tk-tool-submit.yml NOT included in tk-desktop.yml")
            
            if "tk_tool_submit" in content:
                print("✅ tk_tool_submit found in tk-desktop.yml apps")
            else:
                print("❌ tk_tool_submit NOT found in tk-desktop.yml apps")
    
    # Check tk-tool-submit.yml
    submit_file = os.path.join(config_path, "settings", "tk-tool-submit.yml")
    if os.path.exists(submit_file):
        print("✅ tk-tool-submit.yml exists")
    else:
        print("❌ tk-tool-submit.yml NOT found")

def check_toolkit_import():
    """Try to import Toolkit and check if app can be loaded."""
    print("\n" + "=" * 60)
    print("Checking Toolkit import (requires Toolkit environment)...")
    print("=" * 60)
    
    try:
        import sgtk
        print("✅ Toolkit (sgtk) imported successfully")
        
        # Try to get current bundle
        try:
            bundle = sgtk.platform.current_bundle()
            if bundle:
                print(f"✅ Current bundle: {bundle.name}")
            else:
                print("⚠️  No current bundle (this is okay if running standalone)")
        except Exception as e:
            print(f"⚠️  Could not get current bundle: {e}")
            print("   (This is okay if running outside Toolkit environment)")
        
    except ImportError:
        print("⚠️  Toolkit (sgtk) not available")
        print("   (This is okay if running standalone)")

if __name__ == "__main__":
    structure_ok = check_app_structure()
    check_config()
    check_toolkit_import()
    
    print("\n" + "=" * 60)
    if structure_ok:
        print("✅ App structure looks good!")
        print("\nNext steps:")
        print("1. Reload ShotGrid Desktop (Right-click project > Reload and Restart)")
        print("2. Check Toolkit logs: %APPDATA%\\Shotgun\\logs\\tk-desktop.log")
        print("3. Look for 'Submit Tool' in the menu")
    else:
        print("❌ App structure has issues - check missing files above")
    print("=" * 60)

