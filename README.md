# tk_tool_submit

ShotGrid Desktop app wrapper for Steamroller Submit Tool.

## Overview

This is a minimal Toolkit app that provides a bridge between ShotGrid Desktop and the existing Steamroller Submit Tool. It allows users to launch the Submit Tool directly from ShotGrid Desktop while keeping the actual UI and API code separate in their respective repositories.

## Architecture

```
tk_tool_submit (this repo)
    └── Thin wrapper that launches:
        ├── steamroller-ui-submit (UI code)
        └── steamroller-tools-submitter (API/backend code)
```

## Components

- **`app.py`**: Main Toolkit app entry point that registers the menu command
- **`python/app/dialog.py`**: Launcher that calls the existing `steamroller.ui.submit.main.run()` function
- **`info.yml`**: App metadata and requirements

## Dependencies

This app requires:
- `steamroller-ui-submit`: The UI package
- `steamroller-tools-submitter`: The backend submission API
- ShotGrid Toolkit Core v0.20.29 or higher

## Installation

1. Clone this repository to your Toolkit apps location
2. Add the app to your Toolkit configuration:

```yaml
# In tk-config-*/env/includes/settings/tk-desktop.yml
settings.tk-desktop.project:
  apps:
    tk_tool_submit:
      location: "@apps.tk_tool_submit.location"
```

3. Add the app location to your `app_locations.yml`:

```yaml
apps.tk_tool_submit.location:
  type: dev
  path: D:/Steamroller/dev/tk_tool_submit
```

4. Reload ShotGrid Desktop or restart Toolkit

## Usage

Once installed, the "Submit Tool" command will appear in ShotGrid Desktop. Clicking it will launch the Steamroller Submit UI.

## Context Passing

Currently, the app launches the submit tool without automatically passing ShotGrid context. The submit tool will authenticate users independently.

Future enhancements could include:
- Automatically setting the project in the submit tool based on ShotGrid context
- Pre-filling user information
- Passing task/entity context

## Development

### Structure

```
tk_tool_submit/
├── app.py                    # Toolkit app entry point
├── info.yml                  # App metadata
├── README.md                 # This file
└── python/
    ├── __init__.py
    └── app/
        ├── __init__.py
        └── dialog.py         # Launcher implementation
```

### Testing

1. Ensure `steamroller-ui-submit` and `steamroller-tools-submitter` are in your Python path
2. Launch ShotGrid Desktop
3. Click the "Submit Tool" menu item
4. Verify the Submit UI launches correctly

## Related Repositories

- **steamroller-ui-submit**: The UI package for the submission tool
- **steamroller-tools-submitter**: The backend API for submissions

## License

See LICENSE file for details.

