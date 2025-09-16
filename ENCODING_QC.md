# Character Encoding Quality Control System

## Overview
This system provides automated detection and fixing of character encoding issues in HTML files.

## Tools

### 1. `check-encoding.py` - Detection Tool
**Purpose**: Scans HTML files for character encoding issues
**Usage**: `python3 check-encoding.py`
**Output**: 
- ✅ No issues found
- ❌ Lists specific issues with line numbers

### 2. `fix-encoding.py` - Automatic Fix Tool
**Purpose**: Automatically fixes common character encoding issues
**Usage**: `python3 fix-encoding.py`
**Features**:
- Creates automatic backups
- Fixes common problematic characters
- Reports number of fixes applied

### 3. `pre-commit-hook.sh` - Git Integration
**Purpose**: Runs encoding checks before commits
**Usage**: Add to `.git/hooks/pre-commit`

## Common Issues Detected

| Problematic Display | Correct HTML Entity | Description |
|-------------------|-------------------|-------------|
| `â€"` | `&#x2014;` | Em dash (—) |
| `â†'` | `&#x2192;` | Right arrow (→) |
| `â€™` | `&#x2019;` | Right single quote (') |
| `â€œ` | `&#x201C;` | Left double quote (") |
| `â€` | `&#x201D;` | Right double quote (") |
| `ðŸ'‹` | `&#x1F44B;` | Waving hand emoji (👋) |
| `ðŸ'Œ` | `&#x1F4AC;` | Speech bubble emoji (💬) |

## Workflow

### Before Making Changes
```bash
python3 check-encoding.py
```

### After Making Changes
```bash
python3 fix-encoding.py
python3 check-encoding.py  # Verify fixes
```

### Git Integration
```bash
chmod +x pre-commit-hook.sh
cp pre-commit-hook.sh .git/hooks/pre-commit
```

## Best Practices

1. **Always run checks** before committing
2. **Use HTML entities** instead of raw Unicode characters
3. **Test on multiple browsers** after fixes
4. **Keep backups** of original files
5. **Document character choices** for consistency

## Troubleshooting

### If characters still don't display:
1. Check browser encoding settings
2. Verify UTF-8 meta tag: `<meta charset="UTF-8">`
3. Test with different browsers
4. Check server encoding configuration

### If script fails:
1. Ensure Python 3 is installed
2. Check file permissions
3. Verify UTF-8 file encoding
4. Check for file corruption
