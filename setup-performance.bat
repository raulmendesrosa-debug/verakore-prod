@echo off
REM Verakore Performance Monitoring Setup
REM Sets up comprehensive performance monitoring with Core Web Vitals tracking

echo 📊 Verakore Performance Monitoring Setup
echo =========================================

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
pip install requests sqlite3 >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Warning: Could not install some packages
    echo 💡 You can install them manually: pip install requests
) else (
    echo ✅ Required packages installed
)

REM Check for Node.js and Lighthouse CLI
echo 🔍 Checking Node.js and Lighthouse CLI...
node --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Node.js not found
    echo 💡 Install from: https://nodejs.org/
    echo 💡 Then run: npm install -g lighthouse
) else (
    echo ✅ Node.js found
    lighthouse --version >nul 2>&1
    if errorlevel 1 (
        echo ⚠️ Lighthouse CLI not found
        echo 💡 Install with: npm install -g lighthouse
    ) else (
        echo ✅ Lighthouse CLI found
    )
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist "performance_data" mkdir performance_data
if not exist "reports" mkdir reports
echo ✅ Directories created

REM Test the performance monitoring system
echo 🧪 Testing performance monitoring system...
python performance.py setup
if errorlevel 1 (
    echo ❌ Performance monitoring test failed
    echo 📋 Check performance.log for details
) else (
    echo ✅ Performance monitoring system working correctly
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📋 What You Get:
echo • Core Web Vitals monitoring (LCP, FID, CLS)
echo • Performance score tracking
echo • Accessibility and SEO monitoring
echo • Optimization recommendations
echo • Performance budget tracking
echo • Real-time alerts and notifications
echo.
echo 📋 Next Steps:
echo 1. Configure target URLs in performance_config.json
echo 2. Set up performance thresholds
echo 3. Run 'performance.bat check' for initial analysis
echo 4. Start continuous monitoring with 'performance.bat monitor'
echo.
echo 📚 Files Created:
echo • performance.py: Main monitoring script
echo • performance_config.json: Configuration file
echo • performance-dashboard.html: Web dashboard
echo • performance.bat: Windows integration
echo • performance.db: SQLite database for metrics
echo • performance.log: Monitoring logs
echo.
pause
