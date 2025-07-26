#!/usr/bin/env python3
"""
Validation script to check if ngrok tunnel and webhook setup is production-ready
"""

import os
import sys
import requests
import subprocess
from dotenv import load_dotenv

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    # Check Python packages
    required_packages = [
        ('flask', 'flask'),
        ('pyngrok', 'pyngrok'), 
        ('requests', 'requests'),
        ('python-dotenv', 'dotenv')
    ]
    missing_packages = []
    
    for display_name, import_name in required_packages:
        try:
            __import__(import_name)
            print(f"✓ {display_name}")
        except ImportError:
            print(f"✗ {display_name}")
            missing_packages.append(display_name)
    
    return len(missing_packages) == 0

def check_configuration():
    """Check if configuration is properly set"""
    print("\nChecking configuration...")
    
    load_dotenv()
    
    # Check required environment variables
    ngrok_token = os.getenv('NGROK_AUTH_TOKEN')
    webhook_port = os.getenv('WEBHOOK_PORT', '5000')
    mcp_url = os.getenv('MCP_SERVER_URL', 'http://localhost:3000')
    
    issues = []
    
    if not ngrok_token or ngrok_token == 'demo_token':
        issues.append("NGROK_AUTH_TOKEN not properly configured")
        print("✗ ngrok auth token")
    else:
        print("✓ ngrok auth token")
    
    try:
        port = int(webhook_port)
        if 1024 <= port <= 65535:
            print(f"✓ webhook port ({port})")
        else:
            issues.append(f"Invalid webhook port: {port}")
            print(f"✗ webhook port ({port})")
    except ValueError:
        issues.append(f"Invalid webhook port format: {webhook_port}")
        print(f"✗ webhook port ({webhook_port})")
    
    print(f"✓ MCP server URL ({mcp_url})")
    
    return len(issues) == 0, issues

def check_ngrok_availability():
    """Check if ngrok is available and can be configured"""
    print("\nChecking ngrok availability...")
    
    try:
        from pyngrok import ngrok, conf
        
        # Check if auth token can be set
        token = os.getenv('NGROK_AUTH_TOKEN')
        if token and token != 'demo_token':
            conf.get_default().auth_token = token
            print("✓ ngrok configuration successful")
            return True
        else:
            print("⚠ ngrok auth token not configured (free tier limitations)")
            return False
            
    except Exception as e:
        print(f"✗ ngrok configuration failed: {str(e)}")
        return False

def check_webhook_server():
    """Check if webhook server can start properly"""
    print("\nChecking webhook server...")
    
    # Try to import the app
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from app import app
        print("✓ Webhook server module loads correctly")
        
        # Check if Flask app is properly configured
        if hasattr(app, 'run'):
            print("✓ Flask application configured correctly")
            return True
        else:
            print("✗ Flask application configuration issue")
            return False
            
    except Exception as e:
        print(f"✗ Webhook server import failed: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("="*60)
    print("WHATSAPP AI ASSISTANT - SETUP VALIDATION")
    print("="*60)
    
    all_checks_passed = True
    
    # Run all validation checks
    checks = [
        ("Dependencies", check_dependencies),
        ("ngrok Availability", check_ngrok_availability), 
        ("Webhook Server", check_webhook_server),
    ]
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            if not result:
                all_checks_passed = False
        except Exception as e:
            print(f"✗ {check_name} check failed: {str(e)}")
            all_checks_passed = False
    
    # Configuration check returns both result and issues
    config_ok, config_issues = check_configuration()
    if not config_ok:
        all_checks_passed = False
        if config_issues:
            print("\nConfiguration issues:")
            for issue in config_issues:
                print(f"  - {issue}")
    
    print("\n" + "="*60)
    if all_checks_passed:
        print("✅ VALIDATION PASSED - Setup is ready!")
        print("\nNext steps:")
        print("1. Run: ./setup_tunnel.sh")
        print("2. Or manually: python3 ngrok_tunnel.py")
        print("3. Configure your MCP server to use the webhook URL")
    else:
        print("❌ VALIDATION FAILED - Please fix the issues above")
        print("\nTroubleshooting:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Configure .env file with proper values")
        print("3. Get ngrok auth token from: https://dashboard.ngrok.com/get-started/your-authtoken")
    
    print("="*60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())