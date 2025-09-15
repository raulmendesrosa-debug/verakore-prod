#!/usr/bin/env python3
"""
Verakore Website Deployment Script
Creates a deployment package for Netlify
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_package():
    """Create a deployment package for Netlify"""
    
    print("🚀 Verakore Website Deployment Script")
    print("=" * 50)
    
    # Get current directory (should be website/public)
    current_dir = Path.cwd()
    print(f"📁 Working directory: {current_dir}")
    
    # Files to include in deployment
    files_to_include = [
        "index.html",
        "services.html", 
        "careers.html",
        "privacy-policy.html",
        "terms-of-service.html",
        "cookie-policy.html",
        "netlify.toml",
        "DEPLOYMENT_GUIDE.md"
    ]
    
    # Directories to include
    dirs_to_include = [
        "assets"
    ]
    
    # Create deployment package
    zip_filename = "verakore-website-deploy.zip"
    
    print(f"\n📦 Creating deployment package: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add individual files
        for file in files_to_include:
            if os.path.exists(file):
                zipf.write(file)
                print(f"✅ Added: {file}")
            else:
                print(f"⚠️  Missing: {file}")
        
        # Add directories
        for dir_name in dirs_to_include:
            if os.path.exists(dir_name):
                for root, dirs, files in os.walk(dir_name):
                    for file in files:
                        file_path = os.path.join(root, file)
                        zipf.write(file_path)
                        print(f"✅ Added: {file_path}")
            else:
                print(f"⚠️  Missing directory: {dir_name}")
    
    print(f"\n🎉 Deployment package created: {zip_filename}")
    print(f"📏 Package size: {os.path.getsize(zip_filename) / 1024:.1f} KB")
    
    print("\n" + "=" * 50)
    print("🚀 NEXT STEPS:")
    print("=" * 50)
    print("1. Go to https://netlify.com")
    print("2. Sign up/Login to your account")
    print("3. Drag verakore-website-deploy.zip to the deploy area")
    print("4. Your site will be live in minutes!")
    print("\n📧 Don't forget to:")
    print("   - Configure email notifications for info@verakore.com")
    print("   - Set up custom domain verakore.com")
    print("   - Test the contact form")
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    try:
        create_deployment_package()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
