#!/usr/bin/env python3
"""
Verakore Workspace Automation System
A comprehensive cron-like system for maintaining workspace consistency
"""

import os
import sys
import time
import subprocess
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
import schedule
import threading

class VerakoreAutomation:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.log_file = self.workspace_root / "automation.log"
        self.config_file = self.workspace_root / "automation_config.json"
        self.setup_logging()
        self.load_config()
        
    def setup_logging(self):
        """Setup logging for automation system"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self):
        """Load automation configuration"""
        default_config = {
            "character_encoding": {
                "enabled": True,
                "frequency": "daily",
                "auto_fix": True
            },
            "git_operations": {
                "enabled": True,
                "auto_commit": False,
                "commit_message_template": "Automated maintenance: {task}"
            },
            "deployment": {
                "enabled": True,
                "frequency": "manual",
                "auto_deploy": False
            },
            "quality_checks": {
                "enabled": True,
                "frequency": "daily",
                "checks": ["encoding", "mobile", "links", "performance"]
            },
            "backup": {
                "enabled": True,
                "frequency": "weekly",
                "retention_days": 30
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save automation configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def run_command(self, command, description=""):
        """Run a command and log results"""
        try:
            self.logger.info(f"Running: {description or command}")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.logger.info(f"✅ Success: {description or command}")
                if result.stdout:
                    self.logger.info(f"Output: {result.stdout.strip()}")
            else:
                self.logger.error(f"❌ Failed: {description or command}")
                if result.stderr:
                    self.logger.error(f"Error: {result.stderr.strip()}")
                    
            return result.returncode == 0
        except Exception as e:
            self.logger.error(f"Exception running {command}: {e}")
            return False
            
    def character_encoding_check(self):
        """Run character encoding quality control"""
        if not self.config["character_encoding"]["enabled"]:
            return True
            
        self.logger.info("🔍 Running character encoding check...")
        
        # Check for encoding issues
        success = self.run_command("python check-encoding.py", "Character encoding check")
        
        if not success and self.config["character_encoding"]["auto_fix"]:
            self.logger.info("🔧 Auto-fixing character encoding issues...")
            self.run_command("python fix-encoding.py", "Character encoding fix")
            
        return success
        
    def git_health_check(self):
        """Check git repository health"""
        if not self.config["git_operations"]["enabled"]:
            return True
            
        self.logger.info("📁 Checking git repository health...")
        
        # Check git status
        self.run_command("git status --porcelain", "Git status check")
        
        # Check for uncommitted changes
        result = subprocess.run("git diff --quiet", shell=True)
        if result.returncode != 0:
            self.logger.warning("⚠️ Uncommitted changes detected")
            
        return True
        
    def mobile_responsiveness_check(self):
        """Check mobile responsiveness"""
        if not self.config["quality_checks"]["enabled"]:
            return True
            
        self.logger.info("📱 Checking mobile responsiveness...")
        
        # Check for mobile CSS issues
        html_files = list(self.workspace_root.glob("*.html"))
        mobile_issues = []
        
        for html_file in html_files:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for mobile CSS
            if "@media" not in content:
                mobile_issues.append(f"Missing mobile CSS in {html_file.name}")
                
        if mobile_issues:
            self.logger.warning(f"⚠️ Mobile issues found: {mobile_issues}")
        else:
            self.logger.info("✅ Mobile responsiveness looks good")
            
        return len(mobile_issues) == 0
        
    def performance_check(self):
        """Basic performance checks"""
        if not self.config["quality_checks"]["enabled"]:
            return True
            
        self.logger.info("⚡ Running performance checks...")
        
        # Check file sizes
        large_files = []
        for file_path in self.workspace_root.rglob("*"):
            if file_path.is_file() and file_path.stat().st_size > 1024 * 1024:  # 1MB
                large_files.append(f"{file_path.name} ({file_path.stat().st_size / 1024 / 1024:.1f}MB)")
                
        if large_files:
            self.logger.warning(f"⚠️ Large files detected: {large_files}")
        else:
            self.logger.info("✅ File sizes look good")
            
        return True
        
    def backup_workspace(self):
        """Create workspace backup"""
        if not self.config["backup"]["enabled"]:
            return True
            
        self.logger.info("💾 Creating workspace backup...")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"verakore_backup_{timestamp}"
        
        # Create backup directory
        backup_dir = self.workspace_root / "backups" / backup_name
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy important files
        important_files = [
            "*.html", "*.css", "*.js", "*.md", "*.json", "*.toml",
            "*.py", "*.bat", "*.ps1", "*.sh"
        ]
        
        for pattern in important_files:
            for file_path in self.workspace_root.glob(pattern):
                if file_path.is_file():
                    backup_file = backup_dir / file_path.name
                    backup_file.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
                    
        self.logger.info(f"✅ Backup created: {backup_dir}")
        
        # Clean old backups
        self.cleanup_old_backups()
        
        return True
        
    def cleanup_old_backups(self):
        """Remove old backups based on retention policy"""
        retention_days = self.config["backup"]["retention_days"]
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        backups_dir = self.workspace_root / "backups"
        if not backups_dir.exists():
            return
            
        for backup_dir in backups_dir.iterdir():
            if backup_dir.is_dir():
                backup_time = datetime.fromtimestamp(backup_dir.stat().st_mtime)
                if backup_time < cutoff_date:
                    self.logger.info(f"🗑️ Removing old backup: {backup_dir.name}")
                    import shutil
                    shutil.rmtree(backup_dir)
                    
    def deployment_readiness_check(self):
        """Check if workspace is ready for deployment"""
        if not self.config["deployment"]["enabled"]:
            return True
            
        self.logger.info("🚀 Checking deployment readiness...")
        
        checks = [
            ("Character encoding", self.character_encoding_check()),
            ("Mobile responsiveness", self.mobile_responsiveness_check()),
            ("Git health", self.git_health_check()),
            ("Performance", self.performance_check())
        ]
        
        all_passed = all(check[1] for check in checks)
        
        if all_passed:
            self.logger.info("✅ Workspace is ready for deployment!")
        else:
            self.logger.warning("⚠️ Workspace has issues that should be addressed before deployment")
            
        return all_passed
        
    def run_daily_maintenance(self):
        """Run daily maintenance tasks"""
        self.logger.info("🌅 Starting daily maintenance...")
        
        tasks = [
            ("Character encoding check", self.character_encoding_check),
            ("Mobile responsiveness check", self.mobile_responsiveness_check),
            ("Performance check", self.performance_check),
            ("Git health check", self.git_health_check)
        ]
        
        results = []
        for task_name, task_func in tasks:
            try:
                result = task_func()
                results.append((task_name, result))
            except Exception as e:
                self.logger.error(f"Error in {task_name}: {e}")
                results.append((task_name, False))
                
        # Summary
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        self.logger.info(f"📊 Daily maintenance complete: {passed}/{total} tasks passed")
        
        return passed == total
        
    def run_weekly_maintenance(self):
        """Run weekly maintenance tasks"""
        self.logger.info("📅 Starting weekly maintenance...")
        
        # Run daily maintenance first
        daily_result = self.run_daily_maintenance()
        
        # Additional weekly tasks
        weekly_tasks = [
            ("Workspace backup", self.backup_workspace),
            ("Deployment readiness check", self.deployment_readiness_check)
        ]
        
        for task_name, task_func in weekly_tasks:
            try:
                result = task_func()
                self.logger.info(f"{'✅' if result else '❌'} {task_name}")
            except Exception as e:
                self.logger.error(f"Error in {task_name}: {e}")
                
        return daily_result
        
    def start_scheduler(self):
        """Start the automation scheduler"""
        self.logger.info("🤖 Starting Verakore Automation System...")
        
        # Schedule daily maintenance
        schedule.every().day.at("09:00").do(self.run_daily_maintenance)
        
        # Schedule weekly maintenance
        schedule.every().monday.at("09:00").do(self.run_weekly_maintenance)
        
        # Schedule deployment readiness check
        schedule.every().day.at("17:00").do(self.deployment_readiness_check)
        
        self.logger.info("📅 Scheduler started. Press Ctrl+C to stop.")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            self.logger.info("🛑 Automation system stopped by user")
            
    def run_manual_check(self):
        """Run a manual check of all systems"""
        self.logger.info("🔧 Running manual system check...")
        
        return self.run_daily_maintenance()

def main():
    """Main function"""
    automation = VerakoreAutomation()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "daily":
            automation.run_daily_maintenance()
        elif command == "weekly":
            automation.run_weekly_maintenance()
        elif command == "check":
            automation.run_manual_check()
        elif command == "backup":
            automation.backup_workspace()
        elif command == "deploy-check":
            automation.deployment_readiness_check()
        elif command == "start":
            automation.start_scheduler()
        else:
            print("Usage: python automation.py [daily|weekly|check|backup|deploy-check|start]")
    else:
        # Default: run manual check
        automation.run_manual_check()

if __name__ == "__main__":
    main()
