#!/usr/bin/env python3
"""
Verakore Analytics & Reporting System
Comprehensive business intelligence and user behavior analytics
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
import re
from collections import defaultdict, Counter

class AnalyticsEngine:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "analytics_config.json"
        self.db_file = self.workspace_root / "analytics.db"
        self.log_file = self.workspace_root / "analytics.log"
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load analytics configuration"""
        default_config = {
            "analytics": {
                "enabled": True,
                "collection_interval_minutes": 15,
                "retention_days": 365,
                "real_time_enabled": True
            },
            "data_sources": {
                "website_analytics": {
                    "enabled": True,
                    "page_views": True,
                    "user_sessions": True,
                    "bounce_rate": True,
                    "conversion_tracking": True
                },
                "performance_metrics": {
                    "enabled": True,
                    "core_web_vitals": True,
                    "page_load_times": True,
                    "resource_metrics": True
                },
                "business_metrics": {
                    "enabled": True,
                    "lead_generation": True,
                    "contact_form_submissions": True,
                    "service_inquiries": True,
                    "conversion_funnels": True
                },
                "user_behavior": {
                    "enabled": True,
                    "click_tracking": True,
                    "scroll_depth": True,
                    "time_on_page": True,
                    "exit_pages": True
                }
            },
            "tracking": {
                "google_analytics": {
                    "enabled": False,
                    "tracking_id": "",
                    "measurement_id": ""
                },
                "custom_analytics": {
                    "enabled": True,
                    "privacy_compliant": True,
                    "cookie_consent": True
                }
            },
            "reports": {
                "daily_summary": True,
                "weekly_report": True,
                "monthly_analysis": True,
                "quarterly_review": True,
                "custom_reports": True
            },
            "kpis": {
                "website_traffic": {
                    "page_views": True,
                    "unique_visitors": True,
                    "session_duration": True,
                    "bounce_rate": True
                },
                "business_metrics": {
                    "lead_generation": True,
                    "conversion_rate": True,
                    "contact_submissions": True,
                    "service_inquiries": True
                },
                "performance_metrics": {
                    "page_load_time": True,
                    "core_web_vitals": True,
                    "mobile_performance": True,
                    "seo_score": True
                }
            },
            "notifications": {
                "email": "raulmendesrosa@gmail.com",
                "slack_webhook": "",
                "enabled": True,
                "daily_summary": True,
                "weekly_report": True,
                "alert_thresholds": True
            },
            "privacy": {
                "gdpr_compliant": True,
                "data_anonymization": True,
                "retention_policy": True,
                "consent_management": True
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save analytics configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def init_database(self):
        """Initialize SQLite database for analytics data"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create page views table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS page_views (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                page_url TEXT NOT NULL,
                page_title TEXT,
                referrer TEXT,
                user_agent TEXT,
                ip_address TEXT,
                session_id TEXT,
                user_id TEXT,
                country TEXT,
                city TEXT,
                device_type TEXT,
                browser TEXT,
                os TEXT
            )
        ''')
        
        # Create user sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT UNIQUE NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                duration_seconds INTEGER DEFAULT 0,
                page_views INTEGER DEFAULT 0,
                bounce BOOLEAN DEFAULT FALSE,
                conversion BOOLEAN DEFAULT FALSE,
                referrer TEXT,
                landing_page TEXT,
                exit_page TEXT,
                user_id TEXT,
                country TEXT,
                device_type TEXT
            )
        ''')
        
        # Create business events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS business_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                event_name TEXT NOT NULL,
                page_url TEXT,
                session_id TEXT,
                user_id TEXT,
                event_data TEXT,
                conversion_value REAL DEFAULT 0
            )
        ''')
        
        # Create performance metrics table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                page_url TEXT NOT NULL,
                load_time_ms INTEGER,
                lcp REAL,
                fid REAL,
                cls REAL,
                fcp REAL,
                ttfb REAL,
                performance_score INTEGER,
                mobile_score INTEGER,
                seo_score INTEGER,
                session_id TEXT
            )
        ''')
        
        # Create analytics reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS analytics_reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                report_type TEXT NOT NULL,
                period_start DATETIME NOT NULL,
                period_end DATETIME NOT NULL,
                report_data TEXT NOT NULL,
                generated_by TEXT DEFAULT 'system'
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_analytics(self, message, level="INFO"):
        """Log analytics events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def track_page_view(self, page_url, page_title="", referrer="", user_agent="", ip_address="", session_id="", user_id=""):
        """Track a page view"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            # Extract device and browser info
            device_type = self.detect_device_type(user_agent)
            browser = self.detect_browser(user_agent)
            os_info = self.detect_os(user_agent)
            
            cursor.execute('''
                INSERT INTO page_views 
                (page_url, page_title, referrer, user_agent, ip_address, session_id, user_id, device_type, browser, os)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                page_url, page_title, referrer, user_agent, ip_address, session_id, user_id, device_type, browser, os_info
            ))
            
            conn.commit()
            conn.close()
            
            self.log_analytics(f"Page view tracked: {page_url}")
            return True
            
        except Exception as e:
            self.log_analytics(f"Error tracking page view: {e}", "ERROR")
            return False
            
    def track_business_event(self, event_type, event_name, page_url="", session_id="", user_id="", event_data="", conversion_value=0):
        """Track a business event"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO business_events 
                (event_type, event_name, page_url, session_id, user_id, event_data, conversion_value)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_type, event_name, page_url, session_id, user_id, json.dumps(event_data), conversion_value
            ))
            
            conn.commit()
            conn.close()
            
            self.log_analytics(f"Business event tracked: {event_type} - {event_name}")
            return True
            
        except Exception as e:
            self.log_analytics(f"Error tracking business event: {e}", "ERROR")
            return False
            
    def track_performance_metric(self, page_url, load_time_ms, lcp=None, fid=None, cls=None, fcp=None, ttfb=None, performance_score=None, session_id=""):
        """Track performance metrics"""
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO performance_metrics 
                (page_url, load_time_ms, lcp, fid, cls, fcp, ttfb, performance_score, session_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                page_url, load_time_ms, lcp, fid, cls, fcp, ttfb, performance_score, session_id
            ))
            
            conn.commit()
            conn.close()
            
            self.log_analytics(f"Performance metric tracked: {page_url} - {load_time_ms}ms")
            return True
            
        except Exception as e:
            self.log_analytics(f"Error tracking performance metric: {e}", "ERROR")
            return False
            
    def detect_device_type(self, user_agent):
        """Detect device type from user agent"""
        if not user_agent:
            return "Unknown"
            
        user_agent_lower = user_agent.lower()
        
        if any(mobile in user_agent_lower for mobile in ['mobile', 'android', 'iphone', 'ipad', 'tablet']):
            return "Mobile"
        elif 'tablet' in user_agent_lower:
            return "Tablet"
        else:
            return "Desktop"
            
    def detect_browser(self, user_agent):
        """Detect browser from user agent"""
        if not user_agent:
            return "Unknown"
            
        user_agent_lower = user_agent.lower()
        
        if 'chrome' in user_agent_lower:
            return "Chrome"
        elif 'firefox' in user_agent_lower:
            return "Firefox"
        elif 'safari' in user_agent_lower:
            return "Safari"
        elif 'edge' in user_agent_lower:
            return "Edge"
        elif 'opera' in user_agent_lower:
            return "Opera"
        else:
            return "Other"
            
    def detect_os(self, user_agent):
        """Detect operating system from user agent"""
        if not user_agent:
            return "Unknown"
            
        user_agent_lower = user_agent.lower()
        
        if 'windows' in user_agent_lower:
            return "Windows"
        elif 'mac' in user_agent_lower:
            return "macOS"
        elif 'linux' in user_agent_lower:
            return "Linux"
        elif 'android' in user_agent_lower:
            return "Android"
        elif 'ios' in user_agent_lower:
            return "iOS"
        else:
            return "Other"
            
    def generate_daily_report(self, date=None):
        """Generate daily analytics report"""
        if date is None:
            date = datetime.now().date()
            
        self.log_analytics(f"Generating daily report for {date}")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get page views for the day
        cursor.execute('''
            SELECT COUNT(*) as page_views, COUNT(DISTINCT session_id) as unique_sessions
            FROM page_views 
            WHERE DATE(timestamp) = ?
        ''', (date,))
        
        page_stats = cursor.fetchone()
        
        # Get top pages
        cursor.execute('''
            SELECT page_url, COUNT(*) as views
            FROM page_views 
            WHERE DATE(timestamp) = ?
            GROUP BY page_url
            ORDER BY views DESC
            LIMIT 10
        ''', (date,))
        
        top_pages = cursor.fetchall()
        
        # Get device breakdown
        cursor.execute('''
            SELECT device_type, COUNT(*) as count
            FROM page_views 
            WHERE DATE(timestamp) = ?
            GROUP BY device_type
        ''', (date,))
        
        device_breakdown = cursor.fetchall()
        
        # Get business events
        cursor.execute('''
            SELECT event_type, COUNT(*) as count
            FROM business_events 
            WHERE DATE(timestamp) = ?
            GROUP BY event_type
        ''', (date,))
        
        business_events = cursor.fetchall()
        
        conn.close()
        
        # Generate report
        report = {
            "date": str(date),
            "page_views": page_stats[0] if page_stats else 0,
            "unique_sessions": page_stats[1] if page_stats else 0,
            "top_pages": [{"url": page[0], "views": page[1]} for page in top_pages],
            "device_breakdown": [{"device": device[0], "count": device[1]} for device in device_breakdown],
            "business_events": [{"type": event[0], "count": event[1]} for event in business_events]
        }
        
        # Save report
        self.save_report("daily", report, date, date)
        
        return report
        
    def generate_weekly_report(self, week_start=None):
        """Generate weekly analytics report"""
        if week_start is None:
            week_start = datetime.now().date() - timedelta(days=7)
            
        week_end = week_start + timedelta(days=6)
        
        self.log_analytics(f"Generating weekly report for {week_start} to {week_end}")
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Get weekly stats
        cursor.execute('''
            SELECT 
                COUNT(*) as page_views,
                COUNT(DISTINCT session_id) as unique_sessions,
                AVG(duration_seconds) as avg_session_duration
            FROM page_views pv
            LEFT JOIN user_sessions us ON pv.session_id = us.session_id
            WHERE DATE(pv.timestamp) BETWEEN ? AND ?
        ''', (week_start, week_end))
        
        weekly_stats = cursor.fetchone()
        
        # Get daily breakdown
        cursor.execute('''
            SELECT DATE(timestamp) as date, COUNT(*) as page_views
            FROM page_views 
            WHERE DATE(timestamp) BETWEEN ? AND ?
            GROUP BY DATE(timestamp)
            ORDER BY date
        ''', (week_start, week_end))
        
        daily_breakdown = cursor.fetchall()
        
        # Get conversion metrics
        cursor.execute('''
            SELECT COUNT(*) as conversions, SUM(conversion_value) as total_value
            FROM business_events 
            WHERE DATE(timestamp) BETWEEN ? AND ? AND conversion_value > 0
        ''', (week_start, week_end))
        
        conversion_stats = cursor.fetchone()
        
        conn.close()
        
        # Generate report
        report = {
            "period_start": str(week_start),
            "period_end": str(week_end),
            "page_views": weekly_stats[0] if weekly_stats else 0,
            "unique_sessions": weekly_stats[1] if weekly_stats else 0,
            "avg_session_duration": weekly_stats[2] if weekly_stats else 0,
            "daily_breakdown": [{"date": str(day[0]), "page_views": day[1]} for day in daily_breakdown],
            "conversions": conversion_stats[0] if conversion_stats else 0,
            "conversion_value": conversion_stats[1] if conversion_stats else 0
        }
        
        # Save report
        self.save_report("weekly", report, week_start, week_end)
        
        return report
        
    def save_report(self, report_type, report_data, period_start, period_end):
        """Save analytics report to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO analytics_reports 
            (report_type, period_start, period_end, report_data)
            VALUES (?, ?, ?, ?)
        ''', (
            report_type,
            period_start,
            period_end,
            json.dumps(report_data)
        ))
        
        conn.commit()
        conn.close()
        
    def get_kpi_metrics(self, days=30):
        """Get KPI metrics for the specified period"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Website traffic KPIs
        cursor.execute('''
            SELECT 
                COUNT(*) as total_page_views,
                COUNT(DISTINCT session_id) as unique_visitors,
                COUNT(DISTINCT DATE(timestamp)) as active_days
            FROM page_views 
            WHERE DATE(timestamp) BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        traffic_kpis = cursor.fetchone()
        
        # Business KPIs
        cursor.execute('''
            SELECT 
                COUNT(*) as total_events,
                COUNT(CASE WHEN conversion_value > 0 THEN 1 END) as conversions,
                SUM(conversion_value) as total_conversion_value
            FROM business_events 
            WHERE DATE(timestamp) BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        business_kpis = cursor.fetchone()
        
        # Performance KPIs
        cursor.execute('''
            SELECT 
                AVG(load_time_ms) as avg_load_time,
                AVG(performance_score) as avg_performance_score,
                COUNT(*) as performance_samples
            FROM performance_metrics 
            WHERE DATE(timestamp) BETWEEN ? AND ?
        ''', (start_date, end_date))
        
        performance_kpis = cursor.fetchone()
        
        conn.close()
        
        return {
            "period_days": days,
            "website_traffic": {
                "total_page_views": traffic_kpis[0] if traffic_kpis else 0,
                "unique_visitors": traffic_kpis[1] if traffic_kpis else 0,
                "active_days": traffic_kpis[2] if traffic_kpis else 0
            },
            "business_metrics": {
                "total_events": business_kpis[0] if business_kpis else 0,
                "conversions": business_kpis[1] if business_kpis else 0,
                "conversion_value": business_kpis[2] if business_kpis else 0
            },
            "performance_metrics": {
                "avg_load_time": performance_kpis[0] if performance_kpis else 0,
                "avg_performance_score": performance_kpis[1] if performance_kpis else 0,
                "samples": performance_kpis[2] if performance_kpis else 0
            }
        }
        
    def start_analytics_collection(self):
        """Start continuous analytics collection"""
        self.log_analytics("Starting analytics collection service")
        
        while True:
            try:
                # Generate daily report if it's a new day
                current_date = datetime.now().date()
                if not self.has_daily_report(current_date):
                    self.generate_daily_report(current_date)
                
                # Generate weekly report if it's Monday
                if datetime.now().weekday() == 0:  # Monday
                    week_start = current_date - timedelta(days=7)
                    if not self.has_weekly_report(week_start):
                        self.generate_weekly_report(week_start)
                
                interval_minutes = self.config["analytics"]["collection_interval_minutes"]
                self.log_analytics(f"Analytics collection cycle completed, sleeping for {interval_minutes} minutes")
                time.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                self.log_analytics("Analytics collection stopped by user")
                break
            except Exception as e:
                self.log_analytics(f"Analytics collection error: {e}", "ERROR")
                time.sleep(300)  # Wait 5 minutes before retrying
                
    def has_daily_report(self, date):
        """Check if daily report exists for date"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM analytics_reports 
            WHERE report_type = 'daily' AND DATE(period_start) = ?
        ''', (date,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0
        
    def has_weekly_report(self, week_start):
        """Check if weekly report exists for week"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) FROM analytics_reports 
            WHERE report_type = 'weekly' AND DATE(period_start) = ?
        ''', (week_start,))
        
        count = cursor.fetchone()[0]
        conn.close()
        
        return count > 0

def main():
    """Main function"""
    analytics = AnalyticsEngine()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "collect":
            analytics.start_analytics_collection()
        elif command == "daily":
            report = analytics.generate_daily_report()
            print(json.dumps(report, indent=2))
        elif command == "weekly":
            report = analytics.generate_weekly_report()
            print(json.dumps(report, indent=2))
        elif command == "kpis":
            days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            kpis = analytics.get_kpi_metrics(days)
            print(json.dumps(kpis, indent=2))
        elif command == "track":
            if len(sys.argv) > 2:
                page_url = sys.argv[2]
                analytics.track_page_view(page_url)
            else:
                print("Usage: python analytics.py track <page_url>")
        elif command == "event":
            if len(sys.argv) > 3:
                event_type = sys.argv[2]
                event_name = sys.argv[3]
                analytics.track_business_event(event_type, event_name)
            else:
                print("Usage: python analytics.py event <event_type> <event_name>")
        elif command == "setup":
            print("Analytics system setup complete!")
            print(f"Configuration: {analytics.config_file}")
            print(f"Database: {analytics.db_file}")
            print(f"Log file: {analytics.log_file}")
        else:
            print("Usage: python analytics.py [collect|daily|weekly|kpis|track|event|setup]")
    else:
        # Default: generate daily report
        report = analytics.generate_daily_report()
        print(json.dumps(report, indent=2))

if __name__ == "__main__":
    main()
