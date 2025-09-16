@echo off
REM Verakore Security Scanner Setup
REM Sets up comprehensive security scanning and vulnerability assessment

echo 🔒 Verakore Security Scanner Setup
echo ==================================

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
if not exist "security_data" mkdir security_data
if not exist "reports" mkdir reports
echo ✅ Directories created

REM Test the security scanning system
echo 🧪 Testing security scanning system...
python security.py setup
if errorlevel 1 (
    echo ❌ Security scanning test failed
    echo 📋 Check security.log for details
) else (
    echo ✅ Security scanning system working correctly
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📋 What You Get:
echo • Security header validation
echo • SSL/TLS security checks
echo • Vulnerability scanning (XSS, SQL injection, etc.)
echo • OWASP Top 10 compliance checking
echo • Security score calculation
echo • Real-time security alerts
echo • Comprehensive security reporting
echo.
echo 📋 Next Steps:
echo 1. Configure target URLs in security_config.json
echo 2. Set up security thresholds
echo 3. Run 'security.bat check' for initial scan
echo 4. Start continuous monitoring with 'security.bat scan'
echo.
echo 📚 Files Created:
echo • security.py: Main security scanner
echo • security_config.json: Configuration file
echo • security-dashboard.html: Web dashboard
echo • security.bat: Windows integration
echo • security.db: SQLite database for scans
echo • security.log: Security scan logs
echo.
pause
