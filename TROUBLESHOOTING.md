# Troubleshooting: App Not Appearing in ShotGrid Desktop

## Quick Checks

### 1. Verify Configuration Files

Run the diagnostic script:
```bash
cd D:\Steamroller\dev\tk_tool_submit
python check_toolkit_config.py
```

### 2. Check Toolkit Logs

The Toolkit logs will show if the app is loading or if there are errors:

**Windows Log Location:**
```
%APPDATA%\Shotgun\logs\tk-desktop.log
```

**Look for:**
- `"Loading app: tk_tool_submit"`
- `"App tk_tool_submit initialized"`
- Any error messages related to `tk_tool_submit`

**Common Error Patterns:**
- `"App not found"` - Path issue
- `"Import error"` - Python path issue
- `"Syntax error"` - YAML or Python syntax issue

### 3. Verify App Path

Make sure the path in `app_locations.yml` is correct:
```yaml
apps.tk_tool_submit.location:
  type: dev
  path: D:/Steamroller/dev/tk_tool_submit
```

**Note:** Use forward slashes (`/`) in YAML paths, not backslashes.

### 4. Reload Toolkit Properly

1. **Full Reload:**
   - Close ShotGrid Desktop completely
   - Reopen ShotGrid Desktop
   - Select your project

2. **Reload from Menu:**
   - Right-click project → "Reload and Restart"
   - Or: Advanced → Reload

### 5. Check App Structure

Verify all files exist:
```
tk_tool_submit/
├── app.py                    ✅ Must exist
├── info.yml                  ✅ Must exist
├── python/
│   ├── __init__.py          ✅ Must exist
│   └── app/
│       ├── __init__.py      ✅ Must exist
│       └── dialog.py        ✅ Must exist
```

## Common Issues

### Issue: App Not in Menu

**Possible Causes:**
1. App failed to load (check logs)
2. App not in a group (should appear in "Setup Tools" now)
3. Configuration syntax error

**Solution:**
- Check logs for errors
- Verify YAML syntax is correct
- Try adding app directly without groups

### Issue: Import Error

**Error:** `"Failed to import Steamroller Submit UI"`

**Solution:**
- Ensure `steamroller-ui-submit` is in Python path
- Check if Rez packages are loaded
- Test imports manually (see `test_imports.py`)

### Issue: Path Not Found

**Error:** `"App path not found"`

**Solution:**
- Verify path exists: `D:\Steamroller\dev\tk_tool_submit`
- Check path uses forward slashes in YAML
- Ensure path is accessible

### Issue: YAML Syntax Error

**Error:** `"YAML parse error"`

**Solution:**
- Check for indentation issues (use spaces, not tabs)
- Verify all quotes are matched
- Check for trailing commas or colons

## Debug Steps

### Step 1: Check if Toolkit Sees the App

In ShotGrid Desktop Python console:
```python
import sgtk
engine = sgtk.platform.current_engine()
if engine:
    apps = engine.apps
    print("Loaded apps:")
    for app_name in apps.keys():
        print(f"  - {app_name}")
    
    # Check specifically for our app
    if 'tk_tool_submit' in apps:
        print("\n✅ tk_tool_submit is loaded!")
        app = apps['tk_tool_submit']
        print(f"   Location: {app.disk_location}")
    else:
        print("\n❌ tk_tool_submit is NOT loaded")
        print("\nCheck logs for errors:")
        print("%APPDATA%\\Shotgun\\logs\\tk-desktop.log")
```

### Step 2: Check Configuration

In ShotGrid Desktop:
1. Go to: **Advanced → Diagnostic → Show Configuration**
2. Look for `tk_tool_submit` in the apps list
3. Check if location path is correct

### Step 3: Test App Loading Manually

Create a test script to load the app:
```python
# test_app_load.py
import sys
import os

# Add Toolkit to path (adjust if needed)
sys.path.insert(0, r"C:\path\to\toolkit\python")

try:
    import sgtk
    from sgtk.platform import Application
    
    # Try to import the app
    app_path = r"D:\Steamroller\dev\tk_tool_submit"
    sys.path.insert(0, app_path)
    
    # Try importing app.py
    import app as submit_app
    print("✅ Successfully imported app.py")
    print(f"   App class: {submit_app.SubmitToolApp}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

## Where Should the App Appear?

After adding to "Setup Tools" group, the app should appear:
- In the **"Setup Tools"** section
- With the name **"Submit Tool"** (as registered in app.py)

If it doesn't appear:
1. Check if "Setup Tools" group is visible
2. Verify the group pattern matches: `"*Submit*"`
3. Check if app name matches pattern

## Still Not Working?

1. **Check Toolkit Version:**
   - Ensure Toolkit Core version meets requirements (v0.20.29+)
   - Check `info.yml` requirements

2. **Verify Engine:**
   - App should work in `tk-desktop` engine
   - Check if engine is loaded correctly

3. **Check Permissions:**
   - Ensure you have read access to app directory
   - Check if files are not locked

4. **Try Minimal Test:**
   - Temporarily simplify `app.py` to just print a message
   - See if app loads at all

5. **Compare with Working App:**
   - Compare structure with `tk-desktop-SRArez`
   - Check differences in configuration

## Getting Help

If still having issues, gather:
1. Toolkit logs (`tk-desktop.log`)
2. Output from `check_toolkit_config.py`
3. Output from `test_imports.py`
4. Screenshot of ShotGrid Desktop
5. Configuration files (relevant sections)

