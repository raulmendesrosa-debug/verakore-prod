# Verakore Workspace Startup Health Check Integration

## 🚀 Automatic Startup Health Checks

This system ensures your workspace is healthy every time you start working. Multiple integration options are available:

## 📋 Quick Setup Options

### Option 1: VS Code/Cursor Integration (Recommended)
```bash
# Open workspace file
code .vscode/workspace.code-workspace
```
- ✅ **Automatic health check** when workspace opens
- ✅ **Integrated tasks** for manual runs
- ✅ **Debug configurations** available

### Option 2: Windows Startup Integration
```bash
# Run setup
setup-startup.bat
```
- ✅ **Runs when Windows starts**
- ✅ **Runs when user logs in**
- ✅ **Easy to enable/disable**

### Option 3: Manual Startup Script
```bash
# Run health check
startup-health-check.bat
# or
startup-health-check.ps1
```
- ✅ **Runs once per day**
- ✅ **Quick and lightweight**
- ✅ **Cross-platform**

## 🔧 Commands Available

### Startup Health Check
```bash
python automation.py startup
```
**Lightweight checks:**
- Python availability
- Automation script exists
- Configuration valid
- Workspace structure

### Full Health Check
```bash
python automation.py check
```
**Comprehensive checks:**
- Character encoding
- Mobile responsiveness
- Performance
- Git health

### Daily Maintenance
```bash
python automation.py daily
```
**Full maintenance:**
- All health checks
- Quality validation
- Issue detection

## ⚙️ Configuration

### Startup Behavior
Edit `automation_config.json`:
```json
{
  "startup": {
    "enabled": true,
    "frequency": "once_per_day",
    "checks": ["python", "script", "config", "structure"],
    "auto_fix": false
  }
}
```

### Integration Settings
- **VS Code**: Tasks run on folder open
- **Windows**: Startup shortcut created
- **Git**: Pre-commit hooks installed
- **Manual**: Run anytime

## 📊 What Gets Checked

### Startup Health Check (Fast)
1. ✅ **Python Installation** - Required for automation
2. ✅ **Automation Script** - Core system available
3. ✅ **Configuration** - Valid JSON config
4. ✅ **Workspace Structure** - Essential files present

### Full Health Check (Comprehensive)
1. 🔍 **Character Encoding** - No garbled characters
2. 📱 **Mobile Responsiveness** - CSS media queries
3. ⚡ **Performance** - File sizes and optimization
4. 📁 **Git Health** - Repository status
5. 🚀 **Deployment Readiness** - Pre-deploy validation

## 🎯 Benefits

### Consistency
- **Same checks every time** you start working
- **Consistent environment** across sessions
- **Standardized quality** gates

### Early Detection
- **Catch issues early** before they become problems
- **Proactive maintenance** instead of reactive fixes
- **Quality assurance** built into workflow

### Productivity
- **Confidence** that workspace is ready
- **No surprises** during development
- **Automated validation** saves time

## 🛠️ Troubleshooting

### Health Check Fails
1. **Check Python**: `python --version`
2. **Check Script**: `ls automation.py`
3. **Check Config**: `cat automation_config.json`
4. **Check Logs**: `cat automation.log`

### Startup Not Working
1. **VS Code**: Check tasks.json configuration
2. **Windows**: Check startup folder permissions
3. **Manual**: Run startup script directly

### Performance Issues
1. **Reduce frequency**: Change config
2. **Lightweight mode**: Use startup check only
3. **Disable features**: Edit automation_config.json

## 📚 Integration Examples

### VS Code Tasks
```json
{
  "label": "Verakore Health Check",
  "type": "shell",
  "command": "python",
  "args": ["automation.py", "check"],
  "runOptions": {
    "runOn": "folderOpen"
  }
}
```

### Windows Startup
```batch
REM Add to startup folder
copy startup-health-check.bat "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\"
```

### Git Pre-commit
```bash
#!/bin/bash
python automation.py startup
```

## 🎉 Getting Started

### Step 1: Choose Integration
- **VS Code/Cursor**: Open workspace file
- **Windows**: Run `setup-startup.bat`
- **Manual**: Run `startup-health-check.bat`

### Step 2: Test Integration
```bash
python automation.py startup
```

### Step 3: Verify Setup
- Check automation.log for results
- Verify startup behavior
- Test manual commands

### Step 4: Customize (Optional)
- Edit automation_config.json
- Modify startup scripts
- Add custom checks

---

**Your workspace will now automatically check its health every time you start working!** 🎯
