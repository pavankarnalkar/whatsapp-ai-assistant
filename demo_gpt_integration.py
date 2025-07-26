#!/usr/bin/env python3
"""
Demo script showing the OpenAI GPT integration functionality.
Run this to see how the assistant works with the new features.
"""

import os
import time
from message_handler import AutoReplyBot, Message

def main():
    print("🤖 WhatsApp AI Assistant - GPT Integration Demo")
    print("=" * 50)
    
    # Check if OpenAI API key is configured
    api_key_configured = bool(os.getenv('OPENAI_API_KEY'))
    print(f"OpenAI API Key configured: {'✅ Yes' if api_key_configured else '❌ No'}")
    
    if not api_key_configured:
        print("💡 To test with real GPT responses, set OPENAI_API_KEY environment variable")
    
    print("\nTesting the assistant functionality...\n")
    
    # Initialize the bot
    bot = AutoReplyBot()
    
    # Test scenarios
    test_messages = [
        ("help", "Testing help command"),
        ("/summary", "Testing summary command"),
        ("What is Python programming?", "Testing Q&A functionality"),
        ("How do I learn machine learning?", "Testing Q&A with question"),
        ("Hello there", "Testing simple greeting (should not trigger Q&A)"),
        ("ok", "Testing short response (should not trigger Q&A)"),
        ("Can you explain neural networks?", "Testing technical Q&A"),
    ]
    
    chat_id = "demo_chat"
    user_id = "demo_user"
    
    print("📱 Simulating WhatsApp conversation:")
    print("-" * 40)
    
    for i, (message_text, description) in enumerate(test_messages, 1):
        print(f"\n{i}. {description}")
        print(f"👤 User: {message_text}")
        
        # Create message data
        message_data = {
            'chat_id': chat_id,
            'sender_id': user_id,
            'content': message_text,
            'timestamp': time.time()
        }
        
        # Get bot response
        response = bot.handle_incoming_message(message_data)
        
        if response:
            # Truncate long responses for demo
            display_response = response[:200] + "..." if len(response) > 200 else response
            print(f"🤖 Bot: {display_response}")
        else:
            print("🤖 Bot: (no response)")
        
        # Small delay for realism
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("📊 Demo completed! Key features demonstrated:")
    print("  ✅ Help command responses")
    print("  ✅ Summary generation (with chat history)")
    print("  ✅ Q&A responses for questions")
    print("  ✅ Smart triggering (no response for simple messages)")
    print("  ✅ Message storage in SQLite database")
    print("  ✅ Graceful handling without API key")
    
    # Show stored messages
    recent_messages = bot.message_handler.chat_db.get_recent_messages(chat_id, limit=10)
    print(f"\n💾 Stored {len(recent_messages)} messages in database:")
    for sender, timestamp, content, msg_id in recent_messages[-3:]:  # Show last 3
        truncated_content = content[:50] + "..." if len(content) > 50 else content
        print(f"  {sender}: {truncated_content}")
    
    if api_key_configured:
        print("\n🚀 With OpenAI API key configured, responses will be powered by GPT-3.5!")
    else:
        print("\n💡 Set OPENAI_API_KEY environment variable to enable real GPT responses")

if __name__ == "__main__":
    main()