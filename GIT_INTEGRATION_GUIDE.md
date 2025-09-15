# 🚀 Verakore Website - Git Integration with Netlify

## 🎯 **Why Git Integration is Better**

### **✅ Advantages:**
- **🔄 Automatic Deployments** - Every code change goes live automatically
- **📝 Version Control** - Track all changes and rollback if needed
- **👥 Team Collaboration** - Multiple people can work on the site
- **🚀 Deploy Previews** - Test changes before going live
- **🔧 Better Workflow** - Professional development process
- **📊 Build Logs** - See exactly what happens during deployment

### **❌ Manual Upload Limitations:**
- **Manual process** every time you make changes
- **No version control** or change tracking
- **No rollback** if something breaks
- **No team collaboration** features

## 🛠️ **STEP-BY-STEP GIT INTEGRATION SETUP**

### **Step 1: Create GitHub Repository (5 minutes)**

#### **1.1 Create New Repository**
1. **Go to [github.com](https://github.com)**
2. **Click "New repository"** (green button)
3. **Repository name:** `verakore-website`
4. **Description:** `Verakore IT Services Website`
5. **Set to Public** (free hosting)
6. **Don't initialize** with README (we have files already)
7. **Click "Create repository"**

#### **1.2 Upload Your Website Files**
1. **Download GitHub Desktop** or use Git command line
2. **Clone the repository** to your computer
3. **Copy all files** from `website/public/` to the repository folder
4. **Commit and push** to GitHub

### **Step 2: Connect Netlify to GitHub (3 minutes)**

#### **2.1 Connect Repository**
1. **Go to [netlify.com](https://netlify.com)**
2. **Click "New site from Git"**
3. **Choose "GitHub"** as your Git provider
4. **Authorize Netlify** to access your GitHub
5. **Select your repository:** `verakore-website`

#### **2.2 Configure Build Settings**
```
Build command: (leave empty)
Publish directory: . (root directory)
```

#### **2.3 Deploy**
1. **Click "Deploy site"**
2. **Wait 2-3 minutes** for first deployment
3. **Your site will be live** at a Netlify URL

### **Step 3: Configure Custom Domain (5 minutes)**

#### **3.1 Add Domain**
1. **Go to Site Settings** → **Domain Management**
2. **Add custom domain:** `verakore.com`
3. **Add www subdomain:** `www.verakore.com`

#### **3.2 Update DNS**
1. **Get DNS records** from Netlify
2. **Update at your domain registrar:**
   ```
   CNAME: www → your-site-name.netlify.app
   A Record: @ → 75.2.60.5
   ```

### **Step 4: Configure Email Notifications (2 minutes)**

#### **4.1 Set Up Forms**
1. **Go to Site Dashboard** → **Forms**
2. **Find "contact-form"** submissions
3. **Add notification email:** `info@verakore.com`
4. **Enable email notifications**

## 🔄 **AUTOMATED WORKFLOW**

### **How It Works:**
1. **Make changes** to your website files
2. **Commit changes** to Git
3. **Push to GitHub**
4. **Netlify automatically deploys** the changes
5. **Your website updates** live in 2-3 minutes

### **Example Workflow:**
```bash
# Make changes to your website
git add .
git commit -m "Updated contact form"
git push origin main

# Netlify automatically deploys!
```

## 🚀 **DEPLOY PREVIEWS**

### **What Are Deploy Previews?**
- **Test changes** before going live
- **Share with clients** for approval
- **Review changes** in a safe environment
- **No risk** to your live website

### **How to Use:**
1. **Create a pull request** on GitHub
2. **Netlify creates a preview** URL
3. **Test your changes** on the preview
4. **Merge the pull request** to go live

## 📊 **BUILD LOGS & MONITORING**

### **What You Get:**
- **Build logs** - See exactly what happens during deployment
- **Deploy history** - Track all deployments
- **Performance metrics** - Monitor site speed
- **Form submissions** - Track contact form usage
- **Error monitoring** - Catch issues early

## 🔧 **ADVANCED FEATURES**

### **Branch Deploys:**
- **Deploy different branches** for testing
- **Staging environment** for development
- **Production environment** for live site

### **Environment Variables:**
- **Store sensitive data** securely
- **API keys** and configuration
- **Different settings** for different environments

### **Build Hooks:**
- **Trigger deployments** from external services
- **Integrate with other tools**
- **Automate workflows**

## 🎯 **RECOMMENDED REPOSITORY STRUCTURE**

```
verakore-website/
├── index.html
├── services.html
├── careers.html
├── privacy-policy.html
├── terms-of-service.html
├── cookie-policy.html
├── netlify.toml
├── assets/
│   ├── css/
│   ├── images/
│   └── js/
├── README.md
└── .gitignore
```

## 📝 **GIT COMMANDS REFERENCE**

### **Basic Git Commands:**
```bash
# Initialize repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main

# Check status
git status

# View history
git log
```

### **Useful Git Commands:**
```bash
# Create new branch
git checkout -b feature/new-feature

# Switch branches
git checkout main

# Merge branch
git merge feature/new-feature

# Rollback changes
git reset --hard HEAD~1
```

## 🚨 **TROUBLESHOOTING**

### **Build Fails?**
1. **Check build logs** in Netlify dashboard
2. **Verify file paths** are correct
3. **Check for syntax errors** in HTML/CSS
4. **Ensure all files** are committed

### **Site Not Updating?**
1. **Check if changes** are pushed to GitHub
2. **Verify build settings** in Netlify
3. **Check build logs** for errors
4. **Clear browser cache**

### **Domain Not Working?**
1. **Verify DNS records** are correct
2. **Wait 24-48 hours** for propagation
3. **Check SSL certificate** status
4. **Test both www and non-www**

## 🎉 **BENEFITS OF GIT INTEGRATION**

### **For Your Business:**
- ✅ **Professional workflow** - Industry standard
- ✅ **Easy updates** - Make changes quickly
- ✅ **Version control** - Track all changes
- ✅ **Team collaboration** - Work with others
- ✅ **Deploy previews** - Test before going live
- ✅ **Automatic backups** - Code is always safe

### **For Your Clients:**
- ✅ **Faster updates** - Changes go live quickly
- ✅ **Better reliability** - Fewer deployment errors
- ✅ **Professional service** - Modern development practices
- ✅ **Easy maintenance** - Updates are simple

## 🚀 **NEXT STEPS**

1. **Create GitHub repository** for your website
2. **Upload your website files** to the repository
3. **Connect Netlify** to your GitHub repository
4. **Configure build settings** and deploy
5. **Set up custom domain** and email notifications
6. **Test the automated workflow**

## 💡 **PRO TIPS**

### **Best Practices:**
- **Commit often** - Small, frequent commits
- **Use descriptive messages** - Explain what you changed
- **Test locally** - Make sure changes work before pushing
- **Use branches** - Keep main branch stable
- **Review changes** - Use deploy previews

### **Workflow Tips:**
- **Make changes** → **Test locally** → **Commit** → **Push** → **Deploy**
- **Use pull requests** for major changes
- **Keep main branch** always deployable
- **Use meaningful commit messages**

**Git integration will make your Verakore website much more professional and easier to maintain!** 🚀
