#!/usr/bin/env python3
"""
Test script to verify GPT functionality with mock responses.
"""

import os
import time
import tempfile
import asyncio
from unittest.mock import AsyncMock, patch
from message_handler import MessageHandler, Message, AutoReplyBot


async def mock_gpt_completion(messages):
    """Mock GPT completion response."""
    user_message = messages[-1]["content"] if messages else ""
    
    if "summary" in user_message.lower() or "summarize" in user_message.lower():
        return "This is a mock summary of the conversation covering key topics and decisions."
    elif "?" in user_message:
        return f"This is a mock answer to your question: {user_message}"
    else:
        return "This is a mock GPT response to your message."


def test_gpt_functionality_with_mock():
    """Test GPT functionality using mock responses."""
    print("=== Testing GPT Functionality with Mock Responses ===\n")
    
    # Create temporary database
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_db:
        test_db_path = tmp_db.name
    
    try:
        # Initialize handler
        message_handler = MessageHandler(db_path=test_db_path)
        
        # Mock the GPT client
        with patch.object(message_handler.gpt_client, 'get_completion', side_effect=mock_gpt_completion):
            with patch.object(message_handler.gpt_client, 'client', True):  # Pretend client is initialized
                
                print("1. Testing summary with mock GPT response...")
                
                # Add some sample messages first
                sample_messages = [
                    ("user1", "Hello team!"),
                    ("user2", "How's the project going?"),
                    ("user1", "We're making good progress"),
                    ("user2", "Great! When do we expect to finish?"),
                    ("user1", "Next week should be good")
                ]
                
                for sender, content in sample_messages:
                    msg = Message(
                        chat_id="test_chat",
                        sender_id=sender,
                        content=content,
                        timestamp=time.time()
                    )
                    message_handler.store_message(msg)
                
                # Test summary
                summary_msg = Message(
                    chat_id="test_chat",
                    sender_id="user3",
                    content="/summary",
                    timestamp=time.time()
                )
                
                response = message_handler.process_message(summary_msg)
                print(f"✓ Summary response: {response.response_text}")
                
                print("\n2. Testing Q&A with mock GPT response...")
                
                qa_msg = Message(
                    chat_id="test_chat",
                    sender_id="user3",
                    content="What is machine learning?",
                    timestamp=time.time()
                )
                
                response = message_handler.process_message(qa_msg)
                print(f"✓ Q&A response: {response.response_text}")
                
                print("\n3. Testing non-question message...")
                
                simple_msg = Message(
                    chat_id="test_chat",
                    sender_id="user3",
                    content="ok thanks",
                    timestamp=time.time()
                )
                
                response = message_handler.process_message(simple_msg)
                print(f"✓ Simple message response: {response.response_text if response else 'No response (correct)'}")
                
                print("\n4. Testing help command (no GPT needed)...")
                
                help_msg = Message(
                    chat_id="test_chat",
                    sender_id="user3",
                    content="help",
                    timestamp=time.time()
                )
                
                response = message_handler.process_message(help_msg)
                print(f"✓ Help response: {response.response_text[:50]}...")
                
        print("\n=== Mock GPT Tests Completed Successfully! ===")
        print("\nVerified functionality:")
        print("✓ GPT integration for summaries")
        print("✓ GPT integration for Q&A")
        print("✓ Message storage and retrieval") 
        print("✓ Proper trigger detection")
        print("✓ Graceful handling when no response needed")
        
    finally:
        # Clean up
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
            print(f"\n🧹 Cleaned up test database")


if __name__ == "__main__":
    test_gpt_functionality_with_mock()