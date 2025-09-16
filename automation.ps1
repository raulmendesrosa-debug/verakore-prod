# Verakore Workspace Automation - PowerShell Integration
# Advanced automation with Windows Task Scheduler integration

param(
    [string]$Command = "check",
    [switch]$Install,
    [switch]$Uninstall,
    [switch]$Status
)

$ErrorActionPreference = "Stop"

# Configuration
$ScriptPath = $PSScriptRoot
$AutomationScript = Join-Path $ScriptPath "automation.py"
$LogFile = Join-Path $ScriptPath "automation.log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $Timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $LogEntry = "$Timestamp - $Level - $Message"
    Write-Host $LogEntry
    Add-Content -Path $LogFile -Value $LogEntry
}

function Test-PythonInstallation {
    try {
        $pythonVersion = python --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Python found: $pythonVersion" "INFO"
            return $true
        }
    }
    catch {
        Write-Log "Python not found: $($_.Exception.Message)" "ERROR"
        return $false
    }
    return $false
}

function Install-TaskSchedulerTasks {
    Write-Log "Installing Windows Task Scheduler tasks..." "INFO"
    
    # Daily maintenance task (9:00 AM)
    $DailyTask = @{
        TaskName = "VerakoreDailyMaintenance"
        Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automation.py daily" -WorkingDirectory $ScriptPath
        Trigger = New-ScheduledTaskTrigger -Daily -At "09:00"
        Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType InteractiveToken
    }
    
    try {
        Register-ScheduledTask @DailyTask -Force
        Write-Log "✅ Daily maintenance task installed" "INFO"
    }
    catch {
        Write-Log "❌ Failed to install daily task: $($_.Exception.Message)" "ERROR"
    }
    
    # Weekly maintenance task (Monday 9:00 AM)
    $WeeklyTask = @{
        TaskName = "VerakoreWeeklyMaintenance"
        Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automation.py weekly" -WorkingDirectory $ScriptPath
        Trigger = New-ScheduledTaskTrigger -Weekly -DaysOfWeek Monday -At "09:00"
        Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType InteractiveToken
    }
    
    try {
        Register-ScheduledTask @WeeklyTask -Force
        Write-Log "✅ Weekly maintenance task installed" "INFO"
    }
    catch {
        Write-Log "❌ Failed to install weekly task: $($_.Exception.Message)" "ERROR"
    }
    
    # Deployment readiness check (5:00 PM daily)
    $DeployTask = @{
        TaskName = "VerakoreDeployCheck"
        Action = New-ScheduledTaskAction -Execute "python.exe" -Argument "automation.py deploy-check" -WorkingDirectory $ScriptPath
        Trigger = New-ScheduledTaskTrigger -Daily -At "17:00"
        Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
        Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType InteractiveToken
    }
    
    try {
        Register-ScheduledTask @DeployTask -Force
        Write-Log "✅ Deployment check task installed" "INFO"
    }
    catch {
        Write-Log "❌ Failed to install deployment task: $($_.Exception.Message)" "ERROR"
    }
}

function Uninstall-TaskSchedulerTasks {
    Write-Log "Uninstalling Windows Task Scheduler tasks..." "INFO"
    
    $Tasks = @("VerakoreDailyMaintenance", "VerakoreWeeklyMaintenance", "VerakoreDeployCheck")
    
    foreach ($TaskName in $Tasks) {
        try {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
            Write-Log "✅ Removed task: $TaskName" "INFO"
        }
        catch {
            Write-Log "ℹ️ Task not found: $TaskName" "INFO"
        }
    }
}

function Get-TaskStatus {
    Write-Log "Checking task status..." "INFO"
    
    $Tasks = @("VerakoreDailyMaintenance", "VerakoreWeeklyMaintenance", "VerakoreDeployCheck")
    
    foreach ($TaskName in $Tasks) {
        try {
            $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
            if ($Task) {
                $State = $Task.State
                $LastRun = (Get-ScheduledTaskInfo -TaskName $TaskName).LastRunTime
                Write-Log "📋 $TaskName - State: $State, Last Run: $LastRun" "INFO"
            } else {
                Write-Log "❌ Task not found: $TaskName" "WARN"
            }
        }
        catch {
            Write-Log "❌ Error checking task $TaskName : $($_.Exception.Message)" "ERROR"
        }
    }
}

function Start-Automation {
    param([string]$Command)
    
    Write-Log "🤖 Starting Verakore Automation System" "INFO"
    Write-Log "📁 Workspace: $ScriptPath" "INFO"
    Write-Log "🔧 Command: $Command" "INFO"
    
    if (-not (Test-PythonInstallation)) {
        Write-Log "❌ Python installation required" "ERROR"
        return $false
    }
    
    if (-not (Test-Path $AutomationScript)) {
        Write-Log "❌ Automation script not found: $AutomationScript" "ERROR"
        return $false
    }
    
    try {
        $Process = Start-Process -FilePath "python.exe" -ArgumentList "automation.py $Command" -WorkingDirectory $ScriptPath -Wait -PassThru -NoNewWindow
        
        if ($Process.ExitCode -eq 0) {
            Write-Log "✅ Automation completed successfully" "INFO"
            return $true
        } else {
            Write-Log "❌ Automation completed with errors (Exit Code: $($Process.ExitCode))" "ERROR"
            return $false
        }
    }
    catch {
        Write-Log "❌ Failed to run automation: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# Main execution
Write-Host "🤖 Verakore Workspace Automation System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if ($Install) {
    Install-TaskSchedulerTasks
    Write-Host "✅ Task Scheduler integration installed!" -ForegroundColor Green
    Write-Host "💡 Tasks will run automatically:" -ForegroundColor Yellow
    Write-Host "   • Daily maintenance: 9:00 AM" -ForegroundColor White
    Write-Host "   • Weekly maintenance: Monday 9:00 AM" -ForegroundColor White
    Write-Host "   • Deployment check: 5:00 PM daily" -ForegroundColor White
}
elseif ($Uninstall) {
    Uninstall-TaskSchedulerTasks
    Write-Host "✅ Task Scheduler integration removed!" -ForegroundColor Green
}
elseif ($Status) {
    Get-TaskStatus
}
else {
    $Success = Start-Automation -Command $Command
    
    if ($Success) {
        Write-Host "✅ Automation completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Automation completed with errors" -ForegroundColor Red
        Write-Host "📋 Check automation.log for details" -ForegroundColor Yellow
    }
}

Write-Host "`nPress any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
