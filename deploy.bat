@echo off
REM Verakore Deployment Pipeline - Windows Integration
REM Automated deployment with quality gates and rollback

setlocal enabledelayedexpansion

echo.
echo ========================================
echo 🚀 Verakore Deployment Pipeline
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
    set "COMMAND=deploy"
) else (
    set "COMMAND=%1"
)

echo 📁 Workspace: %WORKSPACE_DIR%
echo 🔧 Command: %COMMAND%
echo.

REM Run the deployment pipeline
python deploy.py %COMMAND%

REM Check result
if errorlevel 1 (
    echo.
    echo ❌ Deployment pipeline failed
    echo 📋 Check deployment.log for details
    echo.
    echo 🔄 Rollback options:
    echo   1. Run 'python deploy.py rollback'
    echo   2. Check previous deployment
    echo   3. Fix issues and retry
) else (
    echo.
    echo ✅ Deployment pipeline completed successfully!
    echo 🌍 Website deployed to Cloudflare Pages
    echo 📊 Quality gates passed
    echo 🔒 Security scan completed
)

echo.
echo 📋 Available Commands:
echo   • deploy: Full deployment pipeline
echo   • quality-gates: Run quality gates only
echo   • validate: Validate current deployment
echo   • rollback: Rollback to previous version
echo.

pause