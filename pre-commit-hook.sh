#!/bin/bash
# Pre-commit hook for character encoding validation

echo "🔍 Running character encoding quality control..."

# Run the encoding check
python3 check-encoding.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "✅ Character encoding validation passed!"
    exit 0
else
    echo "❌ Character encoding issues found!"
    echo "💡 Run 'python3 fix-encoding.py' to fix automatically"
    exit 1
fi
