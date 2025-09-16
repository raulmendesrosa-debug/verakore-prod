#!/usr/bin/env python3
"""
Character Encoding Quality Control Script
Detects and reports character encoding issues in HTML files
"""

import re
import os
import sys
from pathlib import Path

def detect_encoding_issues(file_path):
    """Detect common character encoding issues in HTML files"""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        issues.append(f"File encoding issue: {file_path}")
        return issues
    
    # Common problematic character patterns
    problematic_patterns = [
        (r'â€"', 'Em dash (—) should be &#x2014;'),
               (r'â†'', 'Arrow should be &#x2192;'),
        (r'â€™', 'Right single quote (') should be &#x2019;'),
        (r'â€œ', 'Left double quote (") should be &#x201C;'),
        (r'â€', 'Right double quote (") should be &#x201D;'),
        (r'â€¢', 'Bullet (•) should be &#x2022;'),
        (r'â€¦', 'Ellipsis (…) should be &#x2026;'),
        (r'â€"', 'En dash (–) should be &#x2013;'),
        (r'â€˜', 'Left single quote (') should be &#x2018;'),
    ]
    
    for pattern, description in problematic_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"Line {line_num}: {description}")
    
    # Check for common emoji issues
    emoji_patterns = [
        (r'ðŸ'‹', 'Waving hand emoji (👋) should be &#x1F44B;'),
        (r'ðŸ'Œ', 'Speech bubble emoji (💬) should be &#x1F4AC;'),
        (r'ðŸ'‡', 'Check mark emoji (✅) should be &#x2705;'),
        (r'ðŸ'‡', 'Cross mark emoji (❌) should be &#x274C;'),
    ]
    
    for pattern, description in emoji_patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"Line {line_num}: {description}")
    
    return issues

def main():
    """Main function to check all HTML files"""
    html_files = list(Path('.').glob('*.html'))
    
    if not html_files:
        print("No HTML files found in current directory")
        return
    
    total_issues = 0
    
    for html_file in html_files:
        print(f"\n🔍 Checking {html_file}...")
        issues = detect_encoding_issues(html_file)
        
        if issues:
            print(f"❌ Found {len(issues)} encoding issues:")
            for issue in issues:
                print(f"   • {issue}")
            total_issues += len(issues)
        else:
            print("✅ No encoding issues found")
    
    print(f"\n📊 Summary: {total_issues} total encoding issues found")
    
    if total_issues > 0:
        print("\n💡 Run 'python fix-encoding.py' to automatically fix these issues")
        sys.exit(1)
    else:
        print("\n🎉 All files pass character encoding quality control!")
        sys.exit(0)

if __name__ == "__main__":
    main()
