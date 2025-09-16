#!/usr/bin/env python3
"""
Verakore API Integration & Testing System
Comprehensive API testing, monitoring, and integration management
"""

import os
import sys
import json
import time
import requests
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import hashlib
import hmac
import base64
from urllib.parse import urlparse, urljoin

class APIIntegrationSystem:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "api_config.json"
        self.db_file = self.workspace_root / "api.db"
        self.log_file = self.workspace_root / "api.log"
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load API integration configuration"""
        default_config = {
            "api_integration": {
                "enabled": True,
                "test_interval_minutes": 30,
                "retention_days": 90,
                "alert_threshold_ms": 5000
            },
            "integrations": {
                "cloudflare": {
                    "enabled": True,
                    "base_url": "https://api.cloudflare.com/client/v4",
                    "api_token": "Fs6nOuqwFQYj9w_ncNDmxg6jP2HKCn7V5leGA2HN",
                    "endpoints": {
                        "zones": "/zones",
                        "dns_records": "/zones/{zone_id}/dns_records",
                        "analytics": "/zones/{zone_id}/analytics/dashboard"
                    }
                },
                "github": {
                    "enabled": True,
                    "base_url": "https://api.github.com",
                    "api_token": "",
                    "endpoints": {
                        "repos": "/repos/{owner}/{repo}",
                        "commits": "/repos/{owner}/{repo}/commits",
                        "deployments": "/repos/{owner}/{repo}/deployments"
                    }
                },
                "google_analytics": {
                    "enabled": False,
                    "base_url": "https://analyticsreporting.googleapis.com/v4",
                    "api_key": "",
                    "endpoints": {
                        "reports": "/reports:batchGet"
                    }
                },
                "slack": {
                    "enabled": False,
                    "base_url": "https://slack.com/api",
                    "webhook_url": "",
                    "endpoints": {
                        "chat_post": "/chat.postMessage",
                        "webhook": "/webhook"
                    }
                }
            },
            "testing": {
                "enabled": True,
                "test_suite": {
                    "health_checks": True,
                    "response_time": True,
                    "status_codes": True,
                    "data_validation": True,
                    "rate_limiting": True,
                    "authentication": True
                },
                "test_scenarios": {
                    "smoke_tests": True,
                    "integration_tests": True,
                    "load_tests": False,
                    "security_tests": True
                }
            },
            "monitoring": {
                "enabled": True,
                "uptime_monitoring": True,
                "response_time_monitoring": True,
                "error_rate_monitoring": True,
                "rate_limit_monitoring": True
            },
            "notifications": {
                "email": "raulmendesrosa@gmail.com",
                "slack_webhook": "",
                "enabled": True,
                "on_failure": True,
                "on_slow_response": True,
                "on_rate_limit": True
            },
            "security": {
                "api_key_rotation": False,
                "rate_limiting": True,
                "request_signing": False,
                "ssl_verification": True
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save API integration configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def init_database(self):
        """Initialize SQLite database for API data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create API tests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service_name TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                test_type TEXT NOT NULL,
                status_code INTEGER,
                response_time_ms INTEGER,
                success BOOLEAN DEFAULT FALSE,
                error_message TEXT,
                response_data TEXT
            )
        ''')
        
        # Create API monitoring table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_monitoring (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service_name TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                status_code INTEGER,
                response_time_ms INTEGER,
                success BOOLEAN DEFAULT FALSE,
                error_rate REAL DEFAULT 0,
                rate_limit_remaining INTEGER,
                rate_limit_reset DATETIME
            )
        ''')
        
        # Create API integrations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_integrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                service_name TEXT NOT NULL,
                integration_type TEXT NOT NULL,
                status TEXT NOT NULL,
                data_synced INTEGER DEFAULT 0,
                last_sync DATETIME,
                error_count INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_api(self, message, level="INFO"):
        """Log API events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def make_api_request(self, service_name, endpoint, method="GET", data=None, headers=None):
        """Make API request with error handling and monitoring"""
        try:
            service_config = self.config["integrations"][service_name]
            base_url = service_config["base_url"]
            full_url = urljoin(base_url, endpoint)
            
            # Prepare headers
            request_headers = {"Content-Type": "application/json"}
            if headers:
                request_headers.update(headers)
                
            # Add authentication
            if service_config.get("api_token"):
                if service_name == "cloudflare":
                    request_headers["Authorization"] = f"Bearer {service_config['api_token']}"
                elif service_name == "github":
                    request_headers["Authorization"] = f"token {service_config['api_token']}"
            
            start_time = time.time()
            
            # Make request
            if method.upper() == "GET":
                response = requests.get(full_url, headers=request_headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(full_url, headers=request_headers, json=data, timeout=30)
            elif method.upper() == "PUT":
                response = requests.put(full_url, headers=request_headers, json=data, timeout=30)
            elif method.upper() == "DELETE":
                response = requests.delete(full_url, headers=request_headers, timeout=30)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response_time = (time.time() - start_time) * 1000
            
            # Log request
            self.log_api(f"API Request: {method} {full_url} - {response.status_code} - {response_time:.0f}ms")
            
            # Save to monitoring database
            self.save_api_monitoring(service_name, endpoint, response.status_code, response_time, response.status_code < 400)
            
            return {
                "success": response.status_code < 400,
                "status_code": response.status_code,
                "response_time": response_time,
                "data": response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                "headers": dict(response.headers)
            }
            
        except requests.exceptions.Timeout:
            self.log_api(f"API timeout for {service_name}: {endpoint}", "ERROR")
            return {"success": False, "error": "Request timeout"}
        except requests.exceptions.ConnectionError:
            self.log_api(f"API connection error for {service_name}: {endpoint}", "ERROR")
            return {"success": False, "error": "Connection error"}
        except Exception as e:
            self.log_api(f"API error for {service_name}: {endpoint} - {e}", "ERROR")
            return {"success": False, "error": str(e)}
            
    def save_api_monitoring(self, service_name, endpoint, status_code, response_time, success):
        """Save API monitoring data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_monitoring 
            (service_name, endpoint, status_code, response_time_ms, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (service_name, endpoint, status_code, response_time, success))
        
        conn.commit()
        conn.close()
        
    def test_cloudflare_api(self):
        """Test Cloudflare API integration"""
        self.log_api("Testing Cloudflare API integration")
        
        tests = [
            {
                "name": "Token Verification",
                "endpoint": "/user/tokens/verify",
                "method": "GET"
            },
            {
                "name": "Account Info",
                "endpoint": "/accounts",
                "method": "GET"
            }
        ]
        
        results = []
        for test in tests:
            result = self.make_api_request("cloudflare", test["endpoint"], test["method"])
            results.append({
                "test_name": test["name"],
                "success": result["success"],
                "status_code": result.get("status_code"),
                "response_time": result.get("response_time"),
                "error": result.get("error")
            })
            
            # Save test result
            self.save_api_test("cloudflare", test["endpoint"], "health_check", result)
        
        return results
        
    def test_github_api(self):
        """Test GitHub API integration"""
        self.log_api("Testing GitHub API integration")
        
        tests = [
            {
                "name": "Repository Info",
                "endpoint": "/repos/raulmendesrosa-debug/verakore-website",
                "method": "GET"
            },
            {
                "name": "Recent Commits",
                "endpoint": "/repos/raulmendesrosa-debug/verakore-website/commits",
                "method": "GET"
            }
        ]
        
        results = []
        for test in tests:
            result = self.make_api_request("github", test["endpoint"], test["method"])
            results.append({
                "test_name": test["name"],
                "success": result["success"],
                "status_code": result.get("status_code"),
                "response_time": result.get("response_time"),
                "error": result.get("error")
            })
            
            # Save test result
            self.save_api_test("github", test["endpoint"], "health_check", result)
        
        return results
        
    def save_api_test(self, service_name, endpoint, test_type, result):
        """Save API test result"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO api_tests 
            (service_name, endpoint, test_type, status_code, response_time_ms, success, error_message, response_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            service_name,
            endpoint,
            test_type,
            result.get("status_code"),
            result.get("response_time"),
            result["success"],
            result.get("error"),
            json.dumps(result.get("data", {}))
        ))
        
        conn.commit()
        conn.close()
        
    def run_health_checks(self):
        """Run health checks for all integrated APIs"""
        self.log_api("Running API health checks")
        
        health_results = {}
        
        # Test Cloudflare API
        if self.config["integrations"]["cloudflare"]["enabled"]:
            health_results["cloudflare"] = self.test_cloudflare_api()
        
        # Test GitHub API
        if self.config["integrations"]["github"]["enabled"]:
            health_results["github"] = self.test_github_api()
        
        # Test other APIs
        for service_name, service_config in self.config["integrations"].items():
            if service_name not in ["cloudflare", "github"] and service_config["enabled"]:
                self.log_api(f"Testing {service_name} API", "INFO")
                # Add specific tests for other services here
        
        return health_results
        
    def monitor_api_performance(self):
        """Monitor API performance metrics"""
        self.log_api("Monitoring API performance")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get performance metrics for last hour
        cursor.execute('''
            SELECT 
                service_name,
                endpoint,
                AVG(response_time_ms) as avg_response_time,
                COUNT(*) as total_requests,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as error_count,
                MAX(response_time_ms) as max_response_time,
                MIN(response_time_ms) as min_response_time
            FROM api_monitoring 
            WHERE timestamp >= datetime('now', '-1 hour')
            GROUP BY service_name, endpoint
        ''')
        
        performance_data = cursor.fetchall()
        conn.close()
        
        # Analyze performance
        alerts = []
        for row in performance_data:
            service_name, endpoint, avg_time, total_requests, errors, max_time, min_time = row
            
            # Check for slow responses
            if avg_time > self.config["api_integration"]["alert_threshold_ms"]:
                alerts.append({
                    "type": "slow_response",
                    "service": service_name,
                    "endpoint": endpoint,
                    "avg_time": avg_time,
                    "threshold": self.config["api_integration"]["alert_threshold_ms"]
                })
            
            # Check for high error rate
            error_rate = (errors / total_requests) * 100 if total_requests > 0 else 0
            if error_rate > 10:  # 10% error rate threshold
                alerts.append({
                    "type": "high_error_rate",
                    "service": service_name,
                    "endpoint": endpoint,
                    "error_rate": error_rate
                })
        
        return {
            "performance_data": performance_data,
            "alerts": alerts
        }
        
    def generate_api_report(self, days=7):
        """Generate API integration report"""
        self.log_api(f"Generating API report for last {days} days")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get API usage statistics
        cursor.execute('''
            SELECT 
                service_name,
                COUNT(*) as total_requests,
                AVG(response_time_ms) as avg_response_time,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests,
                SUM(CASE WHEN success = 0 THEN 1 ELSE 0 END) as failed_requests,
                MAX(response_time_ms) as max_response_time
            FROM api_monitoring 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY service_name
        '''.format(days))
        
        usage_stats = cursor.fetchall()
        
        # Get test results
        cursor.execute('''
            SELECT 
                service_name,
                test_type,
                COUNT(*) as total_tests,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as passed_tests,
                AVG(response_time_ms) as avg_response_time
            FROM api_tests 
            WHERE timestamp >= datetime('now', '-{} days')
            GROUP BY service_name, test_type
        '''.format(days))
        
        test_results = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report = {
            "period_days": days,
            "usage_statistics": [
                {
                    "service": row[0],
                    "total_requests": row[1],
                    "avg_response_time": row[2],
                    "successful_requests": row[3],
                    "failed_requests": row[4],
                    "max_response_time": row[5],
                    "success_rate": (row[3] / row[1]) * 100 if row[1] > 0 else 0
                }
                for row in usage_stats
            ],
            "test_results": [
                {
                    "service": row[0],
                    "test_type": row[1],
                    "total_tests": row[2],
                    "passed_tests": row[3],
                    "avg_response_time": row[4],
                    "pass_rate": (row[3] / row[2]) * 100 if row[2] > 0 else 0
                }
                for row in test_results
            ]
        }
        
        return report
        
    def start_api_monitoring(self):
        """Start continuous API monitoring"""
        self.log_api("Starting API monitoring service")
        
        while True:
            try:
                # Run health checks
                health_results = self.run_health_checks()
                
                # Monitor performance
                performance_data = self.monitor_api_performance()
                
                # Check for alerts
                if performance_data["alerts"]:
                    self.log_api(f"API alerts detected: {len(performance_data['alerts'])}", "WARN")
                    for alert in performance_data["alerts"]:
                        self.log_api(f"Alert: {alert['type']} - {alert['service']} - {alert.get('endpoint', '')}", "WARN")
                
                interval_minutes = self.config["api_integration"]["test_interval_minutes"]
                self.log_api(f"API monitoring cycle completed, sleeping for {interval_minutes} minutes")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                self.log_api("API monitoring stopped by user")
                break
            except Exception as e:
                self.log_api(f"API monitoring error: {e}", "ERROR")
                time.sleep(300)  # Wait 5 minutes before retrying

def main():
    """Main function"""
    api_system = APIIntegrationSystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "monitor":
            api_system.start_api_monitoring()
        elif command == "test":
            results = api_system.run_health_checks()
            print(json.dumps(results, indent=2))
        elif command == "performance":
            performance = api_system.monitor_api_performance()
            print(json.dumps(performance, indent=2))
        elif command == "report":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            report = api_system.generate_api_report(days)
            print(json.dumps(report, indent=2))
        elif command == "cloudflare":
            results = api_system.test_cloudflare_api()
            print(json.dumps(results, indent=2))
        elif command == "github":
            results = api_system.test_github_api()
            print(json.dumps(results, indent=2))
        elif command == "setup":
            print("API integration system setup complete!")
            print(f"Configuration: {api_system.config_file}")
            print(f"Database: {api_system.db_file}")
            print(f"Log file: {api_system.log_file}")
        else:
            print("Usage: python api.py [monitor|test|performance|report|cloudflare|github|setup]")
    else:
        # Default: run health checks
        results = api_system.run_health_checks()
        print(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
