@echo off
REM Verakore Security Scanner - Windows Integration
REM Comprehensive security validation and vulnerability scanning

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🔒 Verakore Security Scanner
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

REM Run the security scanner
python security.py %COMMAND%

REM Check result
if errorlevel 1 (
    echo.
    echo ❌ Security scan failed
    echo 📋 Check security.log for details
    echo.
    echo 🔧 Troubleshooting:
    echo   1. Check target URLs are accessible
    echo   2. Verify network connectivity
    echo   3. Review security configuration
) else (
    echo.
    echo ✅ Security scan completed successfully!
    echo 🔒 Security headers validated
    echo 🛡️ Vulnerability scan completed
    echo 📊 Security score calculated
)

echo.
echo 📋 Available Commands:
echo   • check: Run single security check
echo   • scan: Start continuous security scanning
echo   • report: Generate security report
echo   • setup: Setup security scanning
echo.

pause
