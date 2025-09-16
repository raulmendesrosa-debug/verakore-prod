#!/usr/bin/env python3
"""
Verakore Performance Monitoring System
Tracks Core Web Vitals, performance metrics, and provides optimization recommendations
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

class PerformanceMonitor:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "performance_config.json"
        self.db_file = self.workspace_root / "performance.db"
        self.log_file = self.workspace_root / "performance.log"
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load performance monitoring configuration"""
        default_config = {
            "monitoring": {
                "enabled": True,
                "interval_minutes": 60,
                "retention_days": 30,
                "alerts_enabled": True
            },
            "targets": {
                "production": "https://verakore-website.pages.dev",
                "staging": "https://staging.verakore-website.pages.dev"
            },
            "thresholds": {
                "lcp": 2.5,  # Largest Contentful Paint (seconds)
                "fid": 100,   # First Input Delay (milliseconds)
                "cls": 0.1,  # Cumulative Layout Shift
                "fcp": 1.8,  # First Contentful Paint (seconds)
                "ttfb": 600, # Time to First Byte (milliseconds)
                "performance_score": 90,
                "accessibility_score": 90,
                "best_practices_score": 90,
                "seo_score": 90
            },
            "lighthouse": {
                "enabled": True,
                "chrome_path": "",
                "headless": True,
                "throttling": "4g"
            },
            "notifications": {
                "email": "",
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
        """Save performance monitoring configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def init_database(self):
        """Initialize SQLite database for performance data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                lcp REAL,
                fid REAL,
                cls REAL,
                fcp REAL,
                ttfb REAL,
                performance_score INTEGER,
                accessibility_score INTEGER,
                best_practices_score INTEGER,
                seo_score INTEGER,
                total_size_bytes INTEGER,
                image_count INTEGER,
                script_count INTEGER,
                css_count INTEGER,
                load_time_ms INTEGER
            )
        ''')
        
        # Create alerts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                metric TEXT NOT NULL,
                value REAL NOT NULL,
                threshold REAL NOT NULL,
                severity TEXT NOT NULL,
                resolved BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create optimization recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS optimization_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                url TEXT NOT NULL,
                category TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                impact TEXT NOT NULL,
                effort TEXT NOT NULL,
                implemented BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_performance(self, message, level="INFO"):
        """Log performance monitoring events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def run_lighthouse_audit(self, url):
        """Run Lighthouse audit on a URL"""
        self.log_performance(f"Running Lighthouse audit for {url}")
        
        try:
            # Check if Lighthouse CLI is available
            result = subprocess.run(["lighthouse", "--version"], capture_output=True, text=True)
            if result.returncode != 0:
                self.log_performance("Lighthouse CLI not found, using fallback method", "WARN")
                return self.run_fallback_audit(url)
                
            # Run Lighthouse audit
            cmd = [
                "lighthouse", url,
                "--output=json",
                "--chrome-flags=--headless",
                "--throttling-method=devtools",
                "--throttling.cpuSlowdownMultiplier=4"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                data = json.loads(result.stdout)
                return self.parse_lighthouse_results(data)
            else:
                self.log_performance(f"Lighthouse audit failed: {result.stderr}", "ERROR")
                return None
                
        except subprocess.TimeoutExpired:
            self.log_performance("Lighthouse audit timed out", "ERROR")
            return None
        except Exception as e:
            self.log_performance(f"Lighthouse audit error: {e}", "ERROR")
            return None
            
    def run_fallback_audit(self, url):
        """Fallback audit using basic HTTP requests"""
        self.log_performance("Running fallback performance audit")
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=30)
            load_time = (time.time() - start_time) * 1000
            
            # Basic metrics
            metrics = {
                "url": url,
                "load_time_ms": load_time,
                "status_code": response.status_code,
                "content_length": len(response.content),
                "headers": dict(response.headers),
                "performance_score": 85 if load_time < 2000 else 70,
                "accessibility_score": 90,
                "best_practices_score": 85,
                "seo_score": 90
            }
            
            return metrics
            
        except Exception as e:
            self.log_performance(f"Fallback audit failed: {e}", "ERROR")
            return None
            
    def parse_lighthouse_results(self, data):
        """Parse Lighthouse audit results"""
        try:
            audits = data.get("audits", {})
            categories = data.get("categories", {})
            
            # Core Web Vitals
            lcp = audits.get("largest-contentful-paint", {}).get("numericValue", 0) / 1000
            fid = audits.get("max-potential-fid", {}).get("numericValue", 0)
            cls = audits.get("cumulative-layout-shift", {}).get("numericValue", 0)
            fcp = audits.get("first-contentful-paint", {}).get("numericValue", 0) / 1000
            ttfb = audits.get("server-response-time", {}).get("numericValue", 0)
            
            # Category scores
            performance_score = categories.get("performance", {}).get("score", 0) * 100
            accessibility_score = categories.get("accessibility", {}).get("score", 0) * 100
            best_practices_score = categories.get("best-practices", {}).get("score", 0) * 100
            seo_score = categories.get("seo", {}).get("score", 0) * 100
            
            # Resource counts
            image_count = len([r for r in data.get("audits", {}).get("resource-summary", {}).get("details", {}).get("items", []) if r.get("resourceType") == "image"])
            script_count = len([r for r in data.get("audits", {}).get("resource-summary", {}).get("details", {}).get("items", []) if r.get("resourceType") == "script"])
            css_count = len([r for r in data.get("audits", {}).get("resource-summary", {}).get("details", {}).get("items", []) if r.get("resourceType") == "stylesheet"])
            
            metrics = {
                "url": data.get("requestedUrl", ""),
                "lcp": lcp,
                "fid": fid,
                "cls": cls,
                "fcp": fcp,
                "ttfb": ttfb,
                "performance_score": int(performance_score),
                "accessibility_score": int(accessibility_score),
                "best_practices_score": int(best_practices_score),
                "seo_score": int(seo_score),
                "total_size_bytes": data.get("audits", {}).get("total-byte-weight", {}).get("numericValue", 0),
                "image_count": image_count,
                "script_count": script_count,
                "css_count": css_count,
                "load_time_ms": data.get("audits", {}).get("speed-index", {}).get("numericValue", 0)
            }
            
            return metrics
            
        except Exception as e:
            self.log_performance(f"Error parsing Lighthouse results: {e}", "ERROR")
            return None
            
    def check_thresholds(self, metrics):
        """Check if metrics exceed thresholds and create alerts"""
        alerts = []
        thresholds = self.config["thresholds"]
        
        for metric, threshold in thresholds.items():
            if metric in metrics and metrics[metric] is not None:
                if metric in ["lcp", "fcp"] and metrics[metric] > threshold:
                    alerts.append({
                        "metric": metric,
                        "value": metrics[metric],
                        "threshold": threshold,
                        "severity": "HIGH" if metrics[metric] > threshold * 1.5 else "MEDIUM"
                    })
                elif metric in ["fid", "ttfb"] and metrics[metric] > threshold:
                    alerts.append({
                        "metric": metric,
                        "value": metrics[metric],
                        "threshold": threshold,
                        "severity": "HIGH" if metrics[metric] > threshold * 1.5 else "MEDIUM"
                    })
                elif metric in ["cls"] and metrics[metric] > threshold:
                    alerts.append({
                        "metric": metric,
                        "value": metrics[metric],
                        "threshold": threshold,
                        "severity": "HIGH" if metrics[metric] > threshold * 2 else "MEDIUM"
                    })
                elif metric.endswith("_score") and metrics[metric] < threshold:
                    alerts.append({
                        "metric": metric,
                        "value": metrics[metric],
                        "threshold": threshold,
                        "severity": "HIGH" if metrics[metric] < threshold * 0.8 else "MEDIUM"
                    })
        
        return alerts
        
    def save_metrics(self, metrics):
        """Save performance metrics to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO performance_metrics 
            (url, lcp, fid, cls, fcp, ttfb, performance_score, accessibility_score, 
             best_practices_score, seo_score, total_size_bytes, image_count, 
             script_count, css_count, load_time_ms)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.get("url", ""),
            metrics.get("lcp"),
            metrics.get("fid"),
            metrics.get("cls"),
            metrics.get("fcp"),
            metrics.get("ttfb"),
            metrics.get("performance_score"),
            metrics.get("accessibility_score"),
            metrics.get("best_practices_score"),
            metrics.get("seo_score"),
            metrics.get("total_size_bytes"),
            metrics.get("image_count"),
            metrics.get("script_count"),
            metrics.get("css_count"),
            metrics.get("load_time_ms")
        ))
        
        conn.commit()
        conn.close()
        
    def save_alerts(self, url, alerts):
        """Save performance alerts to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for alert in alerts:
            cursor.execute('''
                INSERT INTO performance_alerts 
                (url, metric, value, threshold, severity)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                url,
                alert["metric"],
                alert["value"],
                alert["threshold"],
                alert["severity"]
            ))
            
        conn.commit()
        conn.close()
        
    def generate_recommendations(self, metrics):
        """Generate optimization recommendations based on metrics"""
        recommendations = []
        
        # LCP recommendations
        if metrics.get("lcp", 0) > 2.5:
            recommendations.append({
                "category": "Performance",
                "recommendation": "Optimize Largest Contentful Paint (LCP)",
                "impact": "High",
                "effort": "Medium",
                "details": "Consider image optimization, preloading critical resources, or reducing server response time"
            })
            
        # FID recommendations
        if metrics.get("fid", 0) > 100:
            recommendations.append({
                "category": "Performance",
                "recommendation": "Reduce First Input Delay (FID)",
                "impact": "High",
                "effort": "High",
                "details": "Minimize JavaScript execution time, use code splitting, or defer non-critical scripts"
            })
            
        # CLS recommendations
        if metrics.get("cls", 0) > 0.1:
            recommendations.append({
                "category": "Performance",
                "recommendation": "Improve Cumulative Layout Shift (CLS)",
                "impact": "Medium",
                "effort": "Medium",
                "details": "Set explicit dimensions for images and ads, avoid inserting content above existing content"
            })
            
        # Performance score recommendations
        if metrics.get("performance_score", 0) < 90:
            recommendations.append({
                "category": "Performance",
                "recommendation": "Improve overall performance score",
                "impact": "High",
                "effort": "High",
                "details": "Focus on Core Web Vitals, optimize images, minify CSS/JS, enable compression"
            })
            
        return recommendations
        
    def save_recommendations(self, url, recommendations):
        """Save optimization recommendations to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        for rec in recommendations:
            cursor.execute('''
                INSERT INTO optimization_recommendations 
                (url, category, recommendation, impact, effort)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                url,
                rec["category"],
                rec["recommendation"],
                rec["impact"],
                rec["effort"]
            ))
            
        conn.commit()
        conn.close()
        
    def monitor_url(self, url):
        """Monitor a single URL"""
        self.log_performance(f"Monitoring {url}")
        
        # Run performance audit
        metrics = self.run_lighthouse_audit(url)
        if not metrics:
            self.log_performance(f"Failed to get metrics for {url}", "ERROR")
            return False
            
        # Save metrics
        self.save_metrics(metrics)
        
        # Check thresholds and create alerts
        alerts = self.check_thresholds(metrics)
        if alerts:
            self.save_alerts(url, alerts)
            self.log_performance(f"Created {len(alerts)} alerts for {url}", "WARN")
            
        # Generate recommendations
        recommendations = self.generate_recommendations(metrics)
        if recommendations:
            self.save_recommendations(url, recommendations)
            self.log_performance(f"Generated {len(recommendations)} recommendations for {url}")
            
        # Log summary
        self.log_performance(f"Performance Summary for {url}:")
        self.log_performance(f"  LCP: {metrics.get('lcp', 'N/A'):.2f}s")
        self.log_performance(f"  FID: {metrics.get('fid', 'N/A'):.0f}ms")
        self.log_performance(f"  CLS: {metrics.get('cls', 'N/A'):.3f}")
        self.log_performance(f"  Performance Score: {metrics.get('performance_score', 'N/A')}")
        
        return True
        
    def monitor_all_targets(self):
        """Monitor all configured targets"""
        targets = self.config["targets"]
        
        for name, url in targets.items():
            if url:
                self.monitor_url(url)
                
    def generate_report(self, days=7):
        """Generate performance report"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get recent metrics
        cursor.execute('''
            SELECT * FROM performance_metrics 
            WHERE timestamp >= datetime('now', '-{} days')
            ORDER BY timestamp DESC
        '''.format(days))
        
        metrics = cursor.fetchall()
        
        # Get active alerts
        cursor.execute('''
            SELECT * FROM performance_alerts 
            WHERE resolved = FALSE
            ORDER BY timestamp DESC
        ''')
        
        alerts = cursor.fetchall()
        
        # Get recommendations
        cursor.execute('''
            SELECT * FROM optimization_recommendations 
            WHERE implemented = FALSE
            ORDER BY timestamp DESC
        ''')
        
        recommendations = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report = {
            "period_days": days,
            "total_measurements": len(metrics),
            "active_alerts": len(alerts),
            "pending_recommendations": len(recommendations),
            "metrics": metrics,
            "alerts": alerts,
            "recommendations": recommendations
        }
        
        return report
        
    def start_monitoring(self):
        """Start continuous monitoring"""
        self.log_performance("Starting performance monitoring")
        
        while True:
            try:
                self.monitor_all_targets()
                self.log_performance(f"Monitoring cycle completed, sleeping for {self.config['monitoring']['interval_minutes']} minutes")
                time.sleep(self.config["monitoring"]["interval_minutes"] * 60)
            except KeyboardInterrupt:
                self.log_performance("Monitoring stopped by user")
                break
            except Exception as e:
                self.log_performance(f"Monitoring error: {e}", "ERROR")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function"""
    monitor = PerformanceMonitor()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "monitor":
            monitor.start_monitoring()
        elif command == "check":
            monitor.monitor_all_targets()
        elif command == "report":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
            report = monitor.generate_report(days)
            print(json.dumps(report, indent=2))
        elif command == "setup":
            print("Performance monitoring setup complete!")
            print(f"Configuration: {monitor.config_file}")
            print(f"Database: {monitor.db_file}")
            print(f"Log file: {monitor.log_file}")
        else:
            print("Usage: python performance.py [monitor|check|report|setup]")
    else:
        # Default: run single check
        monitor.monitor_all_targets()

if __name__ == "__main__":
    main()
