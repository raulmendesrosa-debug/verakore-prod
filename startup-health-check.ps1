# Verakore Workspace Startup Health Check - PowerShell
# Runs automatically when workspace is opened

param(
    [switch]$Force,
    [switch]$Silent
)

$ErrorActionPreference = "SilentlyContinue"

# Configuration
$ScriptPath = $PSScriptRoot
$AutomationScript = Join-Path $ScriptPath "automation.py"
$LogFile = Join-Path $ScriptPath "automation.log"
$LastRunFile = Join-Path $ScriptPath "last_run_$(Get-Date -Format 'yyyyMMdd').txt"

function Write-StartupLog {
    param([string]$Message, [string]$Level = "INFO")
    if (-not $Silent) {
        Write-Host $Message
    }
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "$Timestamp - STARTUP - $Message"
    Add-Content -Path $LogFile -Value $LogEntry -ErrorAction SilentlyContinue
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-StartupLog "Python found: $pythonVersion"
            return $true
        }
    }
    catch {
        Write-StartupLog "Python not found: $($_.Exception.Message)" "ERROR"
        return $false
    }
    return $false
}

function Test-AutomationScript {
    if (Test-Path $AutomationScript) {
        Write-StartupLog "Automation script found"
        return $true
    } else {
        Write-StartupLog "Automation script not found: $AutomationScript" "ERROR"
        return $false
    }
}

function Start-HealthCheck {
    Write-StartupLog "Starting Verakore workspace health check..."
    
    try {
        $Process = Start-Process -FilePath "python.exe" -ArgumentList "automation.py check" -WorkingDirectory $ScriptPath -Wait -PassThru -NoNewWindow -RedirectStandardOutput "temp_output.txt" -RedirectStandardError "temp_error.txt"
        
        if ($Process.ExitCode -eq 0) {
            Write-StartupLog "Health check completed successfully"
            $Success = $true
        } else {
            Write-StartupLog "Health check completed with issues (Exit Code: $($Process.ExitCode))" "WARN"
            $Success = $false
        }
        
        # Clean up temp files
        Remove-Item "temp_output.txt" -ErrorAction SilentlyContinue
        Remove-Item "temp_error.txt" -ErrorAction SilentlyContinue
        
        return $Success
    }
    catch {
        Write-StartupLog "Failed to run health check: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Main execution
if (-not $Silent) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "🤖 Verakore Workspace Health Check" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

# Check if already run today
if (-not $Force -and (Test-Path $LastRunFile)) {
    Write-StartupLog "Health check already run today"
    if (-not $Silent) {
        Write-Host "ℹ️ Health check already run today" -ForegroundColor Yellow
        Write-Host "💡 Run 'python automation.py check' for manual check" -ForegroundColor Gray
    }
    exit 0
}

# Prerequisites check
$PrerequisitesOK = $true

if (-not (Test-PythonInstallation)) {
    Write-StartupLog "Python installation required" "ERROR"
    $PrerequisitesOK = $false
}

if (-not (Test-AutomationScript)) {
    Write-StartupLog "Automation script required" "ERROR"
    $PrerequisitesOK = $false
}

if (-not $PrerequisitesOK) {
    if (-not $Silent) {
        Write-Host "❌ Prerequisites not met" -ForegroundColor Red
        Write-Host "💡 Run 'setup-automation.bat' to set up the environment" -ForegroundColor Yellow
    }
    exit 1
}

# Run health check
$HealthCheckSuccess = Start-HealthCheck

# Mark as run today
Set-Content -Path $LastRunFile -Value "$(Get-Date)"

# Results
if ($HealthCheckSuccess) {
    Write-StartupLog "Workspace is healthy and ready"
    if (-not $Silent) {
        Write-Host "✅ Workspace is healthy and ready!" -ForegroundColor Green
    }
    exit 0
} else {
    Write-StartupLog "Workspace has issues that should be addressed" "WARN"
    if (-not $Silent) {
        Write-Host "⚠️ Workspace has issues that should be addressed" -ForegroundColor Yellow
        Write-Host "📋 Check automation.log for details" -ForegroundColor Gray
    }
    exit 1
}
