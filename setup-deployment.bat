@echo off
REM Verakore Deployment Pipeline Setup
REM Sets up automated deployment with GitHub Actions and Cloudflare Pages

echo 🚀 Verakore Deployment Pipeline Setup
echo =====================================

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
if not exist ".github\workflows" mkdir .github\workflows
if not exist "deploy" mkdir deploy
if not exist "backups" mkdir backups
echo ✅ Directories created

REM Check for Cloudflare Wrangler CLI
echo 🔍 Checking Cloudflare Wrangler CLI...
wrangler --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Cloudflare Wrangler CLI not found
    echo 💡 Install with: npm install -g wrangler
    echo 💡 Or download from: https://developers.cloudflare.com/workers/wrangler/
) else (
    echo ✅ Cloudflare Wrangler CLI found
)

REM Test the deployment system
echo 🧪 Testing deployment system...
python deploy.py quality-gates
if errorlevel 1 (
    echo ❌ Deployment test failed
    echo 📋 Check deployment.log for details
) else (
    echo ✅ Deployment system working correctly
)

echo.
echo 🎉 Setup Complete!
echo.
echo 📋 Next Steps:
echo 1. Configure Cloudflare Pages:
echo    • Get API token from Cloudflare dashboard
echo    • Update deployment_config.json with your credentials
echo.
echo 2. Set up GitHub Actions:
echo    • Add CLOUDFLARE_API_TOKEN to GitHub secrets
echo    • Add CLOUDFLARE_ACCOUNT_ID to GitHub secrets
echo.
echo 3. Test deployment:
echo    • Run 'deploy.bat' for manual deployment
echo    • Push to main branch for automatic deployment
echo.
echo 📚 Documentation:
echo • GitHub Actions: .github/workflows/deploy.yml
echo • Configuration: deployment_config.json
echo • Deployment Log: deployment.log
echo.
pause
