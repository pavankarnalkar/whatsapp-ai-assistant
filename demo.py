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
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()