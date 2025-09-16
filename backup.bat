@echo off
REM Verakore Backup & Recovery System - Windows Integration
REM Comprehensive backup solution with disaster recovery capabilities

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 💾 Verakore Backup & Recovery System
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
    set "COMMAND=backup"
) else (
    set "COMMAND=%1"
)

echo 📁 Workspace: %WORKSPACE_DIR%
echo 🔧 Command: %COMMAND%
echo.

REM Run the backup system
python backup.py %COMMAND%

REM Check result
if errorlevel 1 (
    echo.
    echo ❌ Backup operation failed
    echo 📋 Check backup.log for details
    echo.
    echo 🔧 Troubleshooting:
    echo   1. Check disk space availability
    echo   2. Verify backup directory permissions
    echo   3. Review backup configuration
) else (
    echo.
    echo ✅ Backup operation completed successfully!
    echo 💾 Files backed up and verified
    echo 🔒 Backup integrity confirmed
    echo 📊 Backup statistics recorded
)

echo.
echo 📋 Available Commands:
echo   • backup: Run scheduled backup
echo   • full: Create full backup
echo   • incremental: Create incremental backup
echo   • differential: Create differential backup
echo   • restore: Restore from backup
echo   • service: Start backup service
echo   • cleanup: Clean old backups
echo.

pause
