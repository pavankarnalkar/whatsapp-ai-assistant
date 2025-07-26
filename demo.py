#!/usr/bin/env python3
"""
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
    interactive_demo()