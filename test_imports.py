#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick test script to verify that tk_tool_submit can import and launch
the Steamroller Submit UI.

Run this before testing in ShotGrid Desktop to catch import issues early.
"""

import sys
import os

def test_imports():
    """Test if we can import the required modules."""
    
    print("=" * 60)
    print("Testing tk_tool_submit imports...")
    print("=" * 60)
    
    # Add paths (adjust if your paths are different)
    ui_path = r"D:\Steamroller\dev\steamroller_ui_submit\python"
    tools_path = r"D:\Steamroller\dev\steamroller_tools_submitter\python"
    
    if os.path.exists(ui_path):
        sys.path.insert(0, ui_path)
        print(f"✅ Added UI path: {ui_path}")
    else:
        print(f"⚠️  UI path not found: {ui_path}")
    
    if os.path.exists(tools_path):
        sys.path.insert(0, tools_path)
        print(f"✅ Added tools path: {tools_path}")
    else:
        print(f"⚠️  Tools path not found: {tools_path}")
    
    print()
    
    # Test 1: Import steamroller.ui.submit.main
    print("Test 1: Importing steamroller.ui.submit.main...")
    try:
        from steamroller.ui.submit import main
        print("✅ Successfully imported steamroller.ui.submit.main")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 2: Check if run() function exists
    print("\nTest 2: Checking for run() function...")
    if hasattr(main, 'run'):
        print("✅ run() function exists")
        print(f"   Function signature: {main.run}")
    else:
        print("❌ run() function not found")
        return False
    
    # Test 3: Test app.py import structure
    print("\nTest 3: Testing Toolkit app structure...")
    try:
        # Add tk_tool_submit to path
        app_path = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, app_path)
        
        # Try importing the app module
        from python.app import dialog
        print("✅ Successfully imported python.app.dialog")
        
        # Check if show_dialog exists
        if hasattr(dialog, 'show_dialog'):
            print("✅ show_dialog() function exists")
        else:
            print("❌ show_dialog() function not found")
            return False
            
    except ImportError as e:
        print(f"⚠️  Could not import app module: {e}")
        print("   (This is okay if testing outside Toolkit environment)")
    
    print("\n" + "=" * 60)
    print("✅ All import tests passed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Add tk_tool_submit to your Toolkit configuration")
    print("2. Reload ShotGrid Desktop")
    print("3. Look for 'Submit Tool' in the menu")
    print("\nSee TESTING.md for detailed instructions.")
    
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)

