@echo off
REM Verakore Backup & Recovery System Setup
REM Sets up comprehensive backup solution with disaster recovery

echo 💾 Verakore Backup & Recovery System Setup
echo ==========================================

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
pip install requests >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Warning: Could not install 'requests' package
    echo 💡 You can install it manually: pip install requests
) else (
    echo ✅ Required packages installed
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "backups" mkdir backups
if not exist "backups\full" mkdir backups\full
if not exist "backups\incremental" mkdir backups\incremental
if not exist "backups\differential" mkdir backups\differential
if not exist "backups\verification" mkdir backups\verification
echo ✅ Directories created

REM Test the backup system
echo 🧪 Testing backup system...
python backup.py setup
if errorlevel 1 (
    echo ❌ Backup system test failed
    echo 📋 Check backup.log for details
) else (
    echo ✅ Backup system working correctly
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📋 What You Get:
echo • Full, incremental, and differential backups
echo • Automated backup scheduling
echo • Backup verification and integrity checks
echo • Disaster recovery capabilities
echo • Backup compression and optimization
echo • Recovery time and point objectives
echo • Comprehensive backup reporting
echo.
echo 📋 Next Steps:
echo 1. Configure backup sources in backup_config.json
echo 2. Set up backup retention policies
echo 3. Run 'backup.bat full' for initial backup
echo 4. Start backup service with 'backup.bat service'
echo.
echo 📚 Files Created:
echo • backup.py: Main backup system
echo • backup_config.json: Configuration file
echo • backup-dashboard.html: Web dashboard
echo • backup.bat: Windows integration
echo • backup.db: SQLite database for tracking
echo • backup.log: Backup operation logs
echo.
pause
