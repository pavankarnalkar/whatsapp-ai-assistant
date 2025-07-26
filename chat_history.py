"""
SQLite chat history storage and retrieval module.

This module provides functionality to store and retrieve WhatsApp chat messages
using SQLite database with the following schema:
- chat_id: Identifier for the chat/conversation
- sender: Message sender identifier  
- timestamp: Message timestamp
- content: Message text content
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional


class ChatHistoryDB:
    """SQLite database handler for chat message storage and retrieval."""
    
    def __init__(self, db_path: str = "chat_history.db"):
        """
        Initialize the chat history database.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self) -> None:
        """Initialize the database and create the messages table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    chat_id TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create index for faster queries by chat_id
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_chat_id_timestamp 
                ON messages(chat_id, timestamp DESC)
            """)
            
            conn.commit()
    
    def store_message(self, chat_id: str, sender: str, timestamp: str, content: str) -> bool:
        """
        Store a message in the database.
        
        Args:
            chat_id: Chat/conversation identifier
            sender: Message sender identifier
            timestamp: Message timestamp (ISO format recommended)
            content: Message text content
            
        Returns:
            bool: True if message was stored successfully, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO messages (chat_id, sender, timestamp, content)
                    VALUES (?, ?, ?, ?)
                """, (chat_id, sender, timestamp, content))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error storing message: {e}")
            return False
    
    def get_recent_messages(self, chat_id: str, limit: int = 50) -> List[Tuple[str, str, str, str]]:
        """
        Retrieve the most recent messages for a given chat_id.
        
        Args:
            chat_id: Chat/conversation identifier
            limit: Maximum number of messages to retrieve (default: 50)
            
        Returns:
            List of tuples containing (sender, timestamp, content, message_id)
            ordered by timestamp (most recent first)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT sender, timestamp, content, id
                    FROM messages 
                    WHERE chat_id = ?
                    ORDER BY timestamp DESC
                    LIMIT ?
                """, (chat_id, limit))
                
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error retrieving messages: {e}")
            return []
    
    def get_chat_message_count(self, chat_id: str) -> int:
        """
        Get the total number of messages for a given chat_id.
        
        Args:
            chat_id: Chat/conversation identifier
            
        Returns:
            int: Total number of messages in the chat
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT COUNT(*) FROM messages WHERE chat_id = ?
                """, (chat_id,))
                
                result = cursor.fetchone()
                return result[0] if result else 0
        except sqlite3.Error as e:
            print(f"Error counting messages: {e}")
            return 0
    
    def delete_chat_history(self, chat_id: str) -> bool:
        """
        Delete all messages for a given chat_id.
        
        Args:
            chat_id: Chat/conversation identifier
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM messages WHERE chat_id = ?", (chat_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error deleting chat history: {e}")
            return False


def create_sample_data(db: ChatHistoryDB) -> None:
    """Create some sample data for testing purposes."""
    sample_messages = [
        ("chat_001", "user_123", "2024-01-01T10:00:00Z", "Hello, how are you?"),
        ("chat_001", "user_456", "2024-01-01T10:01:00Z", "I'm doing great, thanks!"),
        ("chat_001", "user_123", "2024-01-01T10:02:00Z", "That's wonderful to hear."),
        ("chat_002", "user_789", "2024-01-01T11:00:00Z", "Anyone available for a meeting?"),
        ("chat_002", "user_123", "2024-01-01T11:01:00Z", "Yes, I'm free now."),
    ]
    
    for chat_id, sender, timestamp, content in sample_messages:
        db.store_message(chat_id, sender, timestamp, content)


if __name__ == "__main__":
    # Example usage and testing
    print("Initializing chat history database...")
    
    # Create database instance
    db = ChatHistoryDB("test_chat_history.db")
    
    # Create sample data
    print("Adding sample messages...")
    create_sample_data(db)
    
    # Test retrieving messages
    print("\nRetrieving last 50 messages for chat_001:")
    messages = db.get_recent_messages("chat_001")
    for sender, timestamp, content, msg_id in messages:
        print(f"[{timestamp}] {sender}: {content} (ID: {msg_id})")
    
    print(f"\nTotal messages in chat_001: {db.get_chat_message_count('chat_001')}")
    
    print("\nRetrieving last 50 messages for chat_002:")
    messages = db.get_recent_messages("chat_002")
    for sender, timestamp, content, msg_id in messages:
        print(f"[{timestamp}] {sender}: {content} (ID: {msg_id})")
    
    print(f"\nTotal messages in chat_002: {db.get_chat_message_count('chat_002')}")
    
    # Clean up test database
    os.remove("test_chat_history.db")
    print("\nTest completed successfully!")