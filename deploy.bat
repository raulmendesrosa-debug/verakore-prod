@echo off
echo ========================================
echo    Verakore Website Deployment Helper
echo ========================================
echo.

echo Creating deployment package...
echo.

REM Create a temporary directory for deployment
if exist "deploy_temp" rmdir /s /q "deploy_temp"
mkdir "deploy_temp"

REM Copy all files to deployment directory
echo Copying website files...
xcopy /E /I /Y "assets" "deploy_temp\assets"
copy /Y "*.html" "deploy_temp\"
copy /Y "netlify.toml" "deploy_temp\"
copy /Y "DEPLOYMENT_GUIDE.md" "deploy_temp\"

echo.
echo Files copied successfully!
echo.

REM Create ZIP file
echo Creating ZIP file for Netlify deployment...
powershell -command "Compress-Archive -Path 'deploy_temp\*' -DestinationPath 'verakore-website-deploy.zip' -Force"

REM Clean up temporary directory
rmdir /s /q "deploy_temp"

echo.
echo ========================================
echo    DEPLOYMENT PACKAGE READY!
echo ========================================
echo.
echo File created: verakore-website-deploy.zip
echo.
echo Next steps:
echo 1. Go to https://netlify.com
echo 2. Sign up/Login to your account
echo 3. Drag verakore-website-deploy.zip to the deploy area
echo 4. Your site will be live in minutes!
echo.
echo For detailed instructions, see DEPLOYMENT_GUIDE.md
echo.
pause
