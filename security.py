#!/usr/bin/env python3
"""
Verakore Security Scanner
Comprehensive security validation for web applications
"""

import os
import sys
import json
import re
import requests
import subprocess
import hashlib
import ssl
import socket
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
from urllib.parse import urlparse

class SecurityScanner:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "security_config.json"
        self.db_file = self.workspace_root / "security.db"
        self.log_file = self.workspace_root / "security.log"
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load security scanning configuration"""
        default_config = {
            "scanning": {
                "enabled": True,
                "interval_hours": 24,
                "retention_days": 90,
                "alerts_enabled": True
            },
            "targets": {
                "production": "https://verakore-website.pages.dev",
                "staging": "https://staging.verakore-website.pages.dev"
            },
            "security_checks": {
                "headers": True,
                "ssl": True,
                "content_security_policy": True,
                "xss_protection": True,
                "clickjacking": True,
                "mime_sniffing": True,
                "referrer_policy": True,
                "permissions_policy": True,
                "hsts": True,
                "cookies": True,
                "forms": True,
                "external_links": True,
                "file_uploads": True,
                "injection_checks": True
            },
            "vulnerability_scans": {
                "sql_injection": True,
                "xss": True,
                "csrf": True,
                "directory_traversal": True,
                "file_inclusion": True,
                "command_injection": True,
                "xml_external_entity": True,
                "server_side_request_forgery": True
            },
            "compliance": {
                "owasp_top_10": True,
                "pci_dss": False,
                "gdpr": True,
                "hipaa": False,
                "sox": False
            },
            "thresholds": {
                "critical_vulnerabilities": 0,
                "high_vulnerabilities": 2,
                "medium_vulnerabilities": 5,
                "low_vulnerabilities": 10,
                "security_score_minimum": 80
            },
            "notifications": {
                "email": "raulmendesrosa@gmail.com",
                "slack_webhook": "",
                "enabled": True
            },
            "reports": {
                "daily_summary": True,
                "weekly_report": True,
                "monthly_analysis": True
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save security scanning configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def init_database(self):
        """Initialize SQLite database for security data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create security scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                scan_type TEXT NOT NULL,
                status TEXT NOT NULL,
                vulnerabilities_found INTEGER DEFAULT 0,
                security_score INTEGER DEFAULT 0,
                scan_duration_ms INTEGER DEFAULT 0,
                details TEXT
            )
        ''')
        
        # Create vulnerabilities table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                vulnerability_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                location TEXT,
                recommendation TEXT,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create security alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS security_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                alert_type TEXT NOT NULL,
                severity TEXT NOT NULL,
                message TEXT NOT NULL,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_security(self, message, level="INFO"):
        """Log security scanning events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def check_security_headers(self, url):
        """Check security headers"""
        self.log_security(f"Checking security headers for {url}")
        
        try:
            response = requests.get(url, timeout=30)
            headers = response.headers
            
            security_headers = {
                "X-Frame-Options": "DENY",
                "X-Content-Type-Options": "nosniff",
                "X-XSS-Protection": "1; mode=block",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
                "Content-Security-Policy": "default-src 'self'",
                "Strict-Transport-Security": "max-age=31536000; includeSubDomains"
            }
            
            results = {}
            vulnerabilities = []
            
            for header, expected_value in security_headers.items():
                if header in headers:
                    actual_value = headers[header]
                    if header == "Content-Security-Policy":
                        # Check CSP for basic security
                        if "default-src 'self'" in actual_value:
                            results[header] = {"status": "GOOD", "value": actual_value}
                        else:
                            results[header] = {"status": "WARNING", "value": actual_value}
                            vulnerabilities.append({
                                "type": "Missing CSP directive",
                                "severity": "MEDIUM",
                                "description": f"CSP missing 'default-src self' directive"
                            })
                    else:
                        results[header] = {"status": "GOOD", "value": actual_value}
                else:
                    results[header] = {"status": "MISSING", "value": None}
                    vulnerabilities.append({
                        "type": "Missing security header",
                        "severity": "HIGH" if header in ["X-Frame-Options", "X-Content-Type-Options"] else "MEDIUM",
                        "description": f"Missing {header} header"
                    })
            
            return {
                "headers": results,
                "vulnerabilities": vulnerabilities,
                "score": self.calculate_header_score(results)
            }
            
        except Exception as e:
            self.log_security(f"Error checking headers for {url}: {e}", "ERROR")
            return None
            
    def calculate_header_score(self, headers):
        """Calculate security header score"""
        total_headers = len(headers)
        good_headers = sum(1 for h in headers.values() if h["status"] == "GOOD")
        return int((good_headers / total_headers) * 100) if total_headers > 0 else 0
        
    def check_ssl_security(self, url):
        """Check SSL/TLS security"""
        self.log_security(f"Checking SSL security for {url}")
        
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.hostname
            port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
            
            if parsed_url.scheme != 'https':
                return {
                    "ssl_enabled": False,
                    "vulnerabilities": [{
                        "type": "No SSL/TLS",
                        "severity": "CRITICAL",
                        "description": "Website not using HTTPS"
                    }],
                    "score": 0
                }
            
            # Check SSL certificate
            context = ssl.create_default_context()
            with socket.create_connection((hostname, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    cipher = ssock.cipher()
                    
                    vulnerabilities = []
                    score = 100
                    
                    # Check certificate validity
                    if not cert:
                        vulnerabilities.append({
                            "type": "Invalid certificate",
                            "severity": "CRITICAL",
                            "description": "SSL certificate is invalid"
                        })
                        score -= 50
                    
                    # Check cipher strength
                    if cipher and cipher[2] < 128:
                        vulnerabilities.append({
                            "type": "Weak cipher",
                            "severity": "HIGH",
                            "description": f"Weak cipher suite: {cipher[0]}"
                        })
                        score -= 30
                    
                    return {
                        "ssl_enabled": True,
                        "certificate": cert,
                        "cipher": cipher,
                        "vulnerabilities": vulnerabilities,
                        "score": max(0, score)
                    }
                    
        except Exception as e:
            self.log_security(f"Error checking SSL for {url}: {e}", "ERROR")
            return {
                "ssl_enabled": False,
                "vulnerabilities": [{
                    "type": "SSL check failed",
                    "severity": "HIGH",
                    "description": f"SSL check failed: {str(e)}"
                }],
                "score": 0
            }
            
    def check_content_security_policy(self, url):
        """Check Content Security Policy"""
        self.log_security(f"Checking CSP for {url}")
        
        try:
            response = requests.get(url, timeout=30)
            csp_header = response.headers.get('Content-Security-Policy', '')
            
            vulnerabilities = []
            score = 100
            
            # Check for common CSP issues
            if not csp_header:
                vulnerabilities.append({
                    "type": "Missing CSP",
                    "severity": "HIGH",
                    "description": "No Content Security Policy header found"
                })
                score = 0
            else:
                # Check for unsafe directives
                unsafe_patterns = [
                    r"'unsafe-inline'",
                    r"'unsafe-eval'",
                    r"data:",
                    r"javascript:"
                ]
                
                for pattern in unsafe_patterns:
                    if re.search(pattern, csp_header):
                        vulnerabilities.append({
                            "type": "Unsafe CSP directive",
                            "severity": "MEDIUM",
                            "description": f"CSP contains unsafe directive: {pattern}"
                        })
                        score -= 20
                
                # Check for missing directives
                required_directives = ['default-src', 'script-src', 'style-src']
                for directive in required_directives:
                    if directive not in csp_header:
                        vulnerabilities.append({
                            "type": "Missing CSP directive",
                            "severity": "MEDIUM",
                            "description": f"CSP missing {directive} directive"
                        })
                        score -= 15
            
            return {
                "csp_header": csp_header,
                "vulnerabilities": vulnerabilities,
                "score": max(0, score)
            }
            
        except Exception as e:
            self.log_security(f"Error checking CSP for {url}: {e}", "ERROR")
            return None
            
    def check_xss_vulnerabilities(self, url):
        """Check for XSS vulnerabilities"""
        self.log_security(f"Checking XSS vulnerabilities for {url}")
        
        try:
            response = requests.get(url, timeout=30)
            content = response.text
            
            vulnerabilities = []
            
            # Check for common XSS patterns
            xss_patterns = [
                r'<script[^>]*>.*?</script>',
                r'javascript:',
                r'on\w+\s*=',
                r'<iframe[^>]*>',
                r'<object[^>]*>',
                r'<embed[^>]*>'
            ]
            
            for pattern in xss_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    vulnerabilities.append({
                        "type": "Potential XSS",
                        "severity": "HIGH",
                        "description": f"Found potential XSS pattern: {pattern}",
                        "matches": len(matches)
                    })
            
            # Check for reflected XSS
            test_payload = "<script>alert('XSS')</script>"
            test_response = requests.get(f"{url}?test={test_payload}", timeout=30)
            if test_payload in test_response.text:
                vulnerabilities.append({
                    "type": "Reflected XSS",
                    "severity": "CRITICAL",
                    "description": "Reflected XSS vulnerability detected"
                })
            
            return {
                "vulnerabilities": vulnerabilities,
                "score": 100 - (len(vulnerabilities) * 20)
            }
            
        except Exception as e:
            self.log_security(f"Error checking XSS for {url}: {e}", "ERROR")
            return None
            
    def check_sql_injection(self, url):
        """Check for SQL injection vulnerabilities"""
        self.log_security(f"Checking SQL injection for {url}")
        
        try:
            vulnerabilities = []
            
            # Common SQL injection payloads
            sql_payloads = [
                "' OR '1'='1",
                "'; DROP TABLE users; --",
                "' UNION SELECT * FROM users --",
                "1' OR '1'='1",
                "admin'--"
            ]
            
            for payload in sql_payloads:
                test_response = requests.get(f"{url}?id={payload}", timeout=30)
                content = test_response.text.lower()
                
                # Check for SQL error messages
                sql_errors = [
                    "sql syntax",
                    "mysql error",
                    "postgresql error",
                    "sqlite error",
                    "database error",
                    "sql error"
                ]
                
                for error in sql_errors:
                    if error in content:
                        vulnerabilities.append({
                            "type": "SQL Injection",
                            "severity": "CRITICAL",
                            "description": f"SQL injection vulnerability detected with payload: {payload}"
                        })
                        break
            
            return {
                "vulnerabilities": vulnerabilities,
                "score": 100 - (len(vulnerabilities) * 25)
            }
            
        except Exception as e:
            self.log_security(f"Error checking SQL injection for {url}: {e}", "ERROR")
            return None
            
    def check_directory_traversal(self, url):
        """Check for directory traversal vulnerabilities"""
        self.log_security(f"Checking directory traversal for {url}")
        
        try:
            vulnerabilities = []
            
            # Common directory traversal payloads
            traversal_payloads = [
                "../../../etc/passwd",
                "..\\..\\..\\windows\\system32\\drivers\\etc\\hosts",
                "....//....//....//etc/passwd",
                "%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd"
            ]
            
            for payload in traversal_payloads:
                test_response = requests.get(f"{url}?file={payload}", timeout=30)
                content = test_response.text.lower()
                
                # Check for system file contents
                system_files = [
                    "root:x:0:0:",
                    "127.0.0.1",
                    "localhost",
                    "windows",
                    "system32"
                ]
                
                for file_content in system_files:
                    if file_content in content:
                        vulnerabilities.append({
                            "type": "Directory Traversal",
                            "severity": "HIGH",
                            "description": f"Directory traversal vulnerability detected with payload: {payload}"
                        })
                        break
            
            return {
                "vulnerabilities": vulnerabilities,
                "score": 100 - (len(vulnerabilities) * 30)
            }
            
        except Exception as e:
            self.log_security(f"Error checking directory traversal for {url}: {e}", "ERROR")
            return None
            
    def run_comprehensive_scan(self, url):
        """Run comprehensive security scan"""
        self.log_security(f"Starting comprehensive security scan for {url}")
        
        start_time = datetime.now()
        scan_results = {
            "url": url,
            "timestamp": start_time.isoformat(),
            "checks": {},
            "vulnerabilities": [],
            "overall_score": 0
        }
        
        # Run all security checks
        checks = [
            ("Security Headers", self.check_security_headers),
            ("SSL Security", self.check_ssl_security),
            ("Content Security Policy", self.check_content_security_policy),
            ("XSS Vulnerabilities", self.check_xss_vulnerabilities),
            ("SQL Injection", self.check_sql_injection),
            ("Directory Traversal", self.check_directory_traversal)
        ]
        
        total_score = 0
        check_count = 0
        
        for check_name, check_func in checks:
            try:
                result = check_func(url)
                if result:
                    scan_results["checks"][check_name] = result
                    if "score" in result:
                        total_score += result["score"]
                        check_count += 1
                    if "vulnerabilities" in result:
                        scan_results["vulnerabilities"].extend(result["vulnerabilities"])
            except Exception as e:
                self.log_security(f"Error in {check_name}: {e}", "ERROR")
        
        # Calculate overall score
        scan_results["overall_score"] = total_score // check_count if check_count > 0 else 0
        
        # Save scan results
        self.save_scan_results(scan_results)
        
        # Log summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() * 1000
        
        self.log_security(f"Security scan completed for {url}")
        self.log_security(f"  Overall Score: {scan_results['overall_score']}/100")
        self.log_security(f"  Vulnerabilities Found: {len(scan_results['vulnerabilities'])}")
        self.log_security(f"  Scan Duration: {duration:.0f}ms")
        
        return scan_results
        
    def save_scan_results(self, results):
        """Save scan results to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO security_scans 
            (url, scan_type, status, vulnerabilities_found, security_score, scan_duration_ms, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            results["url"],
            "comprehensive",
            "completed",
            len(results["vulnerabilities"]),
            results["overall_score"],
            0,  # Duration will be calculated
            json.dumps(results)
        ))
        
        # Save vulnerabilities
        for vuln in results["vulnerabilities"]:
            cursor.execute('''
                INSERT INTO vulnerabilities 
                (url, vulnerability_type, severity, description, location, recommendation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                results["url"],
                vuln["type"],
                vuln["severity"],
                vuln["description"],
                vuln.get("location", ""),
                self.get_recommendation(vuln["type"])
            ))
        
        conn.commit()
        conn.close()
        
    def get_recommendation(self, vulnerability_type):
        """Get recommendation for vulnerability type"""
        recommendations = {
            "Missing security header": "Add the missing security header to your server configuration",
            "Missing CSP": "Implement a Content Security Policy header",
            "Unsafe CSP directive": "Remove unsafe directives from CSP",
            "No SSL/TLS": "Enable HTTPS and redirect HTTP traffic",
            "Invalid certificate": "Fix SSL certificate issues",
            "Weak cipher": "Use stronger cipher suites",
            "Potential XSS": "Sanitize user input and use proper encoding",
            "Reflected XSS": "Implement input validation and output encoding",
            "SQL Injection": "Use parameterized queries and input validation",
            "Directory Traversal": "Validate file paths and restrict access"
        }
        
        return recommendations.get(vulnerability_type, "Review and fix the security issue")
        
    def scan_all_targets(self):
        """Scan all configured targets"""
        targets = self.config["targets"]
        
        for name, url in targets.items():
            if url:
                self.run_comprehensive_scan(url)
                
    def generate_security_report(self, days=7):
        """Generate security report"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get recent scans
        cursor.execute('''
            SELECT * FROM security_scans 
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days))
        
        scans = cursor.fetchall()
        
        # Get active vulnerabilities
        cursor.execute('''
            SELECT * FROM vulnerabilities 
            WHERE resolved = FALSE
            ORDER BY timestamp DESC
        ''')
        
        vulnerabilities = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report = {
            "period_days": days,
            "total_scans": len(scans),
            "active_vulnerabilities": len(vulnerabilities),
            "scans": scans,
            "vulnerabilities": vulnerabilities
        }
        
        return report
        
    def start_continuous_scanning(self):
        """Start continuous security scanning"""
        self.log_security("Starting continuous security scanning")
        
        while True:
            try:
                self.scan_all_targets()
                self.log_security(f"Scanning cycle completed, sleeping for {self.config['scanning']['interval_hours']} hours")
                time.sleep(self.config["scanning"]["interval_hours"] * 3600)
            except KeyboardInterrupt:
                self.log_security("Security scanning stopped by user")
                break
            except Exception as e:
                self.log_security(f"Scanning error: {e}", "ERROR")
                time.sleep(3600)  # Wait 1 hour before retrying

def main():
    """Main function"""
    scanner = SecurityScanner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "scan":
            scanner.start_continuous_scanning()
        elif command == "check":
            scanner.scan_all_targets()
        elif command == "report":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            report = scanner.generate_security_report(days)
            print(json.dumps(report, indent=2))
        elif command == "setup":
            print("Security scanning setup complete!")
            print(f"Configuration: {scanner.config_file}")
            print(f"Database: {scanner.db_file}")
            print(f"Log file: {scanner.log_file}")
        else:
            print("Usage: python security.py [scan|check|report|setup]")
    else:
        # Default: run single check
        scanner.scan_all_targets()

if __name__ == "__main__":
    main()
