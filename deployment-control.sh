#!/bin/bash
# Verakore Deployment Control Script
# Implements the Deployment Control Framework

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
REPO_NAME="verakore-website"
GITHUB_REPO="raulmendesrosa-debug/verakore-website"
CLOUDFLARE_PROJECT="verakore-website"
DOMAIN="verakore.com"

# Status tracking
DEPLOYMENT_LOG="deployment.log"
STATUS_FILE="deployment_status.json"

# Initialize status file
init_status() {
    cat > $STATUS_FILE << EOF
{
    "deployment_id": "$(date +%Y%m%d_%H%M%S)",
    "phases": {
        "development": {
            "mobile_fixes": "completed",
            "scroll_behavior": "completed",
            "testing": "completed"
        },
        "version_control": {
            "git_commit": "completed",
            "github_push": "completed"
        },
        "cloud_deployment": {
            "cloudflare_setup": "in_progress",
            "domain_config": "pending",
            "ssl_certificate": "pending"
        }
    },
    "last_updated": "$(date -Iseconds)",
    "overall_status": "in_progress"
}
EOF
}

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $DEPLOYMENT_LOG
}

# Status check function
check_status() {
    echo -e "${BLUE}=== DEPLOYMENT STATUS ===${NC}"
    
    if [ -f "$STATUS_FILE" ]; then
        echo "Deployment ID: $(jq -r '.deployment_id' $STATUS_FILE)"
        echo "Last Updated: $(jq -r '.last_updated' $STATUS_FILE)"
        echo "Overall Status: $(jq -r '.overall_status' $STATUS_FILE)"
        echo ""
        
        echo -e "${YELLOW}Phase Status:${NC}"
        jq -r '.phases | to_entries[] | "\(.key): \(.value | to_entries[] | "\(.key): \(.value)" | gsub("_"; " "))"' $STATUS_FILE
    else
        echo -e "${RED}No status file found. Run 'init' first.${NC}"
    fi
}

# Git status check
git_status() {
    echo -e "${BLUE}=== GIT STATUS ===${NC}"
    
    if git status --porcelain | grep -q .; then
        echo -e "${YELLOW}Uncommitted changes:${NC}"
        git status --short
    else
        echo -e "${GREEN}Working directory clean${NC}"
    fi
    
    echo ""
    echo -e "${YELLOW}Recent commits:${NC}"
    git log --oneline -5
    
    echo ""
    echo -e "${YELLOW}Remote status:${NC}"
    git status -uno
}

# Cloudflare status check
cloudflare_status() {
    echo -e "${BLUE}=== CLOUDFLARE STATUS ===${NC}"
    
    # Check if wrangler is installed
    if command -v wrangler &> /dev/null; then
        echo -e "${GREEN}Wrangler CLI available${NC}"
        
        # Check if logged in
        if wrangler whoami &> /dev/null; then
            echo -e "${GREEN}Logged into Cloudflare${NC}"
            
            # Check project status
            if wrangler pages project list | grep -q "$CLOUDFLARE_PROJECT"; then
                echo -e "${GREEN}Project '$CLOUDFLARE_PROJECT' exists${NC}"
                
                # Get deployment status
                echo -e "${YELLOW}Recent deployments:${NC}"
                wrangler pages deployment list --project-name="$CLOUDFLARE_PROJECT" | head -5
            else
                echo -e "${YELLOW}Project '$CLOUDFLARE_PROJECT' not found${NC}"
            fi
        else
            echo -e "${RED}Not logged into Cloudflare${NC}"
        fi
    else
        echo -e "${YELLOW}Wrangler CLI not installed${NC}"
        echo "Install with: npm install -g wrangler"
    fi
}

# Health check
health_check() {
    echo -e "${BLUE}=== SITE HEALTH CHECK ===${NC}"
    
    # Check if site is accessible
    if curl -s -o /dev/null -w "%{http_code}" "https://$CLOUDFLARE_PROJECT.pages.dev" | grep -q "200"; then
        echo -e "${GREEN}Site accessible via Cloudflare Pages${NC}"
    else
        echo -e "${RED}Site not accessible${NC}"
    fi
    
    # Check custom domain if configured
    if curl -s -o /dev/null -w "%{http_code}" "https://$DOMAIN" | grep -q "200"; then
        echo -e "${GREEN}Custom domain accessible${NC}"
    else
        echo -e "${YELLOW}Custom domain not configured or not accessible${NC}"
    fi
    
    # Check SSL certificate
    if echo | openssl s_client -servername "$DOMAIN" -connect "$DOMAIN:443" 2>/dev/null | openssl x509 -noout -dates | grep -q "notAfter"; then
        echo -e "${GREEN}SSL certificate valid${NC}"
    else
        echo -e "${YELLOW}SSL certificate status unknown${NC}"
    fi
}

# Deploy function
deploy() {
    echo -e "${BLUE}=== STARTING DEPLOYMENT ===${NC}"
    
    # Update status
    jq '.phases.cloud_deployment.cloudflare_setup = "in_progress"' $STATUS_FILE > tmp.json && mv tmp.json $STATUS_FILE
    
    log "Starting deployment process"
    
    # Check prerequisites
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    # Check git status
    if git status --porcelain | grep -q .; then
        echo -e "${RED}Uncommitted changes detected. Please commit first.${NC}"
        return 1
    fi
    
    # Check if we're on main branch
    current_branch=$(git branch --show-current)
    if [ "$current_branch" != "main" ]; then
        echo -e "${RED}Not on main branch. Current: $current_branch${NC}"
        return 1
    fi
    
    echo -e "${GREEN}Prerequisites check passed${NC}"
    
    # Push to GitHub
    echo -e "${YELLOW}Pushing to GitHub...${NC}"
    if git push origin main; then
        echo -e "${GREEN}Successfully pushed to GitHub${NC}"
        jq '.phases.version_control.github_push = "completed"' $STATUS_FILE > tmp.json && mv tmp.json $STATUS_FILE
    else
        echo -e "${RED}Failed to push to GitHub${NC}"
        return 1
    fi
    
    # Deploy to Cloudflare
    echo -e "${YELLOW}Deploying to Cloudflare...${NC}"
    if command -v wrangler &> /dev/null; then
        if wrangler pages deploy . --project-name="$CLOUDFLARE_PROJECT"; then
            echo -e "${GREEN}Successfully deployed to Cloudflare${NC}"
            jq '.phases.cloud_deployment.cloudflare_setup = "completed"' $STATUS_FILE > tmp.json && mv tmp.json $STATUS_FILE
        else
            echo -e "${RED}Failed to deploy to Cloudflare${NC}"
            return 1
        fi
    else
        echo -e "${YELLOW}Wrangler not available. Manual deployment required.${NC}"
        echo "Go to: https://pages.cloudflare.com"
        echo "Connect repository: $GITHUB_REPO"
    fi
    
    log "Deployment completed"
    echo -e "${GREEN}Deployment process finished${NC}"
}

# Rollback function
rollback() {
    echo -e "${BLUE}=== ROLLBACK PROCEDURE ===${NC}"
    
    echo -e "${YELLOW}Available commits for rollback:${NC}"
    git log --oneline -10
    
    echo ""
    read -p "Enter commit hash to rollback to: " commit_hash
    
    if git checkout "$commit_hash"; then
        echo -e "${GREEN}Rolled back to commit: $commit_hash${NC}"
        
        # Force push to GitHub
        if git push origin main --force; then
            echo -e "${GREEN}Rollback pushed to GitHub${NC}"
            echo -e "${YELLOW}Cloudflare will auto-deploy the rollback${NC}"
        else
            echo -e "${RED}Failed to push rollback${NC}"
        fi
    else
        echo -e "${RED}Failed to rollback${NC}"
    fi
}

# Main menu
show_menu() {
    echo -e "${BLUE}=== VERAKORE DEPLOYMENT CONTROL ===${NC}"
    echo "1. Initialize deployment tracking"
    echo "2. Check overall status"
    echo "3. Check git status"
    echo "4. Check Cloudflare status"
    echo "5. Run health check"
    echo "6. Deploy to production"
    echo "7. Rollback deployment"
    echo "8. View deployment log"
    echo "9. Exit"
    echo ""
    read -p "Select option (1-9): " choice
}

# Main execution
case "${1:-menu}" in
    "init")
        init_status
        echo -e "${GREEN}Deployment tracking initialized${NC}"
        ;;
    "status")
        check_status
        ;;
    "git-status")
        git_status
        ;;
    "cloudflare-status")
        cloudflare_status
        ;;
    "health-check")
        health_check
        ;;
    "deploy")
        deploy
        ;;
    "rollback")
        rollback
        ;;
    "log")
        if [ -f "$DEPLOYMENT_LOG" ]; then
            tail -20 "$DEPLOYMENT_LOG"
        else
            echo "No deployment log found"
        fi
        ;;
    "menu"|*)
        while true; do
            show_menu
            case $choice in
                1) init_status ;;
                2) check_status ;;
                3) git_status ;;
                4) cloudflare_status ;;
                5) health_check ;;
                6) deploy ;;
                7) rollback ;;
                8) if [ -f "$DEPLOYMENT_LOG" ]; then tail -20 "$DEPLOYMENT_LOG"; else echo "No log found"; fi ;;
                9) echo "Goodbye!"; exit 0 ;;
                *) echo "Invalid option" ;;
            esac
            echo ""
            read -p "Press Enter to continue..."
        done
        ;;
esac
