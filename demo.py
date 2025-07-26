#!/usr/bin/env python3
"""
Demo script showing WhatsApp AI Assistant functionality.
This simulates the complete workflow without requiring an actual MCP server.
"""
import json
import time
from mcp_client import MCPClient
from app import generate_reply


def demo_static_replies():
    """Demo the static reply functionality."""
    print("🤖 WhatsApp AI Assistant - Static Reply Demo")
    print("=" * 50)
    
    test_messages = [
        "help",
        "hello everyone!", 
        "hi there",
        "what's the weather like?",
        "I need help with my order"
    ]
    
    for message in test_messages:
        reply = generate_reply(message.lower())
        print(f"📱 User: {message}")
        print(f"🤖 Bot: {reply}")
        print("-" * 30)


def demo_mcp_client():
    """Demo the MCP client functionality."""
    print("\n📡 MCP Client Demo")
    print("=" * 50)
    
    client = MCPClient()
    print(f"MCP Server: {client.base_url}")
    
    # Demo message data
    recipient = "demo_user_123"
    message = "Hello! This is a demo message from the WhatsApp AI Assistant."
    
    print(f"Attempting to send message...")
    print(f"📱 To: {recipient}")
    print(f"💬 Message: {message}")
    
    try:
        # This will fail since we don't have a real MCP server, but shows the structure
        result = client.send_message(recipient, message)
        print(f"✅ Success: {result}")
    except Exception as e:
        print(f"⚠️  Expected error (no MCP server): {type(e).__name__}")
        print("   In production, this would send the message successfully.")


def demo_webhook_processing():
    """Demo webhook message processing."""
    print("\n🌐 Webhook Processing Demo")
    print("=" * 50)
    
    # Simulate incoming webhook payloads
    sample_messages = [
        {
            "sender": "user_001",
            "chat_id": "chat_001", 
            "text": "hello",
            "timestamp": "2024-01-01T12:00:00Z"
        },
        {
            "sender": "user_002",
            "chat_id": "chat_002",
            "text": "I need help with my account",
            "timestamp": "2024-01-01T12:01:00Z"
        },
        {
            "sender": "user_003", 
            "chat_id": "chat_003",
            "text": "what's your status?",
            "timestamp": "2024-01-01T12:02:00Z"
        }
    ]
    
    for msg in sample_messages:
        print(f"📨 Incoming webhook payload:")
        print(f"   {json.dumps(msg, indent=2)}")
        
        # Process like the webhook would
        reply = generate_reply(msg["text"].lower())
        print(f"🤖 Generated reply: {reply}")
        print(f"📤 Would send to: {msg['chat_id']}")
        print("-" * 40)


if __name__ == "__main__":
    print("🚀 WhatsApp AI Assistant - Complete Demo")
    print("=" * 60)
    print("This demo shows all the implemented functionality:")
    print("1. Static reply generation")
    print("2. MCP client message sending")
    print("3. Webhook message processing")
    print("=" * 60)
    
    demo_static_replies()
    demo_mcp_client()
    demo_webhook_processing()
    
    print("\n✅ Demo completed!")
    print("\n📋 Next Steps:")
    print("1. Set up actual whatsapp-mcp server")
    print("2. Configure MCP_BASE_URL in .env file")
    print("3. Run: python app.py")
    print("4. Configure MCP to send webhooks to your /webhook endpoint")
    print("5. Start receiving and replying to WhatsApp messages!")