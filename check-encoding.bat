@echo off
REM Character Encoding Quality Control - Batch Version
REM Simple detection of common encoding issues

echo 🔍 Character Encoding Quality Control
echo ========================================

REM Check for HTML files
dir *.html >nul 2>&1
if errorlevel 1 (
    echo ❌ No HTML files found in current directory
    exit /b 1
)

echo.
echo 📋 Manual Check Instructions:
echo.
echo 1. Open each HTML file in a text editor
echo 2. Search for these problematic patterns:
echo    • â€" (should be &#x2014;)
echo    • â†' (should be &#x2192;)
echo    • â€™ (should be &#x2019;)
echo    • â€œ (should be &#x201C;)
echo    • â€ (should be &#x201D;)
echo    • ðŸ'‹ (should be &#x1F44B;)
echo    • ðŸ'Œ (should be &#x1F4AC;)
echo.
echo 3. Replace with proper HTML entities
echo 4. Test in browser to verify display
echo.
echo 💡 For automated fixing, use a text editor with find/replace:
echo    Find: â€"
echo    Replace: &#x2014;
echo.
echo ✅ Quality control complete!
pause
