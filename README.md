# WhatsApp AI Assistant

A Python-based WhatsApp AI assistant that provides auto-reply functionality for specific triggers.

## Features

### Auto-Reply Triggers

- **Help Commands**: Responds to `help`, `/help`, `commands`, `/commands` with a comprehensive help message
- **Summary Commands**: Responds to `/summary`, `summary`, `/summarize` with chat summaries (GPT integration planned)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pavankarnalkar/whatsapp-ai-assistant.git
cd whatsapp-ai-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (optional):
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Demo

```bash
python main.py
```

This will demonstrate the auto-reply functionality with example messages.

### Integration with WhatsApp MCP

The bot is designed to integrate with [whatsapp-mcp](https://github.com/lharries/whatsapp-mcp). 

1. Set up the WhatsApp MCP server
2. Configure webhook endpoint to receive messages
3. Use `AutoReplyBot.handle_incoming_message()` to process messages

Example integration:
```python
from message_handler import AutoReplyBot

bot = AutoReplyBot()

# Handle incoming message from webhook
message_data = {
    'chat_id': 'chat_123',
    'sender_id': 'user_456', 
    'content': 'help',
    'timestamp': time.time(),
    'message_id': 'msg_1'
}

response = bot.handle_incoming_message(message_data)
if response:
    # Send response back via MCP API
    send_message_via_mcp(message_data['chat_id'], response)
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for GPT integration
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-3.5-turbo)
- `MCP_BASE_URL`: WhatsApp MCP server URL (default: http://localhost:8000)
- `MCP_API_KEY`: API key for WhatsApp MCP
- `MAX_SUMMARY_MESSAGES`: Number of messages to include in summaries (default: 20)
- `RESPONSE_DELAY`: Delay before sending responses in seconds (default: 1.0)

### Trigger Configuration

Triggers can be customized in `config.py`:
- `HELP_TRIGGERS`: Keywords that trigger help responses
- `SUMMARY_TRIGGERS`: Keywords that trigger summary responses
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
# WhatsApp AI Assistant

A Python-based WhatsApp AI Assistant that integrates with the whatsapp-mcp server to send automated replies to incoming messages.

## Features

- **MCP REST API Integration**: Send messages via the MCP `/message` endpoint
- **Webhook Listener**: Receive incoming WhatsApp messages from MCP server
- **Static Auto-Replies**: Automatic responses to common keywords
- **Manual Message Sending**: REST endpoint for sending custom messages

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your MCP server details
   ```

3. **Set Environment Variables**:
   - `MCP_BASE_URL`: Base URL of your MCP server (default: http://localhost:3000)
   - `MCP_API_KEY`: API key for MCP authentication (optional)
   - `PORT`: Port to run the webhook server (default: 5000)
   - `DEBUG`: Enable debug mode (default: False)

## Usage

### Start the Application

```bash
python app.py
```

The application will start on `http://localhost:5000` (or the port specified in the PORT environment variable).

### Endpoints

#### 1. Webhook Endpoint
- **URL**: `POST /webhook`
- **Purpose**: Receives incoming WhatsApp messages from MCP server
- **Payload**:
  ```json
  {
    "sender": "recipient_phone_number",
    "chat_id": "chat_identifier",
    "text": "incoming message text",
    "timestamp": "2024-01-01T12:00:00Z"
  }
  ```

#### 2. Manual Message Sending
- **URL**: `POST /send-message`
- **Purpose**: Send custom messages via MCP API
- **Payload**:
  ```json
  {
    "recipient": "recipient_id",
    "text": "Your message text"
  }
  ```

#### 3. Health Check
- **URL**: `GET /health`
- **Purpose**: Check if the service is running

### Static Replies

The assistant automatically responds to certain keywords:
- `help` → "Hello! I am your WhatsApp AI Assistant. You can ask me anything!"
- `hello` → "Hi there! How can I help you today?"
- `hi` → "Hello! Nice to meet you!"
- Other messages → "Thanks for your message! This is an automated reply from your AI Assistant."

## Testing

Run the test suite:
```bash
python -m pytest tests/
```

Or run individual test files:
```bash
python -m unittest tests.test_message_handler
```

## Project Structure

```
├── main.py                 # Entry point and demo
├── message_handler.py      # Core message processing logic
├── responses.py           # Predefined response templates
├── config.py             # Configuration management
├── requirements.txt      # Python dependencies
├── tests/               # Test suite
│   └── test_message_handler.py
├── .gitignore          # Git ignore patterns
└── README.md          # This file
```

## Roadmap

- [x] Auto-reply to help triggers
- [x] Auto-reply to summary triggers (placeholder)
- [ ] Full GPT integration for summaries
- [ ] Message storage and retrieval
- [ ] WhatsApp MCP webhook integration
- [ ] Urgent message detection
- [ ] Email notifications
- [ ] Response streaming for long messages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is open source and available under the MIT License.

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
python test_app.py
```

### Manual Testing

1. **Test Webhook**:
   ```bash
   curl -X POST http://localhost:5000/webhook \
     -H "Content-Type: application/json" \
     -d '{"sender": "test_user", "text": "hello", "timestamp": "2024-01-01T12:00:00Z"}'
   ```

2. **Test Manual Sending**:
   ```bash
   curl -X POST http://localhost:5000/send-message \
     -H "Content-Type: application/json" \
     -d '{"recipient": "test_recipient", "text": "Hello from the assistant!"}'
   ```

## Integration with whatsapp-mcp

To integrate with the whatsapp-mcp server:

1. Set up and run the whatsapp-mcp server
2. Configure the MCP server to send webhooks to your assistant's `/webhook` endpoint
3. Update the `MCP_BASE_URL` in your `.env` file to point to the MCP server

## Architecture

- **`mcp_client.py`**: Core MCP REST API client for sending messages
- **`app.py`**: Flask application with webhook listener and auto-reply logic
- **`test_app.py`**: Test suite for validating functionality

## Requirements

- Python 3.7+
- Flask 2.3+
- requests 2.31+
- python-dotenv 1.0+
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
# WhatsApp AI Assistant

This project sets up a WhatsApp AI assistant using the WhatsApp MCP (Model Context Protocol) server. It allows you to interact with WhatsApp through Claude Desktop or other MCP-compatible clients.

## Architecture

The system consists of two main components:

1. **WhatsApp Bridge** (Go): Connects to WhatsApp Web API, handles authentication, and stores message history in SQLite
2. **MCP Server** (Python): Provides standardized tools for Claude to interact with WhatsApp data

## Quick Start

### Prerequisites

- Go 1.24+
- Python 3.11+
- Claude Desktop app (optional, for integration)

### 1. Setup

Run the setup script to install all dependencies:

```bash
./setup.sh
```

This will:
- Initialize the WhatsApp MCP submodule
- Install Go dependencies
- Install Python dependencies (including uv package manager)

**Note**: If you cloned this repository, the WhatsApp MCP submodule is automatically included. The setup script will ensure it's properly initialized.

### 2. Start WhatsApp Bridge

Start the WhatsApp bridge to authenticate with WhatsApp:

```bash
./start-bridge.sh
```

**Important**: On first run, you'll see a QR code in your terminal. Scan this QR code with your WhatsApp mobile app:

1. Open WhatsApp on your phone
2. Go to Settings > Linked Devices
3. Tap "Link a Device"
4. Scan the QR code displayed in your terminal

After scanning, your session will be saved and you won't need to scan again unless you log out or after ~20 days.

### 3. Start MCP Server

In a new terminal, start the MCP server:

```bash
./start-mcp-server.sh
```

### 4. Configure Claude Desktop (Optional)

To integrate with Claude Desktop, you need to configure the MCP server. First, get the required paths:

```bash
# Get the uv path
which uv

# Get the current directory path
pwd
```

Then create/edit your Claude Desktop configuration file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`

Add this configuration (replace `{{PATH_TO_UV}}` and `{{PATH_TO_SRC}}` with actual paths):

```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "{{PATH_TO_UV}}",
      "args": [
        "--directory",
        "{{PATH_TO_SRC}}/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

Example configuration:
```json
{
  "mcpServers": {
    "whatsapp": {
      "command": "/home/runner/.local/bin/uv",
      "args": [
        "--directory",
        "/home/runner/work/whatsapp-ai-assistant/whatsapp-ai-assistant/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```

After configuring, restart Claude Desktop to load the WhatsApp integration.

## Available MCP Tools

Once connected, Claude can use these WhatsApp tools:

- **search_contacts**: Search for contacts by name or phone number
- **list_messages**: Retrieve messages with optional filters
- **list_chats**: List available chats with metadata
- **get_chat**: Get information about a specific chat
- **send_message**: Send WhatsApp messages
- **send_file**: Send media files (images, videos, documents)
- **send_audio_message**: Send voice messages
- **download_media**: Download media from messages

## Troubleshooting

### QR Code Issues
- If QR code doesn't appear, restart the bridge script
- Ensure your terminal supports QR code display
- Check that WhatsApp hasn't reached the linked device limit

### Authentication Issues
- Delete `whatsapp-mcp/whatsapp-bridge/store/*.db` files and restart to re-authenticate
- Ensure WhatsApp Web is working in your browser first

### Dependencies
- If `uv` command not found, run `pip3 install uv`
- For Go dependency issues, run `go mod tidy` in the whatsapp-bridge directory

## Security Note

⚠️ **Important**: This MCP server connects to your personal WhatsApp account. All messages are stored locally in SQLite databases and only sent to Claude when you explicitly use the tools. However, be aware of potential data privacy implications when using AI assistants with personal data.

## Project Structure

```
whatsapp-ai-assistant/
├── setup.sh                 # Main setup script
├── start-bridge.sh          # Start WhatsApp bridge
├── start-mcp-server.sh      # Start MCP server
├── README.md               # This file
└── whatsapp-mcp/           # Cloned WhatsApp MCP repository
    ├── whatsapp-bridge/    # Go WhatsApp bridge
    └── whatsapp-mcp-server/ # Python MCP server
```

## Next Steps

This is the foundation for building WhatsApp AI assistant features. Future issues will add:

- Webhook listeners for real-time message processing
- SQLite integration for chat history storage
- OpenAI GPT integration for intelligent responses
- Automated reply triggers
- Email notifications for urgent messages

## License

This project uses the WhatsApp MCP server from [lharries/whatsapp-mcp](https://github.com/lharries/whatsapp-mcp). See their repository for license information.
