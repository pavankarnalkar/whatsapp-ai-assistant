# WhatsApp AI Assistant - Streaming GPT Responses

A WhatsApp AI assistant that streams GPT responses with realistic typing simulation, implementing issue #16: "Stream responses from GPT to simulate typing".

## Features

### 🔄 Streaming GPT Responses
- **Real-time streaming**: GPT responses are streamed token by token
- **Typing simulation**: Realistic typing delays based on message length
- **Typing indicators**: Shows "typing..." while processing responses
- **Message chunking**: Long responses are split into multiple messages at natural breakpoints

### 📱 WhatsApp Integration
- **MCP Integration**: Works with WhatsApp MCP server for message handling
- **Webhook support**: Receives incoming messages via webhook
- **Typing indicators**: Shows and stops typing indicators via MCP API

### ⚙️ Configurable Behavior
- **Delay settings**: Customizable typing delays per word
- **Chunk sizes**: Configurable message length limits
- **Response strategies**: Automatic selection between streaming and simple responses

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pavankarnalkar/whatsapp-ai-assistant.git
   cd whatsapp-ai-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and settings
   ```
# WhatsApp AI Assistant - Urgency Detection & Email Notifications

This project implements an urgency detection system for WhatsApp messages with automatic email notifications.

## Features

- **Urgency Detection**: Automatically detects urgent messages using configurable keywords
- **Email Notifications**: Sends SMTP email alerts when urgent messages are received
- **Configurable Keywords**: Customizable urgency detection keywords
- **Comprehensive Testing**: Full test suite for all components
- **Easy Setup**: Environment-based configuration

## Quick Start

### 1. Install Dependencies

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

### 2. Configure Environment

Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

Edit `.env` with your SMTP settings:

```env
# SMTP Configuration for Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com
SMTP_TO_EMAIL=alert_recipient@gmail.com

# Urgency Detection Settings
URGENCY_KEYWORDS=urgent,asap,emergency,critical,immediate,help
```

### 3. Run the Demo

```bash
python demo.py
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

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# WhatsApp MCP Configuration  
MCP_BASE_URL=http://localhost:3000
MCP_API_KEY=your_mcp_api_key_here

# Typing Simulation Configuration
TYPING_DELAY_PER_WORD=0.1        # Delay per word (seconds)
CHUNK_SIZE=100                   # Characters per chunk
TYPING_INDICATOR_DELAY=2.0       # Initial typing indicator delay
MAX_MESSAGE_LENGTH=200           # Maximum message length before chunking
MIN_CHUNK_SIZE=50               # Minimum chunk size
```

## Usage

### Running the Assistant

**As a webhook server** (recommended for production):
```bash
python webhook_handler.py
```

**For testing and development**:
```bash
python test_streaming.py
```

**Demo mode**:
```bash
python main.py
```

### Message Flow

1. **Incoming Message**: Received via webhook from WhatsApp MCP
2. **Processing**: Message is analyzed to determine response strategy
3. **Typing Indicator**: "typing..." shown in WhatsApp chat
4. **GPT Streaming**: Response generated and streamed in real-time
5. **Message Chunking**: Long responses split at sentence boundaries
6. **Typing Simulation**: Delays calculated based on message length
7. **Message Delivery**: Chunks sent with realistic typing delays

### Response Strategies

**Streaming Response** (for complex queries):
- Used for queries with keywords: "explain", "describe", "how to", etc.
- Long user messages (>50 characters)
- Responses are streamed and chunked

**Simple Response** (for short interactions):
- Quick replies to greetings, simple questions
- Single message with typing delay

## Architecture

### Core Components

- **`typing_simulator.py`**: Main logic for streaming and typing simulation
- **`gpt_client.py`**: OpenAI GPT client with streaming support  
- **`whatsapp_client.py`**: WhatsApp MCP API client
- **`webhook_handler.py`**: HTTP webhook server for incoming messages
- **`main.py`**: Main application and demo scenarios
- **`config.py`**: Configuration management

### Key Features Implementation

**Streaming Responses**:
```python
async for chunk in self.gpt_client.stream_completion(messages):
    full_response += chunk
```

**Message Chunking**:
```python
def chunk_message(self, text: str) -> List[str]:
    sentences = re.split(r'(?<=[.!?])\s+', text)
    # Split at natural breakpoints while respecting length limits
```

**Typing Simulation**:
```python
def calculate_typing_delay(self, text: str) -> float:
    word_count = len(text.split())
    return word_count * self.config.TYPING_DELAY_PER_WORD
```

**Typing Indicators**:
```python
await whatsapp_client.send_typing_indicator(chat_id)
await asyncio.sleep(typing_delay)
await whatsapp_client.stop_typing_indicator(chat_id)
```

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
from src import MessageProcessor

# Initialize the processor
processor = MessageProcessor()

# Process a message
message_data = {
    'text': 'This is urgent! Need help ASAP!',
    'sender': 'john_doe',
    'chat_id': 'family_chat',
    'timestamp': datetime.now()
}

result = processor.process_message(message_data)

if result['is_urgent']:
    print(f"Urgent message detected! Keywords: {result['matched_keywords']}")
    print(f"Email sent: {result['email_sent']}")
```

### Urgency Detection Only

```python
from src import UrgencyDetector

detector = UrgencyDetector()

# Check if message is urgent
is_urgent = detector.is_urgent("This is urgent!")
keywords = detector.get_matched_keywords("Help! Emergency situation!")

print(f"Urgent: {is_urgent}")
print(f"Keywords found: {keywords}")
```

### Email Notifications Only

```python
from src import EmailNotifier

notifier = EmailNotifier()

# Send urgent alert
message_data = {
    'text': 'Emergency! System down!',
    'sender': 'admin',
    'matched_keywords': ['emergency']
}

success = notifier.send_urgent_alert(message_data)
print(f"Email sent: {success}")
```

## Configuration

### SMTP Settings

The system supports various SMTP providers. Here are common configurations:

#### Gmail
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

#### Outlook/Hotmail
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USERNAME=your_email@outlook.com
SMTP_PASSWORD=your_password
```

#### Yahoo
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USERNAME=your_email@yahoo.com
SMTP_PASSWORD=your_app_password
```

### Urgency Keywords

Configure detection keywords in the `.env` file:

```env
URGENCY_KEYWORDS=urgent,asap,emergency,critical,immediate,help,priority,rush
```

Keywords are:
- Case-insensitive
- Matched as whole words (word boundaries)
- Comma-separated in configuration

## Testing

### Run All Tests

```bash
python tests/run_tests.py
```

### Run Individual Test Suites

```bash
# Test urgency detection
python -m unittest tests.test_urgency_detector

# Test email notifications
python -m unittest tests.test_email_notifier

# Test message processing
python -m unittest tests.test_message_processor
```

### Test Email Configuration

Use the demo script to test your email configuration:

```bash
python demo.py
```

Then type `test` to send a test urgent message.

## API Reference

### MessageProcessor

Main class for processing WhatsApp messages.

#### Methods

- `process_message(message_data: Dict[str, Any]) -> Dict[str, Any]`
  - Processes a message and returns urgency detection and email results
  - Required: `message_data['text']`
  - Optional: `sender`, `chat_id`, `timestamp`

- `test_system() -> Dict[str, Any]`
  - Runs system tests for urgency detection and email configuration

### UrgencyDetector

Detects urgent messages based on keywords.

#### Methods

- `is_urgent(message: str) -> bool`
  - Returns True if message contains urgent keywords

- `get_matched_keywords(message: str) -> List[str]`
  - Returns list of matched urgency keywords

### EmailNotifier

Sends email notifications for urgent messages.

#### Methods

- `send_urgent_alert(message_data: Dict[str, Any]) -> bool`
  - Sends email alert for urgent message
  - Returns True if successful

- `test_email_configuration() -> bool`
  - Tests SMTP configuration by sending test email

## Error Handling

The system includes comprehensive error handling:

- **Invalid message data**: Returns error in result
- **SMTP configuration missing**: Logs error and returns False
- **Email sending failure**: Logs error but continues processing
- **Network issues**: Gracefully handles SMTP connection errors

## Security Considerations

- Store SMTP credentials in environment variables, not in code
- Use app passwords for Gmail (not your main password)
- Ensure `.env` file is in `.gitignore`
- Consider rate limiting for email notifications in production

## Integration with WhatsApp

This urgency detection system is designed to integrate with:

1. **whatsapp-mcp server**: For receiving WhatsApp messages
2. **Webhook endpoints**: For real-time message processing
3. **Database storage**: For message history and analytics
4. **LLM integration**: For advanced message analysis

See the `github_issues_whatsapp_mcp (1).json` file for the complete roadmap.

## Troubleshooting

### Common Issues

1. **Email not sending**
   - Check SMTP credentials
   - Verify network connectivity
   - Enable "Less secure app access" or use app passwords

2. **Keywords not detected**
   - Verify keyword configuration
   - Check for typos in keywords
   - Ensure keywords are comma-separated

3. **Import errors**
   - Ensure you're running from the project root
   - Check Python path configuration

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

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
# Test without API calls
python test_streaming.py

# Test with OpenAI API integration
python test_streaming.py --with-api
```

Test features:
- ✅ Message chunking at sentence boundaries
- ✅ Typing delay calculation
- ✅ Streaming response simulation
- ✅ WhatsApp MCP client integration

## MCP Integration

The assistant integrates with [whatsapp-mcp](https://github.com/lharries/whatsapp-mcp) server:

**Webhook Endpoint**: `POST /webhook/message`
```json
{
  "chat_id": "123456789",
  "sender_id": "user123", 
  "message": {"text": "Hello!"},
  "timestamp": "2023-12-01T10:00:00Z"
}
```

**MCP API Calls**:
- `POST /typing` - Send/stop typing indicators
- `POST /message` - Send messages to chats

## Examples

### Streaming Long Response
```
User: "Explain how machine learning works"
Bot: [typing...] (2 seconds)
Bot: "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed."
Bot: [typing...] (1.5 seconds) 
Bot: "It works by using algorithms to identify patterns in large datasets, then applies these patterns to make predictions or decisions on new data."
Bot: [typing...] (1.2 seconds)
Bot: "Common examples include recommendation systems, image recognition, and natural language processing."
```

### Simple Response
```
User: "Hello!"
Bot: [typing...] (0.8 seconds)
Bot: "Hi there! How can I help you today?"
```
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
4. Test thoroughly
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is part of the WhatsApp AI Assistant implementation for issue #16.
This project is open source and available under the MIT License.
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
