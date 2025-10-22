#!/usr/bin/env python3
"""
Simple script to start Django development server and test connectivity
"""

import os
import sys
import subprocess
import time
import requests
from threading import Thread

def start_django_server():
    """Start Django development server"""
    try:
        # Change to project directory
        os.chdir(r'd:\PROJECT_RENDER\WASHWISH')
        
        # Start Django server
        process = subprocess.Popen([
            sys.executable, 'manage.py', 'runserver', '127.0.0.1:8000'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        print("🚀 Starting Django development server...")
        print("📍 Server will be available at: http://127.0.0.1:8000")
        print("📍 Admin panel: http://127.0.0.1:8000/admin")
        print("\n⏳ Waiting for server to start...")
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Test connectivity
        try:
            response = requests.get('http://127.0.0.1:8000', timeout=5)
            if response.status_code == 200:
                print("✅ Server is running successfully!")
                print("🌐 Open your browser and go to: http://127.0.0.1:8000")
            else:
                print(f"⚠️  Server responded with status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Could not connect to server: {e}")
        
        # Keep server running
        print("\n📝 Server logs:")
        print("-" * 50)
        
        try:
            # Print server output
            for line in process.stdout:
                print(line.strip())
        except KeyboardInterrupt:
            print("\n🛑 Stopping server...")
            process.terminate()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_django_server()