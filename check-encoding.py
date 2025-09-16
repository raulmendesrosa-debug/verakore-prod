#!/usr/bin/env python3
"""
Character Encoding Quality Control Script
Detects and reports character encoding issues in HTML files
"""

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
    
    # Check for common encoding issues using byte patterns
    if b'\xe2\x80\x94'.decode('utf-8', errors='ignore') in content:
        issues.append("Found em dash encoding issue - should be &#x2014;")
    if b'\xe2\x86\x92'.decode('utf-8', errors='ignore') in content:
        issues.append("Found arrow encoding issue - should be &#x2192;")
    if b'\xe2\x80\x99'.decode('utf-8', errors='ignore') in content:
        issues.append("Found quote encoding issue - should be &#x2019;")
    if b'\xe2\x80\x9c'.decode('utf-8', errors='ignore') in content:
        issues.append("Found quote encoding issue - should be &#x201C;")
    if b'\xe2\x80\x9d'.decode('utf-8', errors='ignore') in content:
        issues.append("Found quote encoding issue - should be &#x201D;")
    
    return issues

def main():
    """Main function to check encoding issues"""
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
    else:
        target_path = '.'
    
    target_path = Path(target_path)
    
    if target_path.is_file():
        files_to_check = [target_path]
    elif target_path.is_dir():
        files_to_check = list(target_path.glob('*.html'))
    else:
        print(f"Error: Path '{target_path}' not found.")
        return
    
    total_issues = 0
    for file_path in files_to_check:
        issues = detect_encoding_issues(file_path)
        if issues:
            print(f"\nIssues found in {file_path}:")
            for issue in issues:
                print(f"  {issue}")
            total_issues += len(issues)
    
    if total_issues == 0:
        print("\n✅ No character encoding issues found.")
    else:
        print(f"\n❌ Found {total_issues} character encoding issues.")

if __name__ == "__main__":
    main()