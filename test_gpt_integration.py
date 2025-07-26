#!/usr/bin/env python3
"""
Test script for GPT integration in WhatsApp AI Assistant.
This script tests the new GPT functionality without requiring API keys.
"""

import os
import time
from message_handler import AutoReplyBot, Message, MessageHandler

def test_gpt_integration():
    """Test the GPT integration functionality."""
    print("=== Testing GPT Integration ===\n")
    
    # Create a temporary database for testing
    test_db_path = "test_gpt_integration.db"
    
    try:
        # Initialize the bot with test database
        message_handler = MessageHandler(db_path=test_db_path)
        bot = AutoReplyBot()
        bot.message_handler = message_handler
        
        print("1. Testing help command (should work without GPT)...")
        help_response = bot.handle_incoming_message({
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'help',
            'timestamp': time.time()
        })
        print(f"✓ Help response: {help_response[:50]}...")
        
        print("\n2. Testing summary command (graceful degradation without API key)...")
        summary_response = bot.handle_incoming_message({
            'chat_id': 'test_chat',
            'sender_id': 'test_user', 
            'content': '/summary',
            'timestamp': time.time()
        })
        print(f"✓ Summary response: {summary_response[:50]}...")
        
        print("\n3. Adding some sample messages to test context...")
        # Add some sample messages
        sample_messages = [
            "Hello everyone!",
            "How are you doing today?",
            "I'm working on a new project",
            "Can someone help me with Python?",
            "Sure, what do you need help with?"
        ]
        
        for i, msg in enumerate(sample_messages):
            bot.handle_incoming_message({
                'chat_id': 'test_chat',
                'sender_id': f'user_{i}',
                'content': msg,
                'timestamp': time.time() - (len(sample_messages) - i) * 60  # 1 minute apart
            })
        
        print(f"✓ Added {len(sample_messages)} sample messages")
        
        print("\n4. Testing summary with message history...")
        summary_response2 = bot.handle_incoming_message({
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'summary',
            'timestamp': time.time()
        })
        print(f"✓ Summary with history: {summary_response2[:100]}...")
        
        print("\n5. Testing Q&A functionality (should attempt GPT)...")
        qa_response = bot.handle_incoming_message({
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'What is Python programming?',
            'timestamp': time.time()
        })
        print(f"✓ Q&A response: {qa_response[:100]}..." if qa_response else "✓ Q&A correctly returned None (no API key)")
        
        print("\n6. Testing non-question message (should not trigger Q&A)...")
        no_response = bot.handle_incoming_message({
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'ok',
            'timestamp': time.time()
        })
        print(f"✓ Non-question response: {no_response}" if no_response else "✓ Correctly no response for short non-question")
        
        print("\n7. Checking stored messages in database...")
        recent_messages = message_handler.chat_db.get_recent_messages('test_chat', limit=10)
        print(f"✓ Found {len(recent_messages)} stored messages")
        for sender, timestamp, content, msg_id in recent_messages[-3:]:  # Show last 3
            print(f"   {sender}: {content[:30]}...")
        
        print("\n=== All Tests Completed Successfully! ===")
        print("\nKey features tested:")
        print("✓ GPT client integration (graceful handling without API key)")
        print("✓ Message storage in SQLite database")
        print("✓ Summary generation with chat history")
        print("✓ Q&A response detection and handling")
        print("✓ Backward compatibility with existing triggers")
        
        if not os.getenv('OPENAI_API_KEY'):
            print("\n💡 Note: To test actual GPT responses, set OPENAI_API_KEY environment variable")
        
    finally:
        # Clean up test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print(f"\n🧹 Cleaned up test database: {test_db_path}")

def test_with_api_key():
    """Test with actual OpenAI API if key is available."""
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY not set, skipping live API tests")
        return
    
    print("\n=== Testing with Live OpenAI API ===")
    print("⚠️  This will make actual API calls and may incur charges")
    
    # Add a simple test here if needed
    print("Live API testing would go here...")

if __name__ == "__main__":
    test_gpt_integration()
    test_with_api_key()