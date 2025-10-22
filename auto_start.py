#!/usr/bin/env python3
"""
Auto-start script for WashWish Laundry Management System
This script will:
1. Check the Django project
2. Run migrations
3. Populate initial data
4. Start the server
5. Automatically open the webpage in browser
"""

import os
import sys
import subprocess
import time
import webbrowser
import threading
import signal
from pathlib import Path

# Change to project directory
PROJECT_DIR = Path(__file__).parent
os.chdir(PROJECT_DIR)

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"⚠️  {description} completed with warnings:")
            if result.stderr:
                print(f"   {result.stderr.strip()}")
            return True  # Continue even with warnings
    except Exception as e:
        print(f"❌ {description} failed: {e}")
        return False

def open_browser_delayed():
    """Open browser after a delay to ensure server is ready"""
    time.sleep(5)  # Wait 5 seconds for server to start
    print("🌐 Opening webpage in browser...")
    webbrowser.open('http://127.0.0.1:8000')

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print('\n\n🛑 Shutting down server...')
    sys.exit(0)

def main():
    print("🚀 WashWish Laundry Management System")
    print("=" * 50)
    
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Step 1: Check Django project
    if not run_command("python manage.py check", "Checking Django project"):
        return False
    
    # Step 2: Run migrations
    if not run_command("python manage.py migrate", "Running database migrations"):
        return False
    
    # Step 3: Collect static files
    run_command("python manage.py collectstatic --noinput", "Collecting static files")
    
    # Step 4: Populate initial data
    run_command("python manage.py populate_data", "Populating initial data")
    
    print("\n" + "=" * 50)
    print("🎯 SERVER INFORMATION")
    print("=" * 50)
    print("📍 Local URL: http://127.0.0.1:8000")
    print("📍 Admin Panel: http://127.0.0.1:8000/admin")
    print("👤 Admin Login: admin / admin123")
    print("=" * 50)
    print("🔥 Features Available:")
    print("   • User Registration & Login")
    print("   • Laundry Service Booking")
    print("   • Order Tracking")
    print("   • Payment Processing")
    print("   • Admin Dashboard")
    print("   • Reports & Analytics")
    print("=" * 50)
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    # Step 5: Start browser in background thread
    browser_thread = threading.Thread(target=open_browser_delayed)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Step 6: Start Django development server
    print("🚀 Starting Django development server...")
    try:
        # Start server and keep it running
        subprocess.run([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n❌ Failed to start the application")
            input("Press Enter to exit...")
            sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)