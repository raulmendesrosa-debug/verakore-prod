#!/usr/bin/env python3
"""
GoDaddy File Manager Deployment Script
Deploy Verakore website using GoDaddy File Manager
"""

import os
import zipfile
import shutil
from pathlib import Path

class GoDaddyFileManagerDeployment:
    def __init__(self):
        self.base_path = Path.cwd()
        self.deploy_dir = Path(self.base_path, "godaddy_deploy")
        
    def create_deployment_package(self):
        """Create deployment package for GoDaddy File Manager"""
        print("🚀 Creating GoDaddy File Manager deployment package...")
        
        # Create deployment directory
        if self.deploy_dir.exists():
            shutil.rmtree(self.deploy_dir)
        self.deploy_dir.mkdir()
        
        # Files to deploy
        files_to_deploy = [
            "index.html",
            "services.html", 
            "careers.html",
            "privacy-policy.html",
            "terms-of-service.html",
            "cookie-policy.html",
            "assets",
            "README.md"
        ]
        
        print("📦 Copying files to deployment directory...")
        
        for item in files_to_deploy:
            src_path = Path(self.base_path, item)
            dst_path = Path(self.deploy_dir, item)
            
            if src_path.exists():
                if src_path.is_dir():
                    shutil.copytree(src_path, dst_path)
                else:
                    shutil.copy2(src_path, dst_path)
                print(f"✅ Copied: {item}")
            else:
                print(f"⚠️  Not found: {item}")
        
        # Create ZIP package
        zip_path = Path(self.deploy_dir, "verakore-godaddy-deploy.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.deploy_dir):
                for file in files:
                    if not file.endswith('.zip'):
                        file_path = Path(root, file)
                        arc_path = file_path.relative_to(self.deploy_dir)
                        zipf.write(file_path, arc_path)
        
        print(f"✅ Deployment package created: {zip_path}")
        return zip_path
    
    def create_deployment_instructions(self):
        """Create deployment instructions for GoDaddy File Manager"""
        instructions = """# 🚀 GoDaddy File Manager Deployment Instructions

## 📋 Step-by-Step Deployment Guide

### Step 1: Access GoDaddy File Manager
1. **Login to your GoDaddy account**
2. **Go to "My Products"**
3. **Find "verakore.com" domain**
4. **Click "Manage"**
5. **Click "File Manager"**

### Step 2: Upload Your Website Files
1. **Navigate to the public_html folder** (or www folder)
2. **Delete any existing files** (if any)
3. **Upload the ZIP file:** `verakore-godaddy-deploy.zip`
4. **Extract the ZIP file** in the public_html directory
5. **Delete the ZIP file** after extraction

### Step 3: Verify Deployment
1. **Visit your website:** https://verakore.com
2. **Test all pages:**
   - Homepage: https://verakore.com
   - Services: https://verakore.com/services.html
   - Careers: https://verakore.com/careers.html
   - Privacy Policy: https://verakore.com/privacy-policy.html
   - Terms of Service: https://verakore.com/terms-of-service.html
   - Cookie Policy: https://verakore.com/cookie-policy.html

### Step 4: Configure Contact Form
**Since GoDaddy doesn't have built-in form handling like Netlify:**
1. **Use a third-party service** like Formspree, FormSubmit, or Getform
2. **Update the contact form** to use the service
3. **Test form submissions**

## 🔧 Alternative: Use Formspree for Contact Forms

### Formspree Integration:
1. **Go to [formspree.io](https://formspree.io)**
2. **Sign up for free account**
3. **Create a new form**
4. **Get your form endpoint**
5. **Update contact form** in index.html

### Updated Contact Form Code:
```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
  <input type="text" name="name" required>
  <input type="email" name="email" required>
  <textarea name="message" required></textarea>
  <button type="submit">Send Message</button>
</form>
```

## 🎯 Benefits of GoDaddy File Manager:
- ✅ **Direct control** over your files
- ✅ **No third-party dependencies**
- ✅ **Full access** to your hosting
- ✅ **Custom domain** already configured
- ✅ **SSL certificate** included

## 📞 Support:
- **GoDaddy Support:** [help.godaddy.com](https://help.godaddy.com)
- **File Manager Help:** [help.godaddy.com/file-manager](https://help.godaddy.com/file-manager)

## 🎉 Success!
Once deployed, your Verakore website will be live at https://verakore.com!
"""
        
        instructions_path = Path(self.deploy_dir, "DEPLOYMENT_INSTRUCTIONS.md")
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"✅ Deployment instructions created: {instructions_path}")
        return instructions_path

def main():
    deployment = GoDaddyFileManagerDeployment()
    
    print("🎯 GoDaddy File Manager Deployment System")
    print("=" * 50)
    
    # Create deployment package
    zip_path = deployment.create_deployment_package()
    
    # Create instructions
    instructions_path = deployment.create_deployment_instructions()
    
    print("\n🎉 Deployment package ready!")
    print(f"📦 ZIP file: {zip_path}")
    print(f"📖 Instructions: {instructions_path}")
    
    print("\n📋 Next Steps:")
    print("1. Login to your GoDaddy account")
    print("2. Go to File Manager for verakore.com")
    print("3. Upload and extract the ZIP file")
    print("4. Your website will be live at https://verakore.com")
    
    print("\n💡 Note: You'll need to set up a contact form service")
    print("   like Formspree since GoDaddy doesn't handle forms natively.")

if __name__ == "__main__":
    main()
