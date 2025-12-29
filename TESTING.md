# Testing Guide for tk_tool_submit

This guide walks you through testing the `tk_tool_submit` app in ShotGrid Desktop.

## Prerequisites

Before testing, ensure:
1. ✅ `steamroller-ui-submit` is installed and available in your Python path
2. ✅ `steamroller-tools-submitter` is installed and available in your Python path
3. ✅ ShotGrid Desktop is installed and running
4. ✅ You have access to a Toolkit project configuration

## Step 1: Add App to Toolkit Configuration

### Option A: Development Testing (Recommended for initial testing)

Add the app location to `tk-config-steamroller/env/includes/app_locations.yml`:

```yaml
apps.tk_tool_submit.location:
  type: dev
  path: D:/Steamroller/dev/tk_tool_submit
```

### Option B: ShotGrid Storage (For production)

Upload the app to ShotGrid and reference it:

```yaml
apps.tk_tool_submit.location:
  type: shotgun
  entity_type: CustomNonProjectEntity02
  name: tk_tool_submit
  field: sg_payload
  version: <version_number>
```

## Step 2: Add App to Desktop Settings

Edit `tk-config-steamroller/env/includes/settings/tk-desktop.yml`:

Add the app to the `settings.tk-desktop.project.apps` section:

```yaml
settings.tk-desktop.project:
  apps:
    # ... existing apps ...
    tk_tool_submit:
      location: "@apps.tk_tool_submit.location"
```

You can also create a settings file similar to `tk-desktop-SRArez.yml`:

Create `tk-config-steamroller/env/includes/settings/tk-tool-submit.yml`:

```yaml
includes:
- ../app_locations.yml
- ../engine_locations.yml

settings.tk-tool-submit:
  location: "@apps.tk_tool_submit.location"
```

Then include it in `tk-desktop.yml`:

```yaml
includes:
- ../app_locations.yml
- ../engine_locations.yml
- ./tk-multi-launchapp.yml
- ./tk-multi-screeningroom.yml
- ./tk-desktop-SRArez.yml
- ./tk-tool-submit.yml  # Add this line
```

## Step 3: Reload Toolkit Configuration

### Method 1: Reload in ShotGrid Desktop
1. Open ShotGrid Desktop
2. Right-click on your project
3. Select **"Reload and Restart"** or **"Advanced > Reload"**

### Method 2: Restart ShotGrid Desktop
1. Close ShotGrid Desktop completely
2. Reopen ShotGrid Desktop
3. Select your project

## Step 4: Verify App is Loaded

1. In ShotGrid Desktop, look for the **"Submit Tool"** menu item
2. It should appear in the main menu or in a tools group
3. If you don't see it, check the Toolkit logs (see Troubleshooting below)

## Step 5: Test Launching the App

1. Click **"Submit Tool"** in ShotGrid Desktop
2. The Steamroller Submit UI should launch
3. Verify:
   - ✅ UI window appears
   - ✅ No error dialogs
   - ✅ UI is functional (can select projects, tasks, etc.)

## Step 6: Test Functionality

1. **Project Selection**: Verify you can select a project
2. **Task Selection**: Verify you can select tasks
3. **File Submission**: Try submitting a test file (if safe to do so)
4. **Error Handling**: Test what happens if dependencies are missing

## Troubleshooting

### App Doesn't Appear in Menu

**Check Toolkit Logs:**
- Location: `%APPDATA%\Shotgun\logs\tk-desktop.log` (Windows)
- Look for errors related to `tk_tool_submit`
- Common issues:
  - App path incorrect
  - Missing `app.py` or `info.yml`
  - Syntax errors in YAML files

**Verify Configuration:**
```bash
# Check if app location is correct
# In ShotGrid Desktop, go to: Advanced > Diagnostic > Show Configuration
# Look for tk_tool_submit in the apps list
```

### Import Error: "Failed to import Steamroller Submit UI"

**Check Python Path:**
- Ensure `steamroller-ui-submit` is in your Python path
- Verify `steamroller.tools.submitter` is available
- Check if packages are installed via Rez or pip

**Test Import Manually:**
```python
# In Python console or ShotGrid Desktop Python console
import sys
sys.path.append(r"D:\Steamroller\dev\steamroller-ui-submit\python")
sys.path.append(r"D:\Steamroller\dev\steamroller-tools-submitter\python")

from steamroller.ui.submit import main
main.run()
```

### App Crashes on Launch

**Check Logs:**
- Look for stack traces in Toolkit logs
- Check for Qt/PyQt version conflicts
- Verify all dependencies are installed

**Common Issues:**
- Qt version mismatch (Toolkit uses specific Qt version)
- Missing dependencies (PyQt, steamroller.core, etc.)
- Python version incompatibility

### Quick Test Script

Create a test script to verify imports work:

```python
# test_imports.py
import sys
import os

# Add paths
sys.path.insert(0, r"D:\Steamroller\dev\steamroller-ui-submit\python")
sys.path.insert(0, r"D:\Steamroller\dev\steamroller-tools-submitter\python")

try:
    from steamroller.ui.submit import main
    print("✅ Successfully imported steamroller.ui.submit.main")
    
    # Try to get the run function
    if hasattr(main, 'run'):
        print("✅ run() function exists")
    else:
        print("❌ run() function not found")
        
except ImportError as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
```

Run it:
```bash
python test_imports.py
```

## Debug Mode

To see more detailed logging:

1. Enable debug logging in Toolkit:
   - ShotGrid Desktop > Advanced > Diagnostic > Enable Debug Logging

2. Check logs in real-time:
   - `%APPDATA%\Shotgun\logs\tk-desktop.log`

3. Look for messages like:
   - `"Launching Steamroller Submit Tool from ShotGrid Desktop"`
   - `"Project context: ..."`
   - `"Steamroller Submit Tool launched successfully"`

## Expected Behavior

When working correctly:
1. ✅ "Submit Tool" appears in ShotGrid Desktop menu
2. ✅ Clicking it launches the Submit UI window
3. ✅ UI is fully functional
4. ✅ No error messages
5. ✅ Logs show successful launch

## Next Steps After Testing

Once testing is successful:
1. Commit the configuration changes
2. Deploy to other projects/configs if needed
3. Consider uploading to ShotGrid storage for production use
4. Update version number in `package.py` and `info.yml` as needed

## Support

If you encounter issues:
1. Check Toolkit logs first
2. Verify all dependencies are installed
3. Test imports manually
4. Check Python path configuration
5. Review error messages in detail

