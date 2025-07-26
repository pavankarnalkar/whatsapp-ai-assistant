"""
Test script for chat_history module.

This script demonstrates and validates the chat history storage and retrieval functionality.
"""

import os
import tempfile
from datetime import datetime, timedelta
from chat_history import ChatHistoryDB


def test_chat_history():
    """Test the chat history functionality with various scenarios."""
    
    # Use a temporary database file for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as temp_db:
        db_path = temp_db.name
    
    try:
        print("=== Testing Chat History Database ===\n")
        
        # Initialize database
        db = ChatHistoryDB(db_path)
        print("✓ Database initialized successfully")
        
        # Test 1: Store messages
        print("\n1. Testing message storage...")
        test_messages = [
            ("group_chat", "alice", "2024-01-15T09:00:00Z", "Good morning everyone!"),
            ("group_chat", "bob", "2024-01-15T09:01:00Z", "Morning Alice! How's everyone doing?"),
            ("group_chat", "charlie", "2024-01-15T09:02:00Z", "All good here, ready for the meeting"),
            ("group_chat", "alice", "2024-01-15T09:03:00Z", "Perfect! Let's start in 5 minutes"),
            ("private_chat", "alice", "2024-01-15T10:00:00Z", "Hey, can we talk privately?"),
            ("private_chat", "david", "2024-01-15T10:01:00Z", "Sure, what's up?"),
        ]
        
        for chat_id, sender, timestamp, content in test_messages:
            success = db.store_message(chat_id, sender, timestamp, content)
            if not success:
                print(f"✗ Failed to store message from {sender}")
                return False
        
        print(f"✓ Successfully stored {len(test_messages)} messages")
        
        # Test 2: Retrieve messages for group_chat
        print("\n2. Testing message retrieval for group_chat...")
        messages = db.get_recent_messages("group_chat", limit=50)
        
        if len(messages) != 4:
            print(f"✗ Expected 4 messages, got {len(messages)}")
            return False
        
        print(f"✓ Retrieved {len(messages)} messages for group_chat")
        
        # Verify messages are in reverse chronological order (most recent first)
        print("   Messages (most recent first):")
        for i, (sender, timestamp, content, msg_id) in enumerate(messages):
            print(f"   {i+1}. [{timestamp}] {sender}: {content}")
        
        # Test 3: Retrieve messages for private_chat
        print("\n3. Testing message retrieval for private_chat...")
        private_messages = db.get_recent_messages("private_chat", limit=50)
        
        if len(private_messages) != 2:
            print(f"✗ Expected 2 messages, got {len(private_messages)}")
            return False
        
        print(f"✓ Retrieved {len(private_messages)} messages for private_chat")
        
        # Test 4: Test limit functionality
        print("\n4. Testing message limit...")
        limited_messages = db.get_recent_messages("group_chat", limit=2)
        
        if len(limited_messages) != 2:
            print(f"✗ Expected 2 messages with limit, got {len(limited_messages)}")
            return False
        
        print("✓ Message limit working correctly")
        
        # Test 5: Test message count functionality
        print("\n5. Testing message count...")
        group_count = db.get_chat_message_count("group_chat")
        private_count = db.get_chat_message_count("private_chat")
        nonexistent_count = db.get_chat_message_count("nonexistent_chat")
        
        if group_count != 4:
            print(f"✗ Expected 4 messages in group_chat, got {group_count}")
            return False
        
        if private_count != 2:
            print(f"✗ Expected 2 messages in private_chat, got {private_count}")
            return False
        
        if nonexistent_count != 0:
            print(f"✗ Expected 0 messages in nonexistent_chat, got {nonexistent_count}")
            return False
        
        print("✓ Message counting working correctly")
        
        # Test 6: Test with exactly 50 messages to verify limit
        print("\n6. Testing with 50+ messages...")
        
        # Add 50 more messages to group_chat
        base_time = datetime.fromisoformat("2024-01-15T12:00:00")
        for i in range(50):
            timestamp = (base_time + timedelta(minutes=i)).isoformat() + "Z"
            content = f"Test message number {i+1}"
            db.store_message("group_chat", f"user_{i%3}", timestamp, content)
        
        # Should now have 54 total messages (4 original + 50 new)
        total_count = db.get_chat_message_count("group_chat")
        if total_count != 54:
            print(f"✗ Expected 54 total messages, got {total_count}")
            return False
        
        # Retrieving with limit=50 should return exactly 50 messages
        recent_50 = db.get_recent_messages("group_chat", limit=50)
        if len(recent_50) != 50:
            print(f"✗ Expected 50 messages with limit, got {len(recent_50)}")
            return False
        
        print("✓ Limit of 50 messages working correctly")
        
        # Test 7: Test chat deletion
        print("\n7. Testing chat deletion...")
        deletion_success = db.delete_chat_history("private_chat")
        
        if not deletion_success:
            print("✗ Failed to delete chat history")
            return False
        
        remaining_count = db.get_chat_message_count("private_chat")
        if remaining_count != 0:
            print(f"✗ Expected 0 messages after deletion, got {remaining_count}")
            return False
        
        print("✓ Chat deletion working correctly")
        
        print("\n=== All Tests Passed Successfully! ===")
        return True
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        return False
    
    finally:
        # Clean up test database
        if os.path.exists(db_path):
            os.remove(db_path)


if __name__ == "__main__":
    success = test_chat_history()
    exit(0 if success else 1)