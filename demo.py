#!/usr/bin/env python3
"""
WhatsApp AI Assistant - Urgency Detection Demo

A simple command-line tool to test the urgency detection and email notification system.
"""

import sys
import json
from datetime import datetime
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent))

from src import MessageProcessor, Config


def main():
    """Main function to run the demo."""
    print("🤖 WhatsApp AI Assistant - Urgency Detection Demo")
    print("=" * 50)
    
    # Initialize the message processor
    processor = MessageProcessor()
    
    # Check configuration
    print("\n📋 Configuration Status:")
    print(f"SMTP Host: {Config.SMTP_HOST}")
    print(f"SMTP Port: {Config.SMTP_PORT}")
    print(f"SMTP Configured: {'✅ Yes' if Config.is_smtp_configured() else '❌ No'}")
    print(f"Urgency Keywords: {', '.join(Config.get_urgency_keywords())}")
    
    # Run system test
    print("\n🧪 Running System Tests...")
    test_results = processor.test_system()
    
    print("\n📊 Urgency Detection Tests:")
    for test in test_results['urgency_detection_tests']:
        status = "🚨 URGENT" if test['is_urgent'] else "📝 Normal"
        keywords = f" (Keywords: {', '.join(test['keywords'])})" if test['keywords'] else ""
        print(f"  {status}: \"{test['message']}\"{keywords}")
    
    print(f"\n📧 Email Configuration Test: {'✅ Passed' if test_results['email_configuration_test'] else '❌ Failed'}")
    
    # Interactive demo
    print("\n" + "=" * 50)
    print("🎮 Interactive Demo - Enter messages to test urgency detection")
    print("Type 'quit' to exit, 'test' to send a test urgent message")
    print("=" * 50)
    
    while True:
        try:
            message = input("\n💬 Enter message: ").strip()
            
            if message.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if message.lower() == 'test':
                # Send a test urgent message
                test_message_data = {
                    'text': 'This is an urgent test message from the demo!',
                    'sender': 'Demo User',
                    'chat_id': 'demo_chat',
                    'timestamp': datetime.now()
                }
                result = processor.process_message(test_message_data)
                print("🧪 Test urgent message processed:")
            elif message:
                # Process the entered message
                message_data = {
                    'text': message,
                    'sender': 'Demo User',
                    'chat_id': 'demo_chat',
                    'timestamp': datetime.now()
                }
                result = processor.process_message(message_data)
            else:
                continue
            
            # Display results
            if result['is_urgent']:
                print(f"🚨 URGENT MESSAGE DETECTED!")
                print(f"   Keywords found: {', '.join(result['matched_keywords'])}")
                print(f"   Email sent: {'✅ Yes' if result['email_sent'] else '❌ Failed'}")
            else:
                print("📝 Normal message (no urgency detected)")
            
Interactive demo of WhatsApp AI Assistant auto-reply functionality.

Run this script to test the trigger detection and responses interactively.
"""

from message_handler import AutoReplyBot
import time

def interactive_demo():
    """Run an interactive demo of the auto-reply functionality."""
    print("🤖 WhatsApp AI Assistant - Interactive Demo")
    print("=" * 50)
    print("Type messages to test auto-reply functionality.")
    print("Supported triggers:")
    print("• help, /help, commands")
    print("• /summary, summary, summarize")
    print("• Type 'quit' to exit")
    print("-" * 50)
    
    bot = AutoReplyBot()
    
    while True:
        try:
            user_input = input("\n💬 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            # Simulate message data
            message_data = {
                'chat_id': 'demo_chat',
                'sender_id': 'demo_user',
                'content': user_input,
                'timestamp': time.time(),
                'message_id': f'msg_{time.time()}'
            }
            
            # Get response from bot
            response = bot.handle_incoming_message(message_data)
            
            if response:
                print(f"🤖 Bot: {response}")
            else:
                print("🤖 Bot: (no auto-reply triggered)")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    interactive_demo()
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
