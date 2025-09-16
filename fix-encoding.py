#!/usr/bin/env python3
"""
Character Encoding Fix Script
Automatically fixes common character encoding issues in HTML files
"""

import re
import os
import sys
from pathlib import Path
import shutil
from datetime import datetime

def fix_encoding_issues(file_path):
    """Fix common character encoding issues in HTML files"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        print(f"❌ Cannot read file: {file_path}")
        return False
    
    original_content = content
    
    # Character replacement mappings
    replacements = [
        # Em dashes and en dashes
        (r'â€"', '&#x2014;'),  # Em dash
        (r'â€"', '&#x2013;'),  # En dash
        
        # Arrows
        (r'â†'|â†'', '&#x2192;'),  # Right arrow
        (r'â†'|â†'', '&#x2190;'),  # Left arrow
        (r'â†'|â†'', '&#x2191;'),  # Up arrow
        (r'â†'|â†'', '&#x2193;'),  # Down arrow
        
        # Quotes
        (r'â€™', '&#x2019;'),  # Right single quote
        (r'â€˜', '&#x2018;'),  # Left single quote
        (r'â€œ', '&#x201C;'),  # Left double quote
        (r'â€', '&#x201D;'),  # Right double quote
        
        # Other punctuation
        (r'â€¢', '&#x2022;'),  # Bullet
        (r'â€¦', '&#x2026;'),  # Ellipsis
        
        # Common emojis
        (r'ðŸ'‹', '&#x1F44B;'),  # Waving hand
        (r'ðŸ'Œ', '&#x1F4AC;'),  # Speech bubble
        (r'ðŸ'‡', '&#x2705;'),   # Check mark
        (r'ðŸ'‡', '&#x274C;'),   # Cross mark
        (r'ðŸ'‡', '&#x1F680;'),  # Rocket
        (r'ðŸ'‡', '&#x1F4E1;'),  # Light bulb
    ]
    
    fixes_applied = 0
    
    for pattern, replacement in replacements:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            fixes_applied += len(matches)
            print(f"   • Fixed {len(matches)} instances of {pattern}")
    
    if fixes_applied > 0:
        # Create backup
        backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        shutil.copy2(file_path, backup_path)
        print(f"   • Created backup: {backup_path}")
        
        # Write fixed content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"   ✅ Applied {fixes_applied} fixes to {file_path}")
        return True
    else:
        print(f"   ℹ️  No fixes needed for {file_path}")
        return False

def main():
    """Main function to fix all HTML files"""
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("No HTML files found in current directory")
        return
    
    print("🔧 Character Encoding Fix Tool")
    print("=" * 40)
    
    total_fixes = 0
    files_fixed = 0
    
    for html_file in html_files:
        print(f"\n🔍 Processing {html_file}...")
        if fix_encoding_issues(html_file):
            files_fixed += 1
    
    print(f"\n📊 Summary:")
    print(f"   • Files processed: {len(html_files)}")
    print(f"   • Files fixed: {files_fixed}")
    
    if files_fixed > 0:
        print(f"\n✅ Character encoding fixes applied!")
        print("💡 Run 'python check-encoding.py' to verify fixes")
    else:
        print(f"\n🎉 No character encoding issues found!")

if __name__ == "__main__":
    main()
