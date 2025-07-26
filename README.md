# WhatsApp AI Assistant Webhook

A webhook listener for receiving MCP messages from WhatsApp and storing them in SQLite.

## Features

- **FastAPI-based webhook endpoint** for receiving WhatsApp messages from MCP
- **Flexible message parsing** supporting multiple payload formats
- **SQLite database storage** for persistent message history
- **RESTful API** for retrieving stored messages
- **Comprehensive error handling** and logging
- **Statistics endpoint** for monitoring

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the webhook server:
```bash
python main.py
```

The server will start on `http://localhost:8000` and automatically initialize the SQLite database.

## API Endpoints

### Health Check
```http
GET /
```
Returns server status and timestamp.

### Webhook Endpoint
```http
POST /webhook/message
```
Receives WhatsApp message payloads from MCP. Supports multiple message formats:

**Standard format:**
```json
{
  "sender_id": "1234567890",
  "chat_id": "chat_abc123",
  "timestamp": "2025-07-26T12:25:00Z",
  "message_text": "Hello world!",
  "message_id": "msg_001"
}
```

**Alternative formats:**
```json
{
  "from": "1234567890",
  "chatId": "chat_abc123",
  "time": 1705994700,
  "body": "Hello world!",
  "id": "msg_001"
}
```

### Get Messages
```http
GET /messages/{chat_id}?limit=50
```
Retrieve messages for a specific chat ID (up to 1000 messages).

### Statistics
```http
GET /stats
```
Get total message count and server statistics.

## Message Storage

Messages are stored in SQLite with the following schema:

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id TEXT NOT NULL,
    chat_id TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    message_text TEXT NOT NULL,
    message_id TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Testing

Run the automated test suite:
```bash
python test_webhook.py
```

Or test manually with curl:
```bash
# Send a test message
curl -X POST "http://localhost:8000/webhook/message" \
  -H "Content-Type: application/json" \
  -d '{
    "sender_id": "1234567890",
    "chat_id": "chat_abc123",
    "timestamp": "2025-07-26T12:25:00Z",
    "message_text": "Hello, this is a test message!",
    "message_id": "msg_001"
  }'

# Get messages for a chat
curl "http://localhost:8000/messages/chat_abc123"

# Check statistics
curl "http://localhost:8000/stats"
```

## Configuration with MCP

To connect this webhook with whatsapp-mcp:

1. Start the webhook server (it runs on port 8000 by default)
2. Use ngrok or similar to expose the webhook publicly:
   ```bash
   ngrok http 8000
   ```
3. Configure whatsapp-mcp to send webhooks to your ngrok URL:
   ```
   https://your-ngrok-url.ngrok.io/webhook/message
   ```

## Error Handling

The webhook includes comprehensive error handling:

- **400 Bad Request**: Missing required fields (sender_id, chat_id, message_text)
- **500 Internal Server Error**: Database or server errors
- **Detailed logging**: All requests and errors are logged for debugging

## File Structure

```
├── main.py              # FastAPI application with webhook endpoint
├── models.py            # Pydantic models for data validation
├── database.py          # SQLite database operations
├── requirements.txt     # Python dependencies
├── test_webhook.py      # Automated test suite
├── .gitignore          # Git ignore rules
└── README.md           # This file
```