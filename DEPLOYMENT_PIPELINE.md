# Verakore Deployment Pipeline

## 🚀 Automated Deployment System

A comprehensive deployment pipeline that ensures quality, security, and reliability for your Verakore website.

## 📋 Features

### Quality Gates
- ✅ **Character encoding validation**
- ✅ **Mobile responsiveness checks**
- ✅ **Performance testing**
- ✅ **Security scanning**
- ✅ **File size validation**

### Deployment Process
- 🔄 **Automated GitHub Actions**
- 🌍 **Cloudflare Pages integration**
- 🔒 **Security headers**
- 📊 **Performance monitoring**
- 🔄 **Rollback capabilities**

### Environments
- **Staging**: Testing environment
- **Production**: Live website
- **Automatic promotion** from staging to production

## ⚙️ Setup Instructions

### 1. Prerequisites
```bash
# Install Python dependencies
pip install requests

# Install Cloudflare Wrangler CLI
npm install -g wrangler
```

### 2. Cloudflare Configuration
1. **Get API Token**:
   - Go to Cloudflare Dashboard
   - Navigate to "My Profile" → "API Tokens"
   - Create token with "Cloudflare Pages:Edit" permissions

2. **Get Account ID**:
   - Go to Cloudflare Dashboard
   - Select your domain
   - Copy Account ID from right sidebar

3. **Update Configuration**:
   ```json
   {
     "cloudflare": {
       "account_id": "your-account-id",
       "api_token": "your-api-token",
       "project_name": "verakore-website"
     }
   }
   ```

### 3. GitHub Actions Setup
1. **Add Secrets**:
   - Go to GitHub repository settings
   - Navigate to "Secrets and variables" → "Actions"
   - Add `CLOUDFLARE_API_TOKEN`
   - Add `CLOUDFLARE_ACCOUNT_ID`

2. **Enable Actions**:
   - Actions are automatically enabled when you push the workflow file
   - Workflow triggers on push to `main` branch

## 🔧 Commands

### Manual Deployment
```bash
# Full deployment pipeline
python deploy.py deploy

# Run quality gates only
python deploy.py quality-gates

# Validate current deployment
python deploy.py validate

# Rollback deployment
python deploy.py rollback
```

### Windows Integration
```bash
# Run deployment pipeline
deploy.bat

# Setup deployment system
setup-deployment.bat
```

## 📊 Quality Gates

### Character Encoding
- Detects garbled characters
- Auto-fixes encoding issues
- Validates HTML entities

### Mobile Responsiveness
- Checks CSS media queries
- Validates mobile breakpoints
- Tests responsive design

### Performance
- Lighthouse CI integration
- File size validation
- Performance thresholds

### Security
- Security headers validation
- External script verification
- HTTPS enforcement

## 🌍 Deployment Process

### Automatic (GitHub Actions)
1. **Push to main branch**
2. **Quality gates run**
3. **Security scan**
4. **Performance test**
5. **Deploy to Cloudflare Pages**
6. **Post-deployment validation**

### Manual Deployment
1. **Run quality gates**
2. **Prepare deployment files**
3. **Deploy to Cloudflare**
4. **Validate deployment**
5. **Send notifications**

## 🔒 Security Features

### Security Headers
```http
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'...
```

### HTTPS Enforcement
- Automatic HTTPS redirect
- SSL certificate validation
- Secure cookie settings

### External Script Validation
- Whitelist trusted CDNs
- Block unauthorized scripts
- Validate external resources

## 📈 Performance Monitoring

### Lighthouse CI
- **Performance**: ≥90
- **Accessibility**: ≥90
- **Best Practices**: ≥90
- **SEO**: ≥90

### File Size Limits
- **HTML**: ≤1MB
- **CSS**: ≤512KB
- **JavaScript**: ≤1MB
- **Images**: ≤2MB

## 🔄 Rollback Process

### Automatic Rollback
- Triggers on deployment failure
- Restores previous version
- Validates rollback success

### Manual Rollback
```bash
python deploy.py rollback
```

## 📊 Monitoring & Notifications

### Deployment Notifications
- **Success**: Deployment completed
- **Failure**: Error details and rollback info
- **Performance**: Metrics and thresholds

### Channels
- **Slack**: Real-time notifications
- **Email**: Summary reports
- **Logs**: Detailed deployment logs

## 🛠️ Troubleshooting

### Common Issues

#### Deployment Fails
1. **Check quality gates**: `python deploy.py quality-gates`
2. **Check logs**: `cat deployment.log`
3. **Validate configuration**: Check `deployment_config.json`
4. **Test manually**: `deploy.bat`

#### Cloudflare Issues
1. **Verify API token**: Check permissions
2. **Check account ID**: Ensure correct ID
3. **Test Wrangler**: `wrangler --version`
4. **Check project name**: Match Cloudflare Pages project

#### GitHub Actions Issues
1. **Check secrets**: Verify API token and account ID
2. **Check workflow**: Validate `.github/workflows/deploy.yml`
3. **Check permissions**: Ensure Actions are enabled
4. **Check logs**: View Actions tab in GitHub

### Debug Mode
```bash
# Enable debug logging
python deploy.py deploy --debug
```

## 📚 Configuration Reference

### deployment_config.json
```json
{
  "cloudflare": {
    "account_id": "your-account-id",
    "project_name": "verakore-website",
    "api_token": "your-api-token"
  },
  "quality_gates": {
    "character_encoding": true,
    "mobile_responsiveness": true,
    "performance": true,
    "security": true
  },
  "performance": {
    "lighthouse_thresholds": {
      "performance": 90,
      "accessibility": 90
    }
  }
}
```

## 🎯 Best Practices

### Before Deployment
1. **Run quality gates**: Ensure all checks pass
2. **Test locally**: Validate changes
3. **Check configuration**: Verify settings
4. **Review changes**: Code review process

### During Deployment
1. **Monitor progress**: Watch deployment logs
2. **Check notifications**: Monitor alerts
3. **Validate results**: Test deployed site
4. **Document issues**: Log any problems

### After Deployment
1. **Monitor performance**: Check metrics
2. **Validate functionality**: Test features
3. **Check security**: Verify headers
4. **Monitor errors**: Watch for issues

---

**Your Verakore website now has enterprise-grade deployment automation!** 🎉
