#!/usr/bin/env python3
"""
Test script for WhatsApp AI Assistant webhook functionality
"""

import requests
import json
import time

def test_webhook(base_url="http://localhost:5000"):
    """Test the webhook endpoint with sample data"""
    
    webhook_url = f"{base_url}/webhook"
    health_url = f"{base_url}/health"
    
    print("🧪 Testing WhatsApp AI Assistant...")
    print(f"Base URL: {base_url}")
    
    # Test health check
    print("\n1. Testing health check...")
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test webhook with sample message
    print("\n2. Testing webhook endpoint...")
    test_message = {
        "chat_id": "test_chat_123",
        "sender": "test_user",
        "text": "Hello, can you help me?"
    }
    
    try:
        response = requests.post(
            webhook_url, 
            json=test_message, 
            timeout=10,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("✅ Webhook test passed")
            result = response.json()
            print(f"   Status: {result.get('status')}")
            print(f"   Response: {result.get('response', 'No response')}")
        else:
            print(f"❌ Webhook test failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Webhook test failed: {e}")
        return False
    
    # Test help command
    print("\n3. Testing help command...")
    help_message = {
        "chat_id": "test_chat_123",
        "sender": "test_user",
        "text": "help"
    }
    
    try:
        response = requests.post(webhook_url, json=help_message, timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Help command test passed")
            print(f"   Response: {result.get('response', 'No response')}")
        else:
            print(f"❌ Help command test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Help command test failed: {e}")
    
    # Test message history endpoint
    print("\n4. Testing message history...")
    history_url = f"{base_url}/messages/test_chat_123"
    
    try:
        response = requests.get(history_url, timeout=5)
        if response.status_code == 200:
            result = response.json()
            print("✅ Message history test passed")
            print(f"   Messages count: {len(result.get('messages', []))}")
        else:
            print(f"❌ Message history test failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Message history test failed: {e}")
    
    print("\n🎉 Testing complete!")
    return True

if __name__ == "__main__":
    import sys
    
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:5000"
    test_webhook(base_url)