# Deployment Guide for tk_tool_submit

This document outlines the steps required to deploy `tk_tool_submit` for production use.

## Current Status

Currently, `tk_tool_submit` is configured for **local development only**:
- **Location**: `D:/Steamroller/dev/tk_tool_submit` (dev path)
- **Rez Package**: Not yet installed in Rez repository
- **ShotGrid**: Not yet uploaded as a Toolkit app entity

## Deployment Requirements

### 1. Repository Setup

**Action Required**: Ensure `tk_tool_submit` repository is:
- ✅ Committed to version control (Git/Plastic SCM)
- ✅ Available in a shared repository location
- ✅ Tagged with a version number (e.g., `v1.0.0`)

**Current State**: Repository exists at `D:\Steamroller\dev\tk_tool_submit`

---

### 2. Rez Package Installation

**Action Required**: Install `tk_tool_submit` as a Rez package so it can be resolved by the `pipeline_configuration_init` hook.

**Steps**:
1. Copy `tk_tool_submit` to the Rez packages directory:
   ```
   Source: D:\Steamroller\dev\tk_tool_submit
   Destination: D:\steamroller_pipeline\packages\steamroller\tk_tool_submit\1.0.0\
   ```

2. Ensure the `package.py` file is correct (already configured correctly)

3. Verify Rez can resolve the package:
   ```bash
   rez-env tk_tool_submit -- echo "Package resolved successfully"
   ```

**Current State**: Package is NOT installed in Rez repository yet

**Note**: The `pipeline_configuration_init` hook expects `tk_tool_submit` to be resolvable via Rez. If it can't be resolved, it will be removed from the dependency list (as seen in the warnings).

---

### 3. ShotGrid Toolkit App Upload

**Action Required**: Upload `tk_tool_submit` to ShotGrid as a Toolkit app entity (similar to `tk-desktop-gluon-setup`).

**Steps**:
1. Create a zip file of the `tk_tool_submit` repository:
   ```bash
   # Exclude .git, __pycache__, etc.
   zip -r tk_tool_submit_v1.0.0.zip tk_tool_submit/ \
     -x "*.git*" "*__pycache__*" "*.pyc" "*.log"
   ```

2. Upload to ShotGrid:
   - Navigate to ShotGrid Admin → Pipeline → Toolkit Apps
   - Create a new `CustomNonProjectEntity02` entity (or use existing entity type)
   - Name: `tk_tool_submit`
   - Upload the zip file to the appropriate field (`sg_payload` or `attachment_links`)
   - Note the version number assigned by ShotGrid

3. Update `app_locations.yml`:
   ```yaml
   apps.tk_tool_submit.location:
     entity_type: CustomNonProjectEntity02
     type: shotgun
     name: tk_tool_submit
     field: sg_payload  # or attachment_links, depending on your setup
     version: <VERSION_NUMBER>  # Replace with actual version from ShotGrid
   ```

**Current State**: App is NOT uploaded to ShotGrid yet

**Reference**: See `tk-desktop-gluon-setup` in `app_locations.yml` (line 83-88) for example.

---

### 4. Configuration Updates

**Action Required**: Update `tk-config-steamroller` configuration files.

#### 4.1. `app_locations.yml`

**Current** (dev):
```yaml
apps.tk_tool_submit.location:
  type: dev
  path: D:/Steamroller/dev/tk_tool_submit
```

**Production** (choose one):

**Option A: ShotGrid (Recommended)**
```yaml
apps.tk_tool_submit.location:
  entity_type: CustomNonProjectEntity02
  type: shotgun
  name: tk_tool_submit
  field: sg_payload
  version: <VERSION_NUMBER>
```

**Option B: Git/Plastic SCM**
```yaml
apps.tk_tool_submit.location:
  type: git
  path: <repository_url>
  branch: main
  version: v1.0.0
```

#### 4.2. `tool_dependencies.json`

**Current**: ✅ Already configured
```json
{
    "packages": [
        ...
        "tk_tool_submit"
    ]
}
```

**Action**: Ensure `tk_tool_submit` Rez package is installed (see step 2).

#### 4.3. `tk-desktop.yml`

**Current**: ✅ Already configured correctly
- App is listed in `settings.tk-desktop.site.apps`
- App is listed in `settings.tk-desktop.project.apps`
- App is in the "Submission & Publishing" group

**Action**: No changes needed.

---

### 5. Dependencies Verification

**Action Required**: Verify all dependencies are available in Rez:

- ✅ `steamroller.ui.submit` (already in Rez)
- ✅ `yaml` (PyYAML, already in Rez)
- ✅ `steamroller.core` (dependency of steamroller.ui.submit)
- ✅ `steamroller.qt` (dependency of steamroller.ui.submit)
- ✅ `steamroller.tools.submitter` (dependency of steamroller.ui.submit)

**Current State**: All dependencies should be available. The `pipeline_configuration_init` hook will resolve them automatically.

---

## Deployment Checklist

### Pre-Deployment
- [ ] Code is committed and tagged with version number
- [ ] All tests pass locally
- [ ] Documentation is complete

### Deployment Steps
- [ ] Install `tk_tool_submit` Rez package to repository
- [ ] Verify Rez can resolve `tk_tool_submit` package
- [ ] Upload `tk_tool_submit` to ShotGrid as Toolkit app entity
- [ ] Update `app_locations.yml` with production location
- [ ] Commit configuration changes to `tk-config-steamroller`
- [ ] Test on a non-dev machine/user account

### Post-Deployment Verification
- [ ] App appears in ShotGrid Desktop for all users
- [ ] App launches without errors
- [ ] Project context is correctly passed to UI
- [ ] No console windows appear (Windows)
- [ ] Log files are created correctly (if needed for debugging)

---

## Rollback Plan

If issues occur after deployment:

1. **Revert Configuration**: Change `app_locations.yml` back to dev path temporarily
2. **Remove from Rez**: Delete `tk_tool_submit` package from Rez repository if needed
3. **ShotGrid**: Disable or remove the Toolkit app entity in ShotGrid

---

## Notes

### Development vs Production

**Development** (current):
- Uses `type: dev` with local path
- Requires `TK_BOOTSTRAP_CONFIG_OVERRIDE` environment variable
- Only works for developers with local repository

**Production**:
- Uses `type: shotgun` with ShotGrid entity
- Works for all users automatically
- No environment variables needed

### Rez Package vs ShotGrid App

- **Rez Package**: Required for `pipeline_configuration_init` hook to resolve dependencies
- **ShotGrid App**: Required for Toolkit to download and cache the app for users

Both are needed for full deployment.

---

## Questions to Answer Before Deployment

1. **Where should the Rez package be installed?**
   - Path: `D:\steamroller_pipeline\packages\steamroller\tk_tool_submit\1.0.0\`?
   - Or different location?

2. **What ShotGrid entity type should be used?**
   - `CustomNonProjectEntity02` (like `tk-desktop-gluon-setup`)?
   - Or `CustomNonProjectEntity01` (like `tk-multi-versionsubmit`)?

3. **What field should store the app payload?**
   - `sg_payload`?
   - `attachment_links`?

4. **Who has permissions to upload to ShotGrid?**
   - Pipeline team?
   - Specific user?

5. **What is the deployment process for `tk-config-steamroller`?**
   - How are config changes deployed?
   - Who approves changes?

---

## Summary

**Minimum Required Changes for Production**:

1. ✅ Install `tk_tool_submit` Rez package
2. ✅ Upload app to ShotGrid
3. ✅ Update `app_locations.yml` to use ShotGrid location
4. ✅ Commit and deploy `tk-config-steamroller` changes

**Files Modified**:
- `tk-config-steamroller/env/includes/app_locations.yml` (change location type)
- `tk-config-steamroller/core/hooks/tool_dependencies.json` (already done)
- `tk-config-steamroller/env/includes/settings/tk-desktop.yml` (already done)

**Files Created**:
- `tk_tool_submit/` repository (needs to be committed and tagged)

