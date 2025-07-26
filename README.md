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
