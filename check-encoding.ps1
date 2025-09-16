# Character Encoding Quality Control - PowerShell Version
# Detects and reports character encoding issues in HTML files

Write-Host "🔍 Character Encoding Quality Control" -ForegroundColor Cyan
Write-Host "=" * 40 -ForegroundColor Cyan

$htmlFiles = Get-ChildItem -Path "." -Filter "*.html"

if ($htmlFiles.Count -eq 0) {
    Write-Host "❌ No HTML files found in current directory" -ForegroundColor Red
    exit 1
}

$totalIssues = 0

foreach ($file in $htmlFiles) {
    Write-Host "`n🔍 Checking $($file.Name)..." -ForegroundColor Yellow
    
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $issues = @()
    
    # Common problematic character patterns
    $patterns = @{
        'â€"' = 'Em dash (—) should be &#x2014;'
        'â†'' = 'Arrow (→) should be &#x2192;'
        'â€™' = 'Right single quote (') should be &#x2019;'
        'â€œ' = 'Left double quote (") should be &#x201C;'
        'â€' = 'Right double quote (") should be &#x201D;'
        'â€¢' = 'Bullet (•) should be &#x2022;'
        'â€¦' = 'Ellipsis (…) should be &#x2026;'
        'â€˜' = 'Left single quote (') should be &#x2018;'
        'ðŸ'‹' = 'Waving hand emoji (👋) should be &#x1F44B;'
        'ðŸ'Œ' = 'Speech bubble emoji (💬) should be &#x1F4AC;'
    }
    
    foreach ($pattern in $patterns.Keys) {
        if ($content -match $pattern) {
            $matches = [regex]::Matches($content, [regex]::Escape($pattern))
            foreach ($match in $matches) {
                $lineNum = ($content.Substring(0, $match.Index) -split "`n").Count
                $issues += "Line $lineNum`: $($patterns[$pattern])"
            }
        }
    }
    
    if ($issues.Count -gt 0) {
        Write-Host "❌ Found $($issues.Count) encoding issues:" -ForegroundColor Red
        foreach ($issue in $issues) {
            Write-Host "   • $issue" -ForegroundColor Red
        }
        $totalIssues += $issues.Count
    } else {
        Write-Host "✅ No encoding issues found" -ForegroundColor Green
    }
}

Write-Host "`n📊 Summary: $totalIssues total encoding issues found" -ForegroundColor Cyan

if ($totalIssues -gt 0) {
    Write-Host "`n💡 Run 'python fix-encoding.py' to automatically fix these issues" -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "`n🎉 All files pass character encoding quality control!" -ForegroundColor Green
    exit 0
}
