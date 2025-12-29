@echo off
REM Wrapper script to launch Python script without showing console window
REM This script is called by rez-env and launches the Python script

REM Get the script directory
set SCRIPT_DIR=%~dp0

REM Launch Python script using pythonw.exe (windowless Python) if available
REM Otherwise use python.exe with window hidden
pythonw.exe "%SCRIPT_DIR%launch_submit_ui.py" 2>&1 | findstr /V "^$" > "%TEMP%\steamroller_submit_ui.log" 2>&1

REM If pythonw.exe doesn't exist, fall back to python.exe
if errorlevel 1 (
    python.exe "%SCRIPT_DIR%launch_submit_ui.py" > "%TEMP%\steamroller_submit_ui.log" 2>&1
)

