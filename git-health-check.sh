#!/bin/bash
# Verakore Workspace Health Check - Git Integration
# Runs on git operations to ensure workspace health

echo "🤖 Verakore Workspace Health Check"
echo "=================================="

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.x"
    exit 1
fi

# Check if automation script exists
if [ ! -f "automation.py" ]; then
    echo "❌ Automation script not found"
    exit 1
fi

# Run health check
echo "🔍 Running workspace health check..."
python automation.py check

# Check result
if [ $? -eq 0 ]; then
    echo "✅ Workspace is healthy"
    exit 0
else
    echo "⚠️ Workspace has issues"
    echo "📋 Check automation.log for details"
    exit 1
fi
