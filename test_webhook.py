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
Simple test script to validate the webhook functionality
"""
import requests
import json
import time
from datetime import datetime


def test_webhook_endpoint():
    """Test the webhook endpoint with various message formats"""
    base_url = "http://localhost:8000"
    
    print("Testing WhatsApp AI Assistant Webhook...")
    
    # Test health check
    print("1. Testing health check...")
    response = requests.get(f"{base_url}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("✓ Health check passed")
    
    # Test stats (should show 0 messages initially)
    print("2. Testing stats endpoint...")
    response = requests.get(f"{base_url}/stats")
    assert response.status_code == 200
    data = response.json()
    initial_count = data["total_messages"]
    print(f"✓ Stats endpoint working, initial message count: {initial_count}")
    
    # Test webhook with standard format
    print("3. Testing webhook with standard message format...")
    test_message_1 = {
        "sender_id": "test_sender_123",
        "chat_id": "test_chat_456",
        "timestamp": datetime.now().isoformat(),
        "message_text": "Test message from automated test",
        "message_id": "test_msg_001"
    }
    
    response = requests.post(f"{base_url}/webhook/message", json=test_message_1)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print("✓ Standard format message processed successfully")
    
    # Test webhook with alternative format
    print("4. Testing webhook with alternative message format...")
    test_message_2 = {
        "from": "alt_sender_789",
        "chatId": "test_chat_456",
        "time": int(time.time()),
        "body": "Alternative format test message",
        "id": "test_msg_002"
    }
    
    response = requests.post(f"{base_url}/webhook/message", json=test_message_2)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    print("✓ Alternative format message processed successfully")
    
    # Test retrieving messages for a chat
    print("5. Testing message retrieval...")
    response = requests.get(f"{base_url}/messages/test_chat_456")
    assert response.status_code == 200
    data = response.json()
    assert data["chat_id"] == "test_chat_456"
    assert data["count"] == 2  # Should have 2 messages for this chat
    print(f"✓ Retrieved {data['count']} messages for chat test_chat_456")
    
    # Test updated stats
    print("6. Testing updated stats...")
    response = requests.get(f"{base_url}/stats")
    assert response.status_code == 200
    data = response.json()
    new_count = data["total_messages"]
    assert new_count == initial_count + 2
    print(f"✓ Stats updated correctly, new total: {new_count}")
    
    # Test error handling
    print("7. Testing error handling...")
    invalid_message = {"invalid": "payload"}
    response = requests.post(f"{base_url}/webhook/message", json=invalid_message)
    assert response.status_code == 400
    print("✓ Error handling working correctly")
    
    print("\n🎉 All tests passed! Webhook listener is working correctly.")


if __name__ == "__main__":
    try:
        test_webhook_endpoint()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to webhook server at http://localhost:8000")
        print("Please make sure the server is running with: python main.py")
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
