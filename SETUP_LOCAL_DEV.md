# Setting Up Local Dev Configuration for ShotGrid Desktop

## Problem
ShotGrid Desktop is loading a cached configuration from ShotGrid storage (`v1229186`) instead of your local dev configuration at `D:\Steamroller\dev\tk-config-steamroller`. This means changes to the local config files won't be picked up.

## Solution: Use TK_BOOTSTRAP_CONFIG_OVERRIDE and REZ_SERVER_ROOT

Set both `TK_BOOTSTRAP_CONFIG_OVERRIDE` and `REZ_SERVER_ROOT` environment variables for local dev:
- `TK_BOOTSTRAP_CONFIG_OVERRIDE`: Points Toolkit to your local dev configuration
- `REZ_SERVER_ROOT`: Points to local Rez server path (needed for Maya launch to work)

### Windows PowerShell (Current Session)
```powershell
$env:TK_BOOTSTRAP_CONFIG_OVERRIDE = "D:\Steamroller\dev\tk-config-steamroller"
$env:REZ_SERVER_ROOT = "D:\steamroller_pipeline"
```

### Windows Command Prompt (Current Session)
```cmd
set TK_BOOTSTRAP_CONFIG_OVERRIDE=D:\Steamroller\dev\tk-config-steamroller
set REZ_SERVER_ROOT=D:\steamroller_pipeline
```

### Permanent Setup (System Environment Variable)
1. Open **System Properties** → **Environment Variables**
2. Under **User variables**, click **New** and add:
   - Variable name: `TK_BOOTSTRAP_CONFIG_OVERRIDE`
   - Variable value: `D:\Steamroller\dev\tk-config-steamroller`
3. Click **New** again and add:
   - Variable name: `REZ_SERVER_ROOT`
   - Variable value: `D:\steamroller_pipeline`
4. Click **OK** on all dialogs
5. **Restart ShotGrid Desktop** for the change to take effect

**Note:** The `NEW_REZ_DEPENDENCY_LIST.json` file must exist at `D:\steamroller_pipeline\NEW_REZ_DEPENDENCY_LIST.json` for Maya launch to work. A minimal file has been created for local dev.

### Permanent Setup (PowerShell Profile)
Add this to your PowerShell profile (`$PROFILE`):
```powershell
$env:TK_BOOTSTRAP_CONFIG_OVERRIDE = "D:\Steamroller\dev\tk-config-steamroller"
$env:REZ_SERVER_ROOT = "D:\steamroller_pipeline"
```

## Verification

After setting the environment variable and restarting ShotGrid Desktop, run this in the ShotGrid Desktop Python Console:

```python
import sgtk
import os
engine = sgtk.platform.current_engine()
env = engine._Engine__env
print("Environment path:", env._env_path)
print("Expected: D:\\Steamroller\\dev\\tk-config-steamroller")
print("Config override:", os.environ.get("TK_BOOTSTRAP_CONFIG_OVERRIDE"))
```

The environment path should now point to your local dev config, and `tk_tool_submit` should appear in the configured apps.

## Notes

- **Always restart ShotGrid Desktop** after setting/changing the environment variable
- The override takes precedence over all other configuration methods
- This is intended for development - production should use uploaded configs in ShotGrid
- If you want to go back to using the cached config, simply remove or unset the environment variable

