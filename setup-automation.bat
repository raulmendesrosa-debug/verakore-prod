@echo off
REM Verakore Automation Setup Script
REM Sets up the complete automation environment

echo 🤖 Verakore Automation System Setup
echo ====================================

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.x first.
    echo 💡 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found

REM Install required Python packages
echo 📦 Installing required packages...
pip install schedule >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Warning: Could not install 'schedule' package
    echo 💡 You can install it manually: pip install schedule
) else (
    echo ✅ Required packages installed
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "backups" mkdir backups
if not exist "logs" mkdir logs
echo ✅ Directories created

REM Set up git pre-commit hook
echo 🔗 Setting up git pre-commit hook...
if exist ".git\hooks\pre-commit" (
    echo ℹ️ Pre-commit hook already exists
) else (
    copy pre-commit-hook.sh .git\hooks\pre-commit >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ Warning: Could not set up pre-commit hook
    ) else (
        echo ✅ Pre-commit hook installed
    )
)

REM Test the automation system
echo 🧪 Testing automation system...
python automation.py check
if errorlevel 1 (
    echo ❌ Automation test failed
    echo 📋 Check automation.log for details
) else (
    echo ✅ Automation system working correctly
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📋 Next Steps:
echo 1. Run 'automation.ps1 -Install' to set up scheduled tasks
echo 2. Run 'automation.ps1 -Status' to check task status
echo 3. Run 'python automation.py daily' for manual maintenance
echo.
echo 📚 Documentation: AUTOMATION_GUIDE.md
echo ⚙️ Configuration: automation_config.json
echo 📊 Logs: automation.log
echo.
pause
