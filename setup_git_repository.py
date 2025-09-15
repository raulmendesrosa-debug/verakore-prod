#!/usr/bin/env python3
"""
Verakore Website - Git Repository Setup Script
Prepares your website files for GitHub integration with Netlify
"""

import os
import shutil
from pathlib import Path

def setup_git_repository():
    """Setup Git repository for Verakore website"""
    
    print("🚀 Verakore Website - Git Repository Setup")
    print("=" * 50)
    
    # Get current directory
    current_dir = Path.cwd()
    print(f"📁 Current directory: {current_dir}")
    
    # Create .gitignore file
    gitignore_content = """# Verakore Website - Git Ignore File

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Dependency directories
node_modules/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# Temporary files
*.tmp
*.temp

# Backup files
*.bak
*.backup

# Archive files
*.zip
*.tar.gz
*.rar

# Local development files
local/
dev/
test/
"""
    
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    
    print("✅ Created .gitignore file")
    
    # Create README.md
    readme_content = """# Verakore IT Services Website

Professional website for Verakore IT Services company.

## 🚀 Features

- **Professional Design** - Modern, responsive website
- **Contact Form** - Integrated with Netlify Forms
- **Service Pages** - Detailed service descriptions
- **Career Applications** - Job application system
- **Legal Pages** - Privacy Policy, Terms of Service, Cookie Policy
- **Mobile Responsive** - Works on all devices
- **SEO Optimized** - Search engine friendly

## 📧 Contact

- **Phone:** (617) 865-9705
- **Email:** info@verakore.com
- **Website:** https://verakore.com

## 🛠️ Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Bootstrap
- **JavaScript** - Interactive features
- **Netlify** - Hosting and form handling
- **GitHub** - Version control

## 🚀 Deployment

This website is automatically deployed to Netlify when changes are pushed to the main branch.

### Manual Deployment
1. Go to [netlify.com](https://netlify.com)
2. Drag the website files to the deploy area
3. Configure custom domain and email notifications

### Git Integration
1. Push changes to GitHub
2. Netlify automatically deploys
3. Website updates live in 2-3 minutes

## 📁 File Structure

```
verakore-website/
├── index.html              # Homepage
├── services.html           # Services page
├── careers.html            # Careers page
├── privacy-policy.html     # Privacy policy
├── terms-of-service.html   # Terms of service
├── cookie-policy.html      # Cookie policy
├── netlify.toml           # Netlify configuration
├── assets/
│   ├── css/
│   │   └── styles.css     # Main stylesheet
│   ├── images/
│   │   ├── logos/         # Company logos
│   │   ├── hero/          # Hero images
│   │   ├── services/      # Service images
│   │   ├── team/          # Team photos
│   │   └── portfolio/     # Portfolio images
│   └── js/
│       └── scripts.js     # JavaScript files
└── README.md              # This file
```

## 🔧 Development

### Local Development
1. Clone the repository
2. Open `index.html` in a web browser
3. Make changes to HTML, CSS, or JavaScript
4. Test locally before pushing

### Making Changes
1. Edit files locally
2. Test changes in browser
3. Commit changes: `git commit -m "Description of changes"`
4. Push to GitHub: `git push origin main`
5. Netlify automatically deploys

## 📊 Performance

- **Fast Loading** - Optimized images and code
- **Global CDN** - Netlify's worldwide network
- **Mobile Responsive** - Works on all devices
- **SEO Optimized** - Search engine friendly

## 🔒 Security

- **HTTPS** - Secure connections
- **Security Headers** - Protection against common attacks
- **Form Validation** - Spam protection
- **Regular Updates** - Keep dependencies updated

## 📞 Support

For technical support or questions about this website, contact:
- **Email:** info@verakore.com
- **Phone:** (617) 865-9705

## 📄 License

© 2024 Verakore IT Services. All rights reserved.
"""
    
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ Created README.md file")
    
    # Create initial commit message
    commit_message = """Initial commit: Verakore IT Services Website

- Professional homepage with contact form and chatbot
- Services page with detailed service descriptions
- Careers page with application form
- Legal pages (Privacy Policy, Terms of Service, Cookie Policy)
- Mobile responsive design
- Netlify Forms integration for contact form
- Security headers and optimizations
- Professional branding and logo
- Clickable phone numbers and email links
- Video meeting options (Zoom, Teams, Google Meet)

Ready for deployment to Netlify with Git integration."""
    
    with open('COMMIT_MESSAGE.txt', 'w', encoding='utf-8') as f:
        f.write(commit_message)
    
    print("✅ Created initial commit message")
    
    print("\n" + "=" * 50)
    print("🎯 NEXT STEPS:")
    print("=" * 50)
    print("1. Create GitHub repository:")
    print("   - Go to github.com")
    print("   - Click 'New repository'")
    print("   - Name: verakore-website")
    print("   - Set to Public")
    print("   - Don't initialize with README")
    print()
    print("2. Initialize Git repository:")
    print("   git init")
    print("   git add .")
    print("   git commit -m \"Initial commit: Verakore IT Services Website\"")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/YOUR_USERNAME/verakore-website.git")
    print("   git push -u origin main")
    print()
    print("3. Connect to Netlify:")
    print("   - Go to netlify.com")
    print("   - Click 'New site from Git'")
    print("   - Choose GitHub")
    print("   - Select verakore-website repository")
    print("   - Build command: (leave empty)")
    print("   - Publish directory: . (root)")
    print("   - Click 'Deploy site'")
    print()
    print("4. Configure custom domain:")
    print("   - Add verakore.com in Domain Management")
    print("   - Update DNS records at your registrar")
    print("   - Wait 24-48 hours for propagation")
    print()
    print("5. Set up email notifications:")
    print("   - Go to Forms section")
    print("   - Add notification email: info@verakore.com")
    print("   - Test contact form")
    print()
    print("🎉 Your website will be live with automatic deployments!")
    print("=" * 50)

if __name__ == "__main__":
    try:
        setup_git_repository()
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")
