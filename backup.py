#!/usr/bin/env python3
"""
Verakore Backup & Disaster Recovery System
Comprehensive backup solution with automated recovery capabilities
"""

import os
import sys
import json
import shutil
import zipfile
import hashlib
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import sqlite3
import tarfile
import gzip

class BackupRecoverySystem:
    def __init__(self):
        self.workspace_root = Path.cwd()
        self.config_file = self.workspace_root / "backup_config.json"
        self.db_file = self.workspace_root / "backup.db"
        self.log_file = self.workspace_root / "backup.log"
        self.load_config()
        self.init_database()
        
    def load_config(self):
        """Load backup configuration"""
        default_config = {
            "backup": {
                "enabled": True,
                "interval_hours": 24,
                "retention_days": 30,
                "compression": True,
                "encryption": False,
                "verify_backups": True
            },
            "backup_locations": {
                "local": "./backups",
                "cloud": "",
                "network": ""
            },
            "backup_types": {
                "full": {
                    "enabled": True,
                    "interval_days": 7,
                    "include_files": True,
                    "include_database": True,
                    "include_config": True
                },
                "incremental": {
                    "enabled": True,
                    "interval_hours": 6,
                    "include_files": True,
                    "include_database": True
                },
                "differential": {
                    "enabled": True,
                    "interval_hours": 12,
                    "include_files": True,
                    "include_database": True
                }
            },
            "backup_sources": {
                "website_files": [
                    "*.html",
                    "*.css",
                    "*.js",
                    "*.json",
                    "*.md",
                    "*.py",
                    "*.bat",
                    "*.ps1",
                    "*.sh",
                    "assets/",
                    "tools/"
                ],
                "configuration_files": [
                    "*.config.json",
                    "*.toml",
                    "_headers",
                    ".github/"
                ],
                "database_files": [
                    "*.db",
                    "*.sqlite",
                    "*.sqlite3"
                ],
                "log_files": [
                    "*.log"
                ]
            },
            "exclude_patterns": [
                "node_modules/",
                ".git/",
                "__pycache__/",
                "*.pyc",
                "*.pyo",
                ".DS_Store",
                "Thumbs.db",
                "*.tmp",
                "*.temp"
            ],
            "recovery": {
                "enabled": True,
                "test_restore": True,
                "recovery_time_objective": 4,
                "recovery_point_objective": 1
            },
            "notifications": {
                "email": "raulmendesrosa@gmail.com",
                "slack_webhook": "",
                "enabled": True,
                "on_success": True,
                "on_failure": True,
                "on_recovery": True
            },
            "cloud_storage": {
                "enabled": False,
                "provider": "aws_s3",
                "bucket_name": "",
                "access_key": "",
                "secret_key": "",
                "region": "us-east-1"
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = default_config
            self.save_config()
            
    def save_config(self):
        """Save backup configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
            
    def init_database(self):
        """Initialize SQLite database for backup tracking"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        # Create backup records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                backup_type TEXT NOT NULL,
                backup_path TEXT NOT NULL,
                backup_size_bytes INTEGER DEFAULT 0,
                file_count INTEGER DEFAULT 0,
                status TEXT NOT NULL,
                duration_ms INTEGER DEFAULT 0,
                checksum TEXT,
                details TEXT
            )
        ''')
        
        # Create recovery records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recovery_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                recovery_type TEXT NOT NULL,
                source_backup TEXT NOT NULL,
                target_path TEXT NOT NULL,
                status TEXT NOT NULL,
                duration_ms INTEGER DEFAULT 0,
                files_restored INTEGER DEFAULT 0,
                details TEXT
            )
        ''')
        
        # Create backup verification table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS backup_verification (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                backup_id INTEGER NOT NULL,
                verification_status TEXT NOT NULL,
                checksum_match BOOLEAN DEFAULT FALSE,
                file_integrity BOOLEAN DEFAULT FALSE,
                details TEXT,
                FOREIGN KEY (backup_id) REFERENCES backup_records (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def log_backup(self, message, level="INFO"):
        """Log backup events"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}\n"
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)
            
        print(f"[{level}] {message}")
        
    def create_backup_directory(self):
        """Create backup directory structure"""
        backup_dir = Path(self.config["backup_locations"]["local"])
        backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        (backup_dir / "full").mkdir(exist_ok=True)
        (backup_dir / "incremental").mkdir(exist_ok=True)
        (backup_dir / "differential").mkdir(exist_ok=True)
        (backup_dir / "verification").mkdir(exist_ok=True)
        
        return backup_dir
        
    def get_files_to_backup(self):
        """Get list of files to backup based on configuration"""
        files_to_backup = []
        
        for category, patterns in self.config["backup_sources"].items():
            for pattern in patterns:
                if pattern.endswith('/'):
                    # Directory pattern
                    dir_path = Path(pattern[:-1])
                    if dir_path.exists():
                        for file_path in dir_path.rglob('*'):
                            if file_path.is_file():
                                files_to_backup.append(file_path)
                else:
                    # File pattern
                    for file_path in self.workspace_root.glob(pattern):
                        if file_path.is_file():
                            files_to_backup.append(file_path)
        
        # Filter out excluded patterns
        filtered_files = []
        for file_path in files_to_backup:
            should_exclude = False
            for exclude_pattern in self.config["exclude_patterns"]:
                if exclude_pattern.replace('/', os.sep) in str(file_path):
                    should_exclude = True
                    break
            if not should_exclude:
                filtered_files.append(file_path)
        
        return filtered_files
        
    def calculate_checksum(self, file_path):
        """Calculate MD5 checksum of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            self.log_backup(f"Error calculating checksum for {file_path}: {e}", "ERROR")
            return None
            
    def create_backup_archive(self, files_to_backup, backup_path, backup_type):
        """Create backup archive"""
        self.log_backup(f"Creating {backup_type} backup archive: {backup_path}")
        
        start_time = time.time()
        file_count = 0
        total_size = 0
        
        try:
            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for file_path in files_to_backup:
                        try:
                            # Calculate relative path
                            rel_path = file_path.relative_to(self.workspace_root)
                            zipf.write(file_path, rel_path)
                            file_count += 1
                            total_size += file_path.stat().st_size
                        except Exception as e:
                            self.log_backup(f"Error adding {file_path} to backup: {e}", "WARN")
                            
            elif backup_path.suffix == '.tar.gz':
                with tarfile.open(backup_path, 'w:gz') as tarf:
                    for file_path in files_to_backup:
                        try:
                            rel_path = file_path.relative_to(self.workspace_root)
                            tarf.add(file_path, arcname=rel_path)
                            file_count += 1
                            total_size += file_path.stat().st_size
                        except Exception as e:
                            self.log_backup(f"Error adding {file_path} to backup: {e}", "WARN")
            
            duration = (time.time() - start_time) * 1000
            
            self.log_backup(f"Backup archive created successfully")
            self.log_backup(f"  Files: {file_count}")
            self.log_backup(f"  Size: {total_size / 1024 / 1024:.2f} MB")
            self.log_backup(f"  Duration: {duration:.0f}ms")
            
            return {
                "file_count": file_count,
                "total_size": total_size,
                "duration": duration,
                "status": "SUCCESS"
            }
            
        except Exception as e:
            self.log_backup(f"Error creating backup archive: {e}", "ERROR")
            return {
                "file_count": 0,
                "total_size": 0,
                "duration": 0,
                "status": "FAILED"
            }
            
    def verify_backup(self, backup_path):
        """Verify backup integrity"""
        if not self.config["backup"]["verify_backups"]:
            return True
            
        self.log_backup(f"Verifying backup: {backup_path}")
        
        try:
            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    # Test zip file integrity
                    zipf.testzip()
                    
            elif backup_path.suffix == '.tar.gz':
                with tarfile.open(backup_path, 'r:gz') as tarf:
                    # Test tar file integrity
                    tarf.getmembers()
            
            self.log_backup("Backup verification successful")
            return True
            
        except Exception as e:
            self.log_backup(f"Backup verification failed: {e}", "ERROR")
            return False
            
    def save_backup_record(self, backup_type, backup_path, backup_info, checksum):
        """Save backup record to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO backup_records 
            (backup_type, backup_path, backup_size_bytes, file_count, status, duration_ms, checksum, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            backup_type,
            str(backup_path),
            backup_info["total_size"],
            backup_info["file_count"],
            backup_info["status"],
            backup_info["duration"],
            checksum,
            json.dumps(backup_info)
        ))
        
        backup_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return backup_id
        
    def create_full_backup(self):
        """Create full backup"""
        self.log_backup("Starting full backup")
        
        backup_dir = self.create_backup_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"full_backup_{timestamp}.zip"
        backup_path = backup_dir / "full" / backup_filename
        
        # Get files to backup
        files_to_backup = self.get_files_to_backup()
        
        if not files_to_backup:
            self.log_backup("No files found to backup", "WARN")
            return False
        
        # Create backup archive
        backup_info = self.create_backup_archive(files_to_backup, backup_path, "full")
        
        if backup_info["status"] != "SUCCESS":
            return False
        
        # Verify backup
        if not self.verify_backup(backup_path):
            return False
        
        # Calculate checksum
        checksum = self.calculate_checksum(backup_path)
        
        # Save backup record
        backup_id = self.save_backup_record("full", backup_path, backup_info, checksum)
        
        self.log_backup(f"Full backup completed successfully: {backup_path}")
        return True
        
    def create_incremental_backup(self):
        """Create incremental backup"""
        self.log_backup("Starting incremental backup")
        
        backup_dir = self.create_backup_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"incremental_backup_{timestamp}.zip"
        backup_path = backup_dir / "incremental" / backup_filename
        
        # Get last backup time
        last_backup_time = self.get_last_backup_time("incremental")
        
        # Get files modified since last backup
        files_to_backup = []
        for file_path in self.get_files_to_backup():
            if file_path.stat().st_mtime > last_backup_time:
                files_to_backup.append(file_path)
        
        if not files_to_backup:
            self.log_backup("No new or modified files for incremental backup", "INFO")
            return True
        
        # Create backup archive
        backup_info = self.create_backup_archive(files_to_backup, backup_path, "incremental")
        
        if backup_info["status"] != "SUCCESS":
            return False
        
        # Verify backup
        if not self.verify_backup(backup_path):
            return False
        
        # Calculate checksum
        checksum = self.calculate_checksum(backup_path)
        
        # Save backup record
        backup_id = self.save_backup_record("incremental", backup_path, backup_info, checksum)
        
        self.log_backup(f"Incremental backup completed successfully: {backup_path}")
        return True
        
    def create_differential_backup(self):
        """Create differential backup"""
        self.log_backup("Starting differential backup")
        
        backup_dir = self.create_backup_directory()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"differential_backup_{timestamp}.zip"
        backup_path = backup_dir / "differential" / backup_filename
        
        # Get last full backup time
        last_full_backup_time = self.get_last_backup_time("full")
        
        # Get files modified since last full backup
        files_to_backup = []
        for file_path in self.get_files_to_backup():
            if file_path.stat().st_mtime > last_full_backup_time:
                files_to_backup.append(file_path)
        
        if not files_to_backup:
            self.log_backup("No files changed since last full backup", "INFO")
            return True
        
        # Create backup archive
        backup_info = self.create_backup_archive(files_to_backup, backup_path, "differential")
        
        if backup_info["status"] != "SUCCESS":
            return False
        
        # Verify backup
        if not self.verify_backup(backup_path):
            return False
        
        # Calculate checksum
        checksum = self.calculate_checksum(backup_path)
        
        # Save backup record
        backup_id = self.save_backup_record("differential", backup_path, backup_info, checksum)
        
        self.log_backup(f"Differential backup completed successfully: {backup_path}")
        return True
        
    def get_last_backup_time(self, backup_type):
        """Get timestamp of last backup of specified type"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT timestamp FROM backup_records 
            WHERE backup_type = ? AND status = 'SUCCESS'
            ORDER BY timestamp DESC LIMIT 1
        ''', (backup_type,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return datetime.fromisoformat(result[0]).timestamp()
        else:
            return 0
            
    def restore_from_backup(self, backup_path, target_path=None):
        """Restore files from backup"""
        if target_path is None:
            target_path = self.workspace_root
            
        self.log_backup(f"Starting restore from backup: {backup_path}")
        
        start_time = time.time()
        files_restored = 0
        
        try:
            if backup_path.suffix == '.zip':
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    for member in zipf.namelist():
                        try:
                            zipf.extract(member, target_path)
                            files_restored += 1
                        except Exception as e:
                            self.log_backup(f"Error extracting {member}: {e}", "WARN")
                            
            elif backup_path.suffix == '.tar.gz':
                with tarfile.open(backup_path, 'r:gz') as tarf:
                    tarf.extractall(target_path)
                    files_restored = len(tarf.getnames())
            
            duration = (time.time() - start_time) * 1000
            
            # Save recovery record
            self.save_recovery_record("restore", backup_path, target_path, files_restored, duration)
            
            self.log_backup(f"Restore completed successfully")
            self.log_backup(f"  Files restored: {files_restored}")
            self.log_backup(f"  Duration: {duration:.0f}ms")
            
            return True
            
        except Exception as e:
            self.log_backup(f"Error during restore: {e}", "ERROR")
            return False
            
    def save_recovery_record(self, recovery_type, source_backup, target_path, files_restored, duration):
        """Save recovery record to database"""
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO recovery_records 
            (recovery_type, source_backup, target_path, status, duration_ms, files_restored, details)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            recovery_type,
            str(source_backup),
            str(target_path),
            "SUCCESS",
            duration,
            files_restored,
            json.dumps({"timestamp": datetime.now().isoformat()})
        ))
        
        conn.commit()
        conn.close()
        
    def cleanup_old_backups(self):
        """Clean up old backups based on retention policy"""
        retention_days = self.config["backup"]["retention_days"]
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        
        self.log_backup(f"Cleaning up backups older than {retention_days} days")
        
        backup_dir = Path(self.config["backup_locations"]["local"])
        deleted_count = 0
        
        for backup_type_dir in ["full", "incremental", "differential"]:
            type_dir = backup_dir / backup_type_dir
            if type_dir.exists():
                for backup_file in type_dir.iterdir():
                    if backup_file.is_file():
                        file_time = datetime.fromtimestamp(backup_file.stat().st_mtime)
                        if file_time < cutoff_date:
                            try:
                                backup_file.unlink()
                                deleted_count += 1
                                self.log_backup(f"Deleted old backup: {backup_file}")
                            except Exception as e:
                                self.log_backup(f"Error deleting {backup_file}: {e}", "ERROR")
        
        self.log_backup(f"Cleanup completed: {deleted_count} old backups deleted")
        
    def run_backup_schedule(self):
        """Run scheduled backup based on configuration"""
        self.log_backup("Running scheduled backup")
        
        # Check if full backup is needed
        last_full_backup = self.get_last_backup_time("full")
        full_backup_interval = self.config["backup_types"]["full"]["interval_days"] * 24 * 3600
        
        if time.time() - last_full_backup > full_backup_interval:
            self.create_full_backup()
        else:
            # Check if differential backup is needed
            last_differential_backup = self.get_last_backup_time("differential")
            differential_backup_interval = self.config["backup_types"]["differential"]["interval_hours"] * 3600
            
            if time.time() - last_differential_backup > differential_backup_interval:
                self.create_differential_backup()
            else:
                # Create incremental backup
                self.create_incremental_backup()
        
        # Cleanup old backups
        self.cleanup_old_backups()
        
    def start_backup_service(self):
        """Start continuous backup service"""
        self.log_backup("Starting backup service")
        
        while True:
            try:
                self.run_backup_schedule()
                interval_hours = self.config["backup"]["interval_hours"]
                self.log_backup(f"Backup cycle completed, sleeping for {interval_hours} hours")
                time.sleep(interval_hours * 3600)
            except KeyboardInterrupt:
                self.log_backup("Backup service stopped by user")
                break
            except Exception as e:
                self.log_backup(f"Backup service error: {e}", "ERROR")
                time.sleep(3600)  # Wait 1 hour before retrying

def main():
    """Main function"""
    backup_system = BackupRecoverySystem()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "backup":
            backup_system.run_backup_schedule()
        elif command == "full":
            backup_system.create_full_backup()
        elif command == "incremental":
            backup_system.create_incremental_backup()
        elif command == "differential":
            backup_system.create_differential_backup()
        elif command == "restore":
            if len(sys.argv) > 2:
                backup_path = sys.argv[2]
                backup_system.restore_from_backup(Path(backup_path))
            else:
                print("Usage: python backup.py restore <backup_path>")
        elif command == "service":
            backup_system.start_backup_service()
        elif command == "cleanup":
            backup_system.cleanup_old_backups()
        elif command == "setup":
            print("Backup system setup complete!")
            print(f"Configuration: {backup_system.config_file}")
            print(f"Database: {backup_system.db_file}")
            print(f"Log file: {backup_system.log_file}")
        else:
            print("Usage: python backup.py [backup|full|incremental|differential|restore|service|cleanup|setup]")
    else:
        # Default: run scheduled backup
        backup_system.run_backup_schedule()

if __name__ == "__main__":
    main()
