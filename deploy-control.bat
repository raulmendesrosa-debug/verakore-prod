@echo off
REM Verakore Deployment Control - Windows Batch Launcher
REM This launches the PowerShell deployment control script

echo ========================================
echo   VERAKORE DEPLOYMENT CONTROL SYSTEM
echo ========================================
echo.

REM Check if PowerShell is available
powershell -Command "Get-Host" >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PowerShell is not available on this system.
    echo Please install PowerShell to use the deployment control system.
    pause
    exit /b 1
)

REM Launch the PowerShell script
echo Starting Deployment Control System...
echo.

REM Pass all command line arguments to PowerShell script
if "%1"=="" (
    powershell -ExecutionPolicy Bypass -File "%~dp0deployment-control.ps1" menu
) else (
    powershell -ExecutionPolicy Bypass -File "%~dp0deployment-control.ps1" %*
)

echo.
echo Deployment Control System finished.
pause
