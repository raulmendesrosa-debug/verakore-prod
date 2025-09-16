# Verakore Workspace Automation System

## Overview
A comprehensive cron-like automation system for maintaining workspace consistency, quality control, and automated maintenance tasks.

## 🚀 Quick Start

### Windows (Recommended)
```powershell
# Install automation tasks
.\automation.ps1 -Install

# Run manual check
.\automation.ps1 -Command check

# Check task status
.\automation.ps1 -Status
```

### Cross-Platform
```bash
# Run daily maintenance
python automation.py daily

# Run weekly maintenance
python automation.py weekly

# Manual check
python automation.py check
```

## 📋 Features

### 1. Character Encoding Quality Control
- **Automatic detection** of encoding issues
- **Auto-fix** with backup creation
- **Cross-platform support** (Python, PowerShell, Batch)
- **Pre-commit validation**

### 2. Mobile Responsiveness Monitoring
- **CSS validation** for mobile breakpoints
- **Responsive design checks**
- **Mobile-first validation**

### 3. Performance Monitoring
- **File size analysis**
- **Performance threshold checks**
- **Optimization recommendations**

### 4. Git Repository Health
- **Status monitoring**
- **Uncommitted changes detection**
- **Branch health checks**

### 5. Automated Backups
- **Scheduled backups**
- **Retention management**
- **Selective file inclusion**

### 6. Deployment Readiness
- **Pre-deployment validation**
- **Quality gate checks**
- **Environment-specific rules**

## ⚙️ Configuration

### Environment Settings
The system supports three environments:

#### Development
- ✅ Auto-fix enabled
- ⚠️ Relaxed checks
- 📅 Daily backups

#### Staging
- ❌ Auto-fix disabled
- ✅ Strict checks
- 📅 Daily backups

#### Production
- ❌ Auto-fix disabled
- ✅ Strict checks
- 📅 Weekly backups
- ✅ Pre-deploy validation

### Customization
Edit `automation_config.json` to customize:
- Check frequencies
- Quality thresholds
- Backup retention
- Notification settings

## 📅 Scheduling

### Windows Task Scheduler Integration
The PowerShell script automatically creates scheduled tasks:

- **Daily Maintenance**: 9:00 AM
- **Weekly Maintenance**: Monday 9:00 AM
- **Deployment Check**: 5:00 PM daily

### Manual Scheduling
```bash
# Run specific tasks
python automation.py daily
python automation.py weekly
python automation.py check
python automation.py backup
python automation.py deploy-check
```

## 🔧 Commands

### PowerShell Commands
```powershell
# Install scheduled tasks
.\automation.ps1 -Install

# Uninstall scheduled tasks
.\automation.ps1 -Uninstall

# Check task status
.\automation.ps1 -Status

# Run specific command
.\automation.ps1 -Command daily
.\automation.ps1 -Command weekly
.\automation.ps1 -Command check
.\automation.ps1 -Command backup
.\automation.ps1 -Command deploy-check
```

### Python Commands
```bash
# Start continuous monitoring
python automation.py start

# Run maintenance tasks
python automation.py daily
python automation.py weekly

# Manual operations
python automation.py check
python automation.py backup
python automation.py deploy-check
```

## 📊 Monitoring

### Log Files
- **automation.log**: Main automation log
- **Character encoding logs**: Detailed encoding fixes
- **Performance logs**: Performance monitoring data

### Log Levels
- **INFO**: Normal operations
- **WARNING**: Issues that don't stop execution
- **ERROR**: Critical issues requiring attention

### Alerts
- **Console notifications**: Real-time feedback
- **File logging**: Persistent record
- **Email alerts**: (Configurable)

## 🛠️ Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Install Python 3.x from python.org
# Or use Windows Store version
```

#### Permission Issues
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Task Scheduler Issues
```powershell
# Check task status
.\automation.ps1 -Status

# Reinstall tasks
.\automation.ps1 -Uninstall
.\automation.ps1 -Install
```

### Debug Mode
```bash
# Enable debug logging
python automation.py check --debug
```

## 🔄 Workflow Integration

### Pre-commit Hooks
```bash
# Install git pre-commit hook
cp pre-commit-hook.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### CI/CD Integration
```yaml
# Example GitHub Actions
- name: Run Quality Checks
  run: python automation.py check
```

### Development Workflow
1. **Before coding**: Run `python automation.py check`
2. **During development**: Automated daily checks
3. **Before commit**: Pre-commit hooks validate
4. **Before deploy**: Deployment readiness check

## 📈 Benefits

### Consistency
- **Standardized quality checks**
- **Consistent character encoding**
- **Uniform mobile responsiveness**

### Automation
- **Reduced manual work**
- **Scheduled maintenance**
- **Automated backups**

### Quality Assurance
- **Proactive issue detection**
- **Automated fixes where safe**
- **Comprehensive validation**

### Reliability
- **Backup protection**
- **Error handling**
- **Recovery procedures**

## 🎯 Best Practices

### Daily Routine
1. Check automation logs
2. Review any warnings
3. Address critical issues
4. Verify mobile responsiveness

### Weekly Routine
1. Review backup status
2. Check deployment readiness
3. Update automation config if needed
4. Review performance metrics

### Before Deployment
1. Run deployment readiness check
2. Verify all quality gates pass
3. Check mobile responsiveness
4. Validate character encoding

## 📚 Additional Resources

- **ENCODING_QC.md**: Character encoding quality control
- **DEPLOYMENT_CONTROL_FRAMEWORK.md**: Deployment automation
- **automation.log**: Runtime logs and diagnostics
- **automation_config.json**: Configuration reference

## 🤝 Support

For issues or questions:
1. Check automation.log for errors
2. Review configuration settings
3. Test individual components
4. Consult documentation

---

**Verakore Automation System v2.0** - Maintaining workspace excellence through intelligent automation.
