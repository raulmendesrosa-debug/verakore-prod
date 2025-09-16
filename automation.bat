@echo off
REM Verakore Workspace Automation - Windows Task Scheduler Integration
REM This script integrates with Windows Task Scheduler for cron-like functionality

setlocal enabledelayedexpansion

echo 🤖 Verakore Workspace Automation System
echo ========================================

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.x
    pause
    exit /b 1
)

REM Get current directory
set "WORKSPACE_DIR=%~dp0"
cd /d "%WORKSPACE_DIR%"

REM Check command line arguments
if "%1"=="" (
    set "COMMAND=check"
) else (
    set "COMMAND=%1"
)

echo 📁 Workspace: %WORKSPACE_DIR%
echo 🔧 Command: %COMMAND%
echo.

REM Run the automation system
python automation.py %COMMAND%

REM Check result
if errorlevel 1 (
    echo.
    echo ❌ Automation completed with errors
    echo 📋 Check automation.log for details
) else (
    echo.
    echo ✅ Automation completed successfully
)

echo.
echo Press any key to exit...
pause >nul
