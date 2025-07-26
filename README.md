# WhatsApp AI Assistant - Chat History Module

This module provides SQLite-based storage and retrieval functionality for WhatsApp chat messages.

## Features

- **Message Storage**: Store chat messages with chat_id, sender, timestamp, and content
- **Message Retrieval**: Fetch the last 50 messages (or custom limit) for any chat
- **Chat Management**: Count messages and delete chat history
- **Performance**: Indexed database for fast queries
- **Error Handling**: Robust error handling with meaningful feedback

## Database Schema

The `messages` table contains:
- `id`: Auto-incrementing primary key
- `chat_id`: Chat/conversation identifier (TEXT)
- `sender`: Message sender identifier (TEXT) 
- `timestamp`: Message timestamp in ISO format (TEXT)
- `content`: Message text content (TEXT)
- `created_at`: Database insertion timestamp (DATETIME)

## Usage

### Basic Usage

```python
from chat_history import ChatHistoryDB

# Initialize database
db = ChatHistoryDB("chat_history.db")

# Store a message
db.store_message(
    chat_id="group_123",
    sender="user_456", 
    timestamp="2024-01-15T10:30:00Z",
    content="Hello everyone!"
)

# Retrieve last 50 messages for a chat
messages = db.get_recent_messages("group_123", limit=50)
for sender, timestamp, content, msg_id in messages:
    print(f"[{timestamp}] {sender}: {content}")

# Get message count for a chat
count = db.get_chat_message_count("group_123")
print(f"Total messages: {count}")
```

### Advanced Usage

```python
# Custom database path
db = ChatHistoryDB("/path/to/your/database.db")

# Retrieve fewer messages
recent_10 = db.get_recent_messages("chat_id", limit=10)

# Delete all messages for a chat
db.delete_chat_history("old_chat_id")
```

## API Reference

### `ChatHistoryDB(db_path="chat_history.db")`
Initialize the chat history database.

### `store_message(chat_id, sender, timestamp, content) -> bool`
Store a message in the database. Returns True if successful.

### `get_recent_messages(chat_id, limit=50) -> List[Tuple]`
Retrieve recent messages for a chat. Returns list of (sender, timestamp, content, id) tuples ordered by timestamp (newest first).

### `get_chat_message_count(chat_id) -> int`
Get total number of messages for a chat.

### `delete_chat_history(chat_id) -> bool`
Delete all messages for a chat. Returns True if successful.

## Testing

Run the test suite:

```bash
python test_chat_history.py
```

Run the example with sample data:

```bash
python chat_history.py
```

## Requirements

- Python 3.6+
- SQLite3 (included with Python standard library)

No additional dependencies required.