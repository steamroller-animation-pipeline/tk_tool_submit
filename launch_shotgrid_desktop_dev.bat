@echo off
REM Launcher script for ShotGrid Desktop with local dev config override
REM This ensures the TK_BOOTSTRAP_CONFIG_OVERRIDE is set before launching

set TK_BOOTSTRAP_CONFIG_OVERRIDE=D:\Steamroller\dev\tk-config-steamroller

REM Find ShotGrid Desktop executable
set SHOTGRID_DESKTOP="C:\Program Files\Shotgun\Shotgun.exe"

if exist %SHOTGRID_DESKTOP% (
    echo Launching ShotGrid Desktop with local dev config...
    echo Config override: %TK_BOOTSTRAP_CONFIG_OVERRIDE%
    start "" %SHOTGRID_DESKTOP%
) else (
    echo ERROR: ShotGrid Desktop not found at %SHOTGRID_DESKTOP%
    echo Please update the path in this script.
    pause
)

