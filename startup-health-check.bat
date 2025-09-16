@echo off
REM Verakore Workspace Startup Health Check
REM Runs automatically when workspace is opened

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🤖 Verakore Workspace Health Check
echo ========================================
echo.

REM Get current directory
set "WORKSPACE_DIR=%~dp0"
cd /d "%WORKSPACE_DIR%"

REM Check if this is the first run today
set "TODAY=%date:~-4,4%%date:~-10,2%%date:~-7,2%"
set "LAST_RUN_FILE=last_run_%TODAY%.txt"

if exist "%LAST_RUN_FILE%" (
    echo ℹ️ Health check already run today
    echo 💡 Run 'python automation.py check' for manual check
    goto :end
)

REM Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.x
    echo 💡 Download from: https://www.python.org/downloads/
    goto :end
)

echo ✅ Python found
echo.

REM Run health check
echo 🔍 Running workspace health check...
python automation.py check

REM Mark as run today
echo %date% %time% > "%LAST_RUN_FILE%"

REM Check result
if errorlevel 1 (
    echo.
    echo ⚠️ Health check completed with issues
    echo 📋 Check automation.log for details
    echo 💡 Run 'python automation.py check' to see details
) else (
    echo.
    echo ✅ Workspace is healthy and ready!
)

echo.
echo 📋 Quick Commands:
echo   • Health Check: python automation.py check
echo   • Daily Maintenance: python automation.py daily
echo   • Weekly Maintenance: python automation.py weekly
echo   • Setup Automation: setup-automation.bat
echo.

:end
echo Press any key to continue...
pause >nul
