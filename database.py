import sqlite3
import logging
from datetime import datetime
from typing import List, Optional
from models import MessagePayload, StoredMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_PATH = "messages.db"


def init_database():
    """Initialize the SQLite database and create tables"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id TEXT NOT NULL,
                chat_id TEXT NOT NULL,
                timestamp DATETIME NOT NULL,
                message_text TEXT NOT NULL,
                message_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes for better query performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_chat_id ON messages(chat_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON messages(timestamp)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sender_id ON messages(sender_id)")
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise


def store_message(message: MessagePayload) -> int:
    """Store a message in the database and return the row ID"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (sender_id, chat_id, timestamp, message_text, message_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            message.sender_id,
            message.chat_id,
            message.timestamp,
            message.message_text,
            message.message_id
        ))
        
        row_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        logger.info(f"Message stored successfully with ID: {row_id}")
        return row_id
        
    except Exception as e:
        logger.error(f"Error storing message: {e}")
        raise


def get_messages_by_chat(chat_id: str, limit: int = 50) -> List[StoredMessage]:
    """Retrieve messages for a specific chat ID"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, sender_id, chat_id, timestamp, message_text, message_id, created_at
            FROM messages
            WHERE chat_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (chat_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        messages = []
        for row in rows:
            messages.append(StoredMessage(
                id=row[0],
                sender_id=row[1],
                chat_id=row[2],
                timestamp=datetime.fromisoformat(row[3]) if isinstance(row[3], str) else row[3],
                message_text=row[4],
                message_id=row[5],
                created_at=datetime.fromisoformat(row[6]) if isinstance(row[6], str) else row[6]
            ))
        
        return messages
        
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        raise


def get_message_count() -> int:
    """Get total count of messages in database"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
        
    except Exception as e:
        logger.error(f"Error getting message count: {e}")
        raise