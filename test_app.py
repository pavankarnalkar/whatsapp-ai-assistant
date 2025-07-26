"""
Simple test script for the MCP client and message sending functionality.
"""
import os
import sys
import time
from mcp_client import MCPClient


def test_mcp_client():
    """Test the MCP client functionality."""
    print("Testing MCP Client...")
    
    # Initialize client
    client = MCPClient()
    print(f"MCP Base URL: {client.base_url}")
    
    # Test data
    test_recipient = "test_recipient_id"
    test_message = "Hello! This is a test message from the WhatsApp AI Assistant."
    
    print(f"Attempting to send test message to: {test_recipient}")
    print(f"Message: {test_message}")
    
    try:
        # Test sending a message
        result = client.send_message(test_recipient, test_message)
        print(f"✅ Message sent successfully: {result}")
        
        # Test the reply wrapper function
        reply_success = client.send_reply(test_recipient, "This is a test reply!")
        if reply_success:
            print("✅ Reply function working correctly")
        else:
            print("❌ Reply function failed")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        print("Note: This is expected if MCP server is not running or not configured correctly.")


def test_static_replies():
    """Test the static reply generation logic."""
    print("\nTesting static reply generation...")
    
    # Import the function from app.py
    sys.path.append(os.path.dirname(__file__))
    from app import generate_reply
    
    test_cases = [
        ("help", "Hello! I am your WhatsApp AI Assistant. You can ask me anything!"),
        ("hello there", "Hi there! How can I help you today?"),
        ("hi everyone", "Hello! Nice to meet you!"),
        ("random message", "Thanks for your message! This is an automated reply from your AI Assistant."),
        ("I need help please", "Hello! I am your WhatsApp AI Assistant. You can ask me anything!"),
    ]
    
    for input_msg, expected in test_cases:
        result = generate_reply(input_msg.lower())
        if expected in result or result == expected:
            print(f"✅ '{input_msg}' -> '{result}'")
        else:
            print(f"❌ '{input_msg}' -> Expected: '{expected}', Got: '{result}'")


if __name__ == "__main__":
    print("WhatsApp AI Assistant - Test Suite")
    print("=" * 50)
    
    test_static_replies()
    test_mcp_client()
    
    print("\n" + "=" * 50)
    print("Test completed!")
    print("\nTo test the full webhook functionality:")
    print("1. Start the app: python app.py")
    print("2. Use curl or Postman to send POST requests to /webhook")
    print("3. Check the logs for message sending attempts")