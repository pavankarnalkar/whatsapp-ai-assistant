"""Main entry point for WhatsApp AI Assistant."""

import logging
import time
from typing import Dict, Any

from message_handler import AutoReplyBot
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate the auto-reply functionality."""
    logger.info("Starting WhatsApp AI Assistant")
    
    # Initialize the bot
    bot = AutoReplyBot()
    
    # Example usage - simulate incoming messages
    example_messages = [
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': 'help',
            'timestamp': time.time(),
            'message_id': 'msg_1'
        },
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': '/summary',
            'timestamp': time.time(),
            'message_id': 'msg_2'
        },
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': 'Hello there!',
            'timestamp': time.time(),
            'message_id': 'msg_3'
        }
    ]
    
    print("=" * 60)
    print("WhatsApp AI Assistant - Auto-Reply Demo")
    print("=" * 60)
    
    for i, message_data in enumerate(example_messages, 1):
        print(f"\n--- Test Message {i} ---")
        print(f"Input: {message_data['content']}")
        
        response = bot.handle_incoming_message(message_data)
        
        if response:
            print(f"✅ Auto-reply triggered:")
            print(response)
        else:
            print("❌ No auto-reply triggered")
        
        print("-" * 40)
    
    print("\n🎉 Demo completed successfully!")
    print("\nTo integrate with WhatsApp MCP:")
    print("1. Set up webhook endpoint to receive messages")
    print("2. Configure MCP_BASE_URL and MCP_API_KEY")
    print("3. Add OpenAI API key for summary functionality")

if __name__ == "__main__":
    main()