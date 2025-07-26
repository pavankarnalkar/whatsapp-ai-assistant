#!/usr/bin/env python3
"""
Example integration script showing how to use the urgency detection system
in a real WhatsApp AI Assistant webhook.
"""

import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src import MessageProcessor


def simulate_webhook_handler(message_data):
    """
    Simulate a webhook handler that would receive WhatsApp messages.
    
    This function demonstrates how the urgency detection would integrate
    into a real WhatsApp webhook endpoint.
    """
    print(f"📱 Received message from {message_data.get('sender', 'unknown')}")
    print(f"📄 Content: {message_data['text']}")
    
    # Initialize the message processor
    processor = MessageProcessor()
    
    # Process the message for urgency
    result = processor.process_message(message_data)
    
    # Handle the result
    if result['is_urgent']:
        print(f"🚨 URGENT MESSAGE DETECTED!")
        print(f"   Keywords: {', '.join(result['matched_keywords'])}")
        print(f"   Email alert sent: {'✅ Yes' if result['email_sent'] else '❌ Failed'}")
        
        # In a real application, you might also:
        # - Store the urgent flag in your database
        # - Send a priority response
        # - Escalate to human operators
        # - Log the urgent message for review
        
    else:
        print("📝 Normal message processing")
    
    print("-" * 50)
    return result


def main():
    """Run example integration scenarios."""
    print("🔗 WhatsApp AI Assistant - Integration Example")
    print("=" * 50)
    
    # Example messages that might come from WhatsApp webhook
    example_messages = [
        {
            'text': 'Hey, how are you doing today?',
            'sender': 'john_doe',
            'chat_id': 'personal_chat',
            'timestamp': datetime.now()
        },
        {
            'text': 'URGENT: Server is down! Need immediate help!',
            'sender': 'admin_user',
            'chat_id': 'it_support',
            'timestamp': datetime.now()
        },
        {
            'text': 'Can you help me with this task when you have time?',
            'sender': 'colleague',
            'chat_id': 'work_chat',
            'timestamp': datetime.now()
        },
        {
            'text': 'Emergency! Car broke down, need pickup ASAP!',
            'sender': 'family_member',
            'chat_id': 'family_group',
            'timestamp': datetime.now()
        }
    ]
    
    # Process each message
    for i, message in enumerate(example_messages, 1):
        print(f"Message {i}:")
        result = simulate_webhook_handler(message)
    
    print("\n💡 Integration Notes:")
    print("- Configure SMTP settings in .env for email notifications")
    print("- Customize urgency keywords for your use case")
    print("- Store urgency status in your database for analytics")
    print("- Consider rate limiting email notifications in production")
    print("- Add webhook authentication for security")


if __name__ == "__main__":
    main()