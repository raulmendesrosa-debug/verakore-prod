# Verakore Deployment Control Script (PowerShell)
# Implements the Deployment Control Framework

# Configuration
$REPO_NAME = "verakore-website"
$GITHUB_REPO = "raulmendesrosa-debug/verakore-website"
$CLOUDFLARE_PROJECT = "verakore-website"
$DOMAIN = "verakore.com"

# Status tracking
$DEPLOYMENT_LOG = "deployment.log"
$STATUS_FILE = "deployment_status.json"

# Colors for output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Initialize status file
function Initialize-Status {
    $status = @{
        deployment_id = Get-Date -Format "yyyyMMdd_HHmmss"
        phases = @{
            development = @{
                mobile_fixes = "completed"
                scroll_behavior = "completed"
                testing = "completed"
            }
            version_control = @{
                git_commit = "completed"
                github_push = "completed"
            }
            cloud_deployment = @{
                cloudflare_setup = "in_progress"
                domain_config = "pending"
                ssl_certificate = "pending"
            }
        }
        last_updated = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss")
        overall_status = "in_progress"
    }
    
    $status | ConvertTo-Json -Depth 3 | Out-File -FilePath $STATUS_FILE -Encoding UTF8
    Write-ColorOutput "Deployment tracking initialized" "Green"
}

# Log function
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logEntry = "[$timestamp] $Message"
    Write-Host $logEntry
    $logEntry | Out-File -FilePath $DEPLOYMENT_LOG -Append -Encoding UTF8
}

# Status check function
function Show-Status {
    Write-ColorOutput "=== DEPLOYMENT STATUS ===" "Blue"
    
    if (Test-Path $STATUS_FILE) {
        $status = Get-Content $STATUS_FILE | ConvertFrom-Json
        Write-Host "Deployment ID: $($status.deployment_id)"
        Write-Host "Last Updated: $($status.last_updated)"
        Write-Host "Overall Status: $($status.overall_status)"
        Write-Host ""
        
        Write-ColorOutput "Phase Status:" "Yellow"
        foreach ($phase in $status.phases.PSObject.Properties) {
            Write-Host "$($phase.Name):"
            foreach ($component in $phase.Value.PSObject.Properties) {
                Write-Host "  $($component.Name): $($component.Value)"
            }
        }
    } else {
        Write-ColorOutput "No status file found. Run 'Initialize-Status' first." "Red"
    }
}

# Git status check
function Show-GitStatus {
    Write-ColorOutput "=== GIT STATUS ===" "Blue"
    
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-ColorOutput "Uncommitted changes:" "Yellow"
        git status --short
    } else {
        Write-ColorOutput "Working directory clean" "Green"
    }
    
    Write-Host ""
    Write-ColorOutput "Recent commits:" "Yellow"
    git log --oneline -5
    
    Write-Host ""
    Write-ColorOutput "Remote status:" "Yellow"
    git status -uno
}

# Cloudflare status check
function Show-CloudflareStatus {
    Write-ColorOutput "=== CLOUDFLARE STATUS ===" "Blue"
    
    # Check if wrangler is installed
    try {
        $wranglerVersion = wrangler --version 2>$null
        if ($wranglerVersion) {
            Write-ColorOutput "Wrangler CLI available: $wranglerVersion" "Green"
            
            # Check if logged in
            try {
                $whoami = wrangler whoami 2>$null
                if ($whoami) {
                    Write-ColorOutput "Logged into Cloudflare" "Green"
                    
                    # Check project status
                    $projects = wrangler pages project list 2>$null
                    if ($projects -match $CLOUDFLARE_PROJECT) {
                        Write-ColorOutput "Project '$CLOUDFLARE_PROJECT' exists" "Green"
                        
                        # Get deployment status
                        Write-ColorOutput "Recent deployments:" "Yellow"
                        wrangler pages deployment list --project-name="$CLOUDFLARE_PROJECT" 2>$null | Select-Object -First 5
                    } else {
                        Write-ColorOutput "Project '$CLOUDFLARE_PROJECT' not found" "Yellow"
                    }
                } else {
                    Write-ColorOutput "Not logged into Cloudflare" "Red"
                }
            } catch {
                Write-ColorOutput "Not logged into Cloudflare" "Red"
            }
        } else {
            Write-ColorOutput "Wrangler CLI not installed" "Yellow"
            Write-Host "Install with: npm install -g wrangler"
        }
    } catch {
        Write-ColorOutput "Wrangler CLI not installed" "Yellow"
        Write-Host "Install with: npm install -g wrangler"
    }
}

# Health check
function Test-SiteHealth {
    Write-ColorOutput "=== SITE HEALTH CHECK ===" "Blue"
    
    # Check if site is accessible
    try {
        $response = Invoke-WebRequest -Uri "https://$CLOUDFLARE_PROJECT.pages.dev" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "Site accessible via Cloudflare Pages" "Green"
        } else {
            Write-ColorOutput "Site returned status: $($response.StatusCode)" "Yellow"
        }
    } catch {
        Write-ColorOutput "Site not accessible: $($_.Exception.Message)" "Red"
    }
    
    # Check custom domain if configured
    try {
        $response = Invoke-WebRequest -Uri "https://$DOMAIN" -UseBasicParsing -TimeoutSec 10
        if ($response.StatusCode -eq 200) {
            Write-ColorOutput "Custom domain accessible" "Green"
        } else {
            Write-ColorOutput "Custom domain returned status: $($response.StatusCode)" "Yellow"
        }
    } catch {
        Write-ColorOutput "Custom domain not configured or not accessible: $($_.Exception.Message)" "Yellow"
    }
}

# Deploy function
function Start-Deployment {
    Write-ColorOutput "=== STARTING DEPLOYMENT ===" "Blue"
    
    Write-Log "Starting deployment process"
    
    # Check prerequisites
    Write-ColorOutput "Checking prerequisites..." "Yellow"
    
    # Check git status
    $gitStatus = git status --porcelain
    if ($gitStatus) {
        Write-ColorOutput "Uncommitted changes detected. Please commit first." "Red"
        return
    }
    
    # Check if we're on main branch
    $currentBranch = git branch --show-current
    if ($currentBranch -ne "main") {
        Write-ColorOutput "Not on main branch. Current: $currentBranch" "Red"
        return
    }
    
    Write-ColorOutput "Prerequisites check passed" "Green"
    
    # Push to GitHub
    Write-ColorOutput "Pushing to GitHub..." "Yellow"
    $pushResult = git push origin main 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "Successfully pushed to GitHub" "Green"
    } else {
        Write-ColorOutput "Failed to push to GitHub: $pushResult" "Red"
        return
    }
    
    # Deploy to Cloudflare
    Write-ColorOutput "Deploying to Cloudflare..." "Yellow"
    try {
        $wranglerVersion = wrangler --version 2>$null
        if ($wranglerVersion) {
            $deployResult = wrangler pages deploy . --project-name="$CLOUDFLARE_PROJECT" 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "Successfully deployed to Cloudflare" "Green"
            } else {
                Write-ColorOutput "Failed to deploy to Cloudflare: $deployResult" "Red"
                return
            }
        } else {
            Write-ColorOutput "Wrangler not available. Manual deployment required." "Yellow"
            Write-Host "Go to: https://pages.cloudflare.com"
            Write-Host "Connect repository: $GITHUB_REPO"
        }
    } catch {
        Write-ColorOutput "Wrangler deployment failed: $($_.Exception.Message)" "Red"
    }
    
    Write-Log "Deployment completed"
    Write-ColorOutput "Deployment process finished" "Green"
}

# Rollback function
function Start-Rollback {
    Write-ColorOutput "=== ROLLBACK PROCEDURE ===" "Blue"
    
    Write-ColorOutput "Available commits for rollback:" "Yellow"
    git log --oneline -10
    
    Write-Host ""
    $commitHash = Read-Host "Enter commit hash to rollback to"
    
    $checkoutResult = git checkout $commitHash 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-ColorOutput "Rolled back to commit: $commitHash" "Green"
        
        # Force push to GitHub
        $pushResult = git push origin main --force 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "Rollback pushed to GitHub" "Green"
            Write-ColorOutput "Cloudflare will auto-deploy the rollback" "Yellow"
        } else {
            Write-ColorOutput "Failed to push rollback: $pushResult" "Red"
        }
    } else {
        Write-ColorOutput "Failed to rollback: $checkoutResult" "Red"
    }
}

# Main menu
function Show-Menu {
    Write-ColorOutput "=== VERAKORE DEPLOYMENT CONTROL ===" "Blue"
    Write-Host "1. Initialize deployment tracking"
    Write-Host "2. Check overall status"
    Write-Host "3. Check git status"
    Write-Host "4. Check Cloudflare status"
    Write-Host "5. Run health check"
    Write-Host "6. Deploy to production"
    Write-Host "7. Rollback deployment"
    Write-Host "8. View deployment log"
    Write-Host "9. Exit"
    Write-Host ""
}

# Main execution
param(
    [string]$Action = "menu"
)

switch ($Action.ToLower()) {
    "init" {
        Initialize-Status
    }
    "status" {
        Show-Status
    }
    "git-status" {
        Show-GitStatus
    }
    "cloudflare-status" {
        Show-CloudflareStatus
    }
    "health-check" {
        Test-SiteHealth
    }
    "deploy" {
        Start-Deployment
    }
    "rollback" {
        Start-Rollback
    }
    "log" {
        if (Test-Path $DEPLOYMENT_LOG) {
            Get-Content $DEPLOYMENT_LOG | Select-Object -Last 20
        } else {
            Write-Host "No deployment log found"
        }
    }
    "menu" {
        while ($true) {
            Show-Menu
            $choice = Read-Host "Select option (1-9)"
            
            switch ($choice) {
                "1" { Initialize-Status }
                "2" { Show-Status }
                "3" { Show-GitStatus }
                "4" { Show-CloudflareStatus }
                "5" { Test-SiteHealth }
                "6" { Start-Deployment }
                "7" { Start-Rollback }
                "8" { 
                    if (Test-Path $DEPLOYMENT_LOG) {
                        Get-Content $DEPLOYMENT_LOG | Select-Object -Last 20
                    } else {
                        Write-Host "No log found"
                    }
                }
                "9" { Write-Host "Goodbye!"; exit 0 }
                default { Write-ColorOutput "Invalid option" "Red" }
            }
            Write-Host ""
            Read-Host "Press Enter to continue"
        }
    }
    default {
        Write-ColorOutput "Unknown action: $Action" "Red"
        Write-Host "Available actions: init, status, git-status, cloudflare-status, health-check, deploy, rollback, log, menu"
    }
}
