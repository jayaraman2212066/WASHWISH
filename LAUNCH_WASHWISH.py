#!/usr/bin/env python3
"""
WashWish Laundry Management System - Complete Launcher
This script will setup and launch the entire system automatically
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
from pathlib import Path

class WashWishLauncher:
    def __init__(self):
        self.project_dir = Path(__file__).parent
        os.chdir(self.project_dir)
        
    def print_header(self):
        print("=" * 60)
        print("    WashWish Laundry Management System")
        print("    Complete Setup and Launch")
        print("=" * 60)
        
    def run_command(self, command, description, critical=True):
        """Run a command and handle errors"""
        print(f"[STEP] {description}...")
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print(f"[SUCCESS] {description}")
                return True
            else:
                print(f"[WARNING] {description} - {result.stderr.strip()}")
                if critical:
                    return False
                return True
                
        except subprocess.TimeoutExpired:
            print(f"[ERROR] {description} timed out")
            return False
        except Exception as e:
            print(f"[ERROR] {description} failed: {e}")
            return False
    
    def setup_system(self):
        """Setup the Django system"""
        print("\n[PHASE 1] System Setup")
        print("-" * 30)
        
        # Check Django installation
        if not self.run_command("python -c \"import django; print('Django OK')\"", "Checking Django"):
            print("[ERROR] Django not installed. Please run: pip install -r requirements.txt")
            return False
            
        # System check
        if not self.run_command("python manage.py check", "Django system check"):
            return False
            
        # Database migrations
        if not self.run_command("python manage.py migrate", "Database setup"):
            return False
            
        # Collect static files
        self.run_command("python manage.py collectstatic --noinput", "Static files", critical=False)
        
        # Populate initial data
        self.run_command("python manage.py populate_data", "Initial data", critical=False)
        
        return True
    
    def create_superuser_if_needed(self):
        """Create superuser if none exists"""
        print("\n[PHASE 2] Admin User Setup")
        print("-" * 30)
        
        check_admin = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detergee.settings')
django.setup()
from django.contrib.auth.models import User
if User.objects.filter(is_superuser=True).exists():
    print('ADMIN_EXISTS')
else:
    print('NO_ADMIN')
"""
        
        result = subprocess.run([sys.executable, '-c', check_admin], 
                              capture_output=True, text=True)
        
        if 'NO_ADMIN' in result.stdout:
            print("[INFO] Creating admin user...")
            create_admin = """
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'detergee.settings')
django.setup()
from django.contrib.auth.models import User
User.objects.create_superuser('admin', 'admin@washwish.com', 'admin123')
print('Admin user created: admin/admin123')
"""
            subprocess.run([sys.executable, '-c', create_admin])
        else:
            print("[INFO] Admin user already exists")
    
    def open_browser_delayed(self):
        """Open browser after server starts"""
        time.sleep(8)  # Wait for server to fully start
        print("\n[INFO] Opening browser...")
        webbrowser.open('http://127.0.0.1:8000')
    
    def start_server(self):
        """Start the Django development server"""
        print("\n[PHASE 3] Starting Server")
        print("-" * 30)
        
        # Start browser in background
        browser_thread = threading.Thread(target=self.open_browser_delayed)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("\n" + "=" * 60)
        print("    SERVER RUNNING")
        print("=" * 60)
        print("URL: http://127.0.0.1:8000")
        print("Admin: http://127.0.0.1:8000/admin")
        print("Login: admin / admin123")
        print("=" * 60)
        print("Features:")
        print("• User Registration & Login")
        print("• Service Booking & Tracking")
        print("• Payment Processing")
        print("• Admin Dashboard")
        print("• Reports & Analytics")
        print("=" * 60)
        print("Press Ctrl+C to stop")
        print("=" * 60)
        
        try:
            # Start Django server
            subprocess.run([
                sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
            ], check=True)
        except KeyboardInterrupt:
            print("\n\n[INFO] Server stopped by user")
        except Exception as e:
            print(f"\n[ERROR] Server error: {e}")
            return False
        
        return True
    
    def launch(self):
        """Main launch sequence"""
        self.print_header()
        
        try:
            # Phase 1: Setup
            if not self.setup_system():
                print("\n[FAILED] System setup failed")
                input("Press Enter to exit...")
                return False
            
            # Phase 2: Admin user
            self.create_superuser_if_needed()
            
            # Phase 3: Start server
            self.start_server()
            
        except KeyboardInterrupt:
            print("\n\n[INFO] Launch cancelled by user")
        except Exception as e:
            print(f"\n[ERROR] Launch failed: {e}")
            input("Press Enter to exit...")
            return False
        
        return True

def main():
    launcher = WashWishLauncher()
    launcher.launch()

if __name__ == "__main__":
    main()