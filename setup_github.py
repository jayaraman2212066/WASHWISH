#!/usr/bin/env python3
"""
GitHub Repository Setup Script for WashWish
This script helps you set up a GitHub repository for the WashWish project
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"[INFO] {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[SUCCESS] {description}")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"[ERROR] {description} failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"[ERROR] {description} failed: {e}")
        return False

def main():
    print("=" * 60)
    print("    WashWish GitHub Repository Setup")
    print("=" * 60)
    
    # Check if we're in a git repository
    if not os.path.exists('.git'):
        print("[ERROR] Not in a Git repository. Please run 'git init' first.")
        return False
    
    print("\nTo set up your GitHub repository, follow these steps:")
    print("\n1. Create a new repository on GitHub:")
    print("   - Go to https://github.com/new")
    print("   - Repository name: washwish-laundry-system")
    print("   - Description: Django-based laundry management system")
    print("   - Make it Public or Private (your choice)")
    print("   - DO NOT initialize with README, .gitignore, or license")
    print("   - Click 'Create repository'")
    
    print("\n2. Copy the repository URL from GitHub")
    print("   Example: https://github.com/yourusername/washwish-laundry-system.git")
    
    # Get repository URL from user
    repo_url = input("\n3. Enter your GitHub repository URL: ").strip()
    
    if not repo_url:
        print("[ERROR] Repository URL is required")
        return False
    
    # Add remote origin
    if not run_command(f"git remote add origin {repo_url}", "Adding GitHub remote"):
        # If remote already exists, try to set the URL
        run_command(f"git remote set-url origin {repo_url}", "Updating GitHub remote URL")
    
    # Push to GitHub
    print("\n[INFO] Pushing to GitHub...")
    if run_command("git branch -M main", "Setting main branch"):
        if run_command("git push -u origin main", "Pushing to GitHub"):
            print("\n" + "=" * 60)
            print("    SUCCESS! Repository uploaded to GitHub")
            print("=" * 60)
            print(f"Repository URL: {repo_url}")
            print(f"View online: {repo_url.replace('.git', '')}")
            print("\nNext steps:")
            print("1. Visit your repository on GitHub")
            print("2. Add collaborators if needed")
            print("3. Set up branch protection rules")
            print("4. Configure deployment settings")
            print("=" * 60)
            return True
    
    return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n[FAILED] GitHub setup incomplete")
            input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\n\n[INFO] Setup cancelled by user")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        input("Press Enter to exit...")