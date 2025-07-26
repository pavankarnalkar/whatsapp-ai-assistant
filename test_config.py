#!/usr/bin/env python3
"""
Test script for ngrok tunnel manager configuration
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_configuration():
    """Test the configuration for ngrok tunnel"""
    print("="*60)
    print("NGROK TUNNEL CONFIGURATION TEST")
    print("="*60)
    
    # Check environment variables
    webhook_port = int(os.getenv('WEBHOOK_PORT', 5000))
    mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:3000')
    ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
    ngrok_subdomain = os.getenv('NGROK_SUBDOMAIN')
    
    print(f"Webhook Port: {webhook_port}")
    print(f"MCP Server URL: {mcp_server_url}")
    print(f"ngrok Auth Token: {'Set' if ngrok_auth_token else 'Not set'}")
    print(f"ngrok Subdomain: {ngrok_subdomain if ngrok_subdomain else 'Not configured'}")
    
    # Check if required dependencies are available
    try:
        from pyngrok import ngrok, conf
        print("✓ pyngrok library available")
    except ImportError:
        print("✗ pyngrok library not found")
        return False
    
    try:
        import requests
        print("✓ requests library available") 
    except ImportError:
        print("✗ requests library not found")
        return False
    
    # Check ngrok configuration
    if ngrok_auth_token and ngrok_auth_token != 'demo_token':
        print("✓ ngrok auth token configured")
    else:
        print("⚠ ngrok auth token not properly configured (using demo token)")
        print("  Get your token from: https://dashboard.ngrok.com/get-started/your-authtoken")
    
    print("\nConfiguration test completed!")
    print("Use ngrok_tunnel.py to start the actual tunnel.")
    
    return True

if __name__ == "__main__":
    test_configuration()