#!/usr/bin/env python3
"""
Verakore Deployment Pipeline Controller
Manages automated deployment with quality gates and rollback capabilities
"""

import os
import sys
import json
import subprocess
import time
import requests
from datetime import datetime
from pathlib import Path

class DeploymentController:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "deployment_config.json"
        self.deployment_log = self.workspace_root / "deployment.log"
        self.load_config()
        
    def load_config(self):
        """Load deployment configuration"""
        default_config = {
            "cloudflare": {
                "account_id": "",
                "project_name": "verakore-website",
                "api_token": "",
                "pages_url": "https://verakore-website.pages.dev"
            },
            "github": {
                "repository": "raulmendesrosa-debug/verakore-website",
                "branch": "main"
            },
            "deployment": {
                "auto_deploy": False,
                "quality_gates": True,
                "rollback_enabled": True,
                "staging_enabled": False
            },
            "notifications": {
                "slack_webhook": "",
                "email": "",
                "enabled": True
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save deployment configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def log_deployment(self, message, level="INFO"):
        """Log deployment events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.deployment_log, 'a') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def run_quality_gates(self):
        """Run all quality gates before deployment"""
        self.log_deployment("Running quality gates...")
        
        gates = [
            ("Character encoding check", "python check-encoding.py"),
            ("Workspace health check", "python automation.py startup"),
            ("Comprehensive health check", "python automation.py check"),
            ("Deployment readiness", "python automation.py deploy-check")
        ]
        
        passed_gates = 0
        for gate_name, command in gates:
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                if result.returncode == 0:
                    self.log_deployment(f"[PASS] {gate_name} passed")
                    passed_gates += 1
                else:
                    self.log_deployment(f"[FAIL] {gate_name} failed: {result.stderr}", "ERROR")
            except Exception as e:
                self.log_deployment(f"[ERROR] {gate_name} error: {e}", "ERROR")
                
        if passed_gates == len(gates):
            self.log_deployment("[SUCCESS] All quality gates passed")
            return True
        else:
            self.log_deployment(f"[FAILED] {passed_gates}/{len(gates)} quality gates passed", "ERROR")
            return False
            
    def prepare_deployment(self):
        """Prepare files for deployment"""
        self.log_deployment("Preparing deployment files...")
        
        deploy_dir = self.workspace_root / "deploy"
        if deploy_dir.exists():
            import shutil
            shutil.rmtree(deploy_dir)
        deploy_dir.mkdir()
        
        # Copy essential files
        essential_files = [
            "*.html", "*.toml", "*.json", "*.md", "*.bat", "*.ps1", "*.py", "*.sh"
        ]
        
        for pattern in essential_files:
            for file_path in self.workspace_root.glob(pattern):
                if file_path.is_file():
                    deploy_file = deploy_dir / file_path.name
                    deploy_file.write_text(file_path.read_text(encoding='utf-8'), encoding='utf-8')
                    
        # Copy directories
        essential_dirs = ["assets", "tools"]
        for dir_name in essential_dirs:
            src_dir = self.workspace_root / dir_name
            if src_dir.exists():
                dst_dir = deploy_dir / dir_name
                import shutil
                shutil.copytree(src_dir, dst_dir)
                
        # Create deployment info
        deployment_info = {
            "timestamp": datetime.now().isoformat(),
            "version": "2.0.0",
            "environment": "production",
            "quality_gates_passed": True,
            "files_deployed": len(list(deploy_dir.rglob("*")))
        }
        
        info_file = deploy_dir / "deployment_info.json"
        info_file.write_text(json.dumps(deployment_info, indent=2))
        
        self.log_deployment(f"✅ Deployment prepared: {deployment_info['files_deployed']} files")
        return True
        
    def deploy_to_cloudflare(self):
        """Deploy to Cloudflare Pages"""
        self.log_deployment("Deploying to Cloudflare Pages...")
        
        # Check if Cloudflare CLI is available
        try:
            result = subprocess.run(["wrangler", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log_deployment("❌ Cloudflare Wrangler CLI not found", "ERROR")
                return False
        except:
            self.log_deployment("❌ Cloudflare Wrangler CLI not installed", "ERROR")
            return False
            
        # Deploy using Wrangler
        try:
            deploy_cmd = f"wrangler pages deploy deploy --project-name {self.config['cloudflare']['project_name']}"
            result = subprocess.run(deploy_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log_deployment("✅ Successfully deployed to Cloudflare Pages")
                return True
            else:
                self.log_deployment(f"❌ Deployment failed: {result.stderr}", "ERROR")
                return False
        except Exception as e:
            self.log_deployment(f"❌ Deployment error: {e}", "ERROR")
            return False
            
    def validate_deployment(self):
        """Validate the deployment"""
        self.log_deployment("Validating deployment...")
        
        pages_url = self.config['cloudflare']['pages_url']
        
        try:
            response = requests.get(pages_url, timeout=30)
            if response.status_code == 200:
                self.log_deployment("✅ Deployment validation successful")
                return True
            else:
                self.log_deployment(f"❌ Deployment validation failed: HTTP {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log_deployment(f"❌ Deployment validation error: {e}", "ERROR")
            return False
            
    def rollback_deployment(self):
        """Rollback to previous deployment"""
        self.log_deployment("Rolling back deployment...")
        
        # This would implement rollback logic
        # For now, just log the action
        self.log_deployment("⚠️ Rollback functionality not yet implemented", "WARN")
        return False
        
    def send_notification(self, message, success=True):
        """Send deployment notification"""
        if not self.config['notifications']['enabled']:
            return
            
        status = "✅ SUCCESS" if success else "❌ FAILED"
        notification = f"{status} - Verakore Deployment\n{message}"
        
        # Add Slack notification if configured
        if self.config['notifications']['slack_webhook']:
            try:
                payload = {"text": notification}
                requests.post(self.config['notifications']['slack_webhook'], json=payload)
            except:
                pass
                
        self.log_deployment(f"Notification sent: {notification}")
        
    def deploy(self):
        """Main deployment process"""
        self.log_deployment("Starting Verakore deployment pipeline...")
        
        # Step 1: Quality Gates
        if not self.run_quality_gates():
            self.log_deployment("❌ Quality gates failed - deployment aborted", "ERROR")
            self.send_notification("Quality gates failed", False)
            return False
            
        # Step 2: Prepare Deployment
        if not self.prepare_deployment():
            self.log_deployment("❌ Deployment preparation failed", "ERROR")
            self.send_notification("Deployment preparation failed", False)
            return False
            
        # Step 3: Deploy to Cloudflare
        if not self.deploy_to_cloudflare():
            self.log_deployment("❌ Cloudflare deployment failed", "ERROR")
            self.send_notification("Cloudflare deployment failed", False)
            return False
            
        # Step 4: Validate Deployment
        if not self.validate_deployment():
            self.log_deployment("❌ Deployment validation failed", "ERROR")
            self.send_notification("Deployment validation failed", False)
            return False
            
        # Success
        self.log_deployment("🎉 Deployment pipeline completed successfully!")
        self.send_notification("Deployment completed successfully", True)
        return True

def main():
    """Main function"""
    controller = DeploymentController()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "deploy":
            success = controller.deploy()
            sys.exit(0 if success else 1)
        elif command == "quality-gates":
            success = controller.run_quality_gates()
            sys.exit(0 if success else 1)
        elif command == "validate":
            success = controller.validate_deployment()
            sys.exit(0 if success else 1)
        elif command == "rollback":
            success = controller.rollback_deployment()
            sys.exit(0 if success else 1)
        else:
            print("Usage: python deploy.py [deploy|quality-gates|validate|rollback]")
    else:
        # Default: run full deployment
        success = controller.deploy()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()