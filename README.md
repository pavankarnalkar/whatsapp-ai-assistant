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