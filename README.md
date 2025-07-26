# WhatsApp AI Assistant

A webhook-based AI assistant that integrates with WhatsApp through the MCP (Model Context Protocol) server.

## Features

- Webhook server to receive WhatsApp messages from MCP
- ngrok tunnel integration for local development
- Automatic MCP webhook configuration
- Health check endpoints
- Environment-based configuration

## Quick Start

### Prerequisites

- Python 3.7+
- ngrok account (free tier available at [ngrok.com](https://ngrok.com))
- whatsapp-mcp server running (see [whatsapp-mcp](https://github.com/lharries/whatsapp-mcp))

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pavankarnalkar/whatsapp-ai-assistant.git
cd whatsapp-ai-assistant
```

2. Validate your setup (optional but recommended):
```bash
python3 validate_setup.py
```

3. Run the setup script:
```bash
./setup_tunnel.sh
```

4. Configure your environment:
   - The script will create a `.env` file from the template
   - Add your ngrok auth token (required)
   - Optionally configure MCP server URL and other settings

5. The script will automatically:
   - Install Python dependencies
   - Start the webhook server
   - Create an ngrok tunnel
   - Attempt to configure the MCP webhook

## Manual Setup

If you prefer manual setup:

### 1. Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

Copy the example environment file and edit it:
```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Required
NGROK_AUTH_TOKEN=your_ngrok_auth_token_here

# Optional
MCP_SERVER_URL=http://localhost:3000
WEBHOOK_PORT=5000
NGROK_SUBDOMAIN=your-subdomain  # Paid plans only
```

### 3. Start the Webhook Server

```bash
python3 app.py
```

The server will start on the port specified in `WEBHOOK_PORT` (default: 5000).

### 4. Start ngrok Tunnel

In a separate terminal:
```bash
python3 ngrok_tunnel.py
```

This will:
- Start an ngrok tunnel pointing to your webhook server
- Display the public webhook URL
- Attempt to configure the MCP server automatically
- Keep the tunnel alive until you press Ctrl+C

## API Endpoints

### Health Check
```
GET /health
```
Returns server status and timestamp.

### Webhook Endpoint
```
POST /webhook
```
Receives WhatsApp messages from MCP server.

Expected payload:
```json
{
  "chatId": "string",
  "senderId": "string", 
  "message": "string",
  "timestamp": "ISO8601"
}
```

### Webhook Verification
```
GET /webhook?challenge=<challenge>
```
Used by some webhook systems for verification.

## MCP Integration

### Automatic Configuration

The ngrok tunnel script will attempt to automatically configure your MCP server by sending a POST request to:
```
POST {MCP_SERVER_URL}/config/webhook
```

With payload:
```json
{
  "webhook_url": "https://your-ngrok-url.ngrok.io/webhook",
  "events": ["message_received"]
}
```

### Manual Configuration

If automatic configuration fails, manually configure your MCP server to send webhooks to:
```
https://your-ngrok-url.ngrok.io/webhook
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NGROK_AUTH_TOKEN` | Yes | - | Your ngrok authentication token |
| `MCP_SERVER_URL` | No | `http://localhost:3000` | URL of your MCP server |
| `WEBHOOK_PORT` | No | `5000` | Port for the webhook server |
| `NGROK_SUBDOMAIN` | No | - | Custom subdomain (paid plans only) |
| `FLASK_DEBUG` | No | `False` | Enable Flask debug mode |

## Validation

Before setting up the tunnel, you can validate your configuration:

```bash
python3 validate_setup.py
```

This will check:
- Required Python dependencies
- Environment configuration
- ngrok availability
- Webhook server functionality

## Development

### Testing the Webhook

You can test the webhook endpoint manually:

```bash
curl -X POST http://localhost:5000/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "test-chat",
    "senderId": "test-sender",
    "message": "Hello, World!",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

### Testing via ngrok

Once the tunnel is running, test the public endpoint:

```bash
curl -X POST https://your-ngrok-url.ngrok.io/webhook \
  -H "Content-Type: application/json" \
  -d '{
    "chatId": "test-chat",
    "senderId": "test-sender", 
    "message": "Hello via ngrok!",
    "timestamp": "2024-01-01T12:00:00Z"
  }'
```

## Troubleshooting

### ngrok Auth Token Issues
- Ensure you have a valid ngrok account
- Get your auth token from [ngrok dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)
- Verify the token is correctly set in `.env`

### MCP Connection Issues
- Verify MCP server is running on the specified URL
- Check if MCP server has the correct API endpoints
- Manual webhook configuration may be required

### Port Conflicts
- Change `WEBHOOK_PORT` in `.env` if port 5000 is in use
- Restart both the webhook server and ngrok tunnel after changes

### Webhook Not Receiving Messages
- Verify the ngrok tunnel is active and accessible
- Check MCP server webhook configuration
- Review webhook server logs for errors

## Next Steps

This webhook server provides the foundation for:
- Message processing and storage
- AI-powered responses using OpenAI GPT
- Auto-replies based on triggers
- Message summarization
- Urgent message detection

See the project issues for planned features and enhancements.

## License

This project is open source. See LICENSE file for details.