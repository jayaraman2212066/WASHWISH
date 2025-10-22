import os
import subprocess
import sys

def run_setup():
    print("Setting up WashWish Laundry Management System...")
    
    # Change to project directory
    os.chdir(r'd:\PROJECT_RENDER\WASHWISH')
    
    commands = [
        ("python manage.py check", "System check"),
        ("python manage.py migrate", "Database setup"),
        ("python manage.py populate_data", "Initial data"),
        ("python manage.py collectstatic --noinput", "Static files")
    ]
    
    for cmd, desc in commands:
        print(f"\n{desc}...")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {desc} completed")
            else:
                print(f"! {desc} completed with warnings")
        except Exception as e:
            print(f"✗ {desc} failed: {e}")
    
    print("\n" + "="*50)
    print("Setup completed!")
    print("To start the server, run: RUN_WASHWISH.bat")
    print("Or manually: python manage.py runserver 127.0.0.1:8000")
    print("Then open: http://127.0.0.1:8000")
    print("="*50)

if __name__ == "__main__":
    run_setup()