@echo off
REM Verakore Performance Monitoring - Windows Integration
REM Monitors Core Web Vitals, performance metrics, and provides optimization insights

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 📊 Verakore Performance Monitoring
echo ========================================
echo.

REM Get current directory
set "WORKSPACE_DIR=%~dp0"
cd /d "%WORKSPACE_DIR%"

REM Check Python availability
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.x
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check command line arguments
if "%1"=="" (
    set "COMMAND=check"
) else (
    set "COMMAND=%1"
)

echo 📁 Workspace: %WORKSPACE_DIR%
echo 🔧 Command: %COMMAND%
echo.

REM Run the performance monitoring
python performance.py %COMMAND%

REM Check result
if errorlevel 1 (
    echo.
    echo ❌ Performance monitoring failed
    echo 📋 Check performance.log for details
    echo.
    echo 🔧 Troubleshooting:
    echo   1. Install Lighthouse CLI: npm install -g lighthouse
    echo   2. Check Chrome installation
    echo   3. Verify target URLs are accessible
) else (
    echo.
    echo ✅ Performance monitoring completed successfully!
    echo 📊 Core Web Vitals analyzed
    echo 🎯 Optimization recommendations generated
    echo 📈 Performance trends tracked
)

echo.
echo 📋 Available Commands:
echo   • check: Run single performance check
echo   • monitor: Start continuous monitoring
echo   • report: Generate performance report
echo   • setup: Setup performance monitoring
echo.

pause
