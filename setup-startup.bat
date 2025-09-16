@echo off
REM Verakore Workspace Auto-Start
REM Creates Windows startup entry for automatic health checks

setlocal enabledelayedexpansion

echo 🤖 Verakore Workspace Auto-Start Setup
echo ======================================

REM Get current directory
set "WORKSPACE_DIR=%~dp0"
set "STARTUP_SCRIPT=%WORKSPACE_DIR%startup-health-check.bat"

REM Check if startup script exists
if not exist "%STARTUP_SCRIPT%" (
    echo ❌ Startup script not found: %STARTUP_SCRIPT%
    pause
    exit /b 1
)

echo 📁 Workspace: %WORKSPACE_DIR%
echo 🔧 Startup script: %STARTUP_SCRIPT%

REM Create startup shortcut
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\Verakore Workspace Health Check.lnk"

echo.
echo 📋 Options:
echo 1. Add to Windows Startup (runs when Windows starts)
echo 2. Add to Current User Startup (runs when user logs in)
echo 3. Remove from Startup
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🔧 Adding to Windows Startup...
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%STARTUP_SCRIPT%'; $Shortcut.WorkingDirectory = '%WORKSPACE_DIR%'; $Shortcut.Save()"
    if errorlevel 1 (
        echo ❌ Failed to create startup shortcut
    ) else (
        echo ✅ Added to Windows Startup
        echo 💡 Health check will run when Windows starts
    )
) else if "%choice%"=="2" (
    echo 🔧 Adding to Current User Startup...
    set "USER_STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USER_STARTUP%\Verakore Workspace Health Check.lnk'); $Shortcut.TargetPath = '%STARTUP_SCRIPT%'; $Shortcut.WorkingDirectory = '%WORKSPACE_DIR%'; $Shortcut.Save()"
    if errorlevel 1 (
        echo ❌ Failed to create startup shortcut
    ) else (
        echo ✅ Added to Current User Startup
        echo 💡 Health check will run when you log in
    )
) else if "%choice%"=="3" (
    echo 🗑️ Removing from Startup...
    if exist "%SHORTCUT_PATH%" (
        del "%SHORTCUT_PATH%"
        echo ✅ Removed from Windows Startup
    ) else (
        echo ℹ️ No startup shortcut found
    )
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice
    pause
    exit /b 1
)

echo.
echo 📋 Manual Commands:
echo   • Run health check: startup-health-check.bat
echo   • Run automation: python automation.py check
echo   • Setup automation: setup-automation.bat
echo.

pause
