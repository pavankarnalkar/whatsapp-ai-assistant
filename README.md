# WhatsApp AI Assistant

A Flask-based backend for a WhatsApp AI assistant that integrates with MCP (Message Control Protocol) to receive and send WhatsApp messages, process them with OpenAI's GPT, and store conversation history.

## Features

- **Webhook Integration**: Receives messages from whatsapp-mcp via HTTP webhooks
- **AI Processing**: Uses OpenAI GPT-3.5-turbo for intelligent responses
- **Message Storage**: SQLite database for conversation history
- **Command Support**: Built-in commands like `/help` and `/summary`
- **Urgent Message Detection**: Automatically flags and responds to urgent messages
- **Health Monitoring**: Health check endpoint for deployment monitoring

## API Endpoints

- `GET /health` - Health check endpoint
- `POST /webhook` - Webhook endpoint for receiving messages from MCP
- `POST /send` - Manual endpoint to send messages
- `GET /messages/<chat_id>` - Retrieve message history for a chat

## Local Development

### Prerequisites

- Python 3.11+
- OpenAI API key
- whatsapp-mcp server running

### Setup

1. Clone the repository:
```bash
git clone https://github.com/pavankarnalkar/whatsapp-ai-assistant.git
cd whatsapp-ai-assistant
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000` by default.

## Deployment

This application is configured for deployment on Railway and Fly.io with HTTPS support.

### Railway Deployment

1. **Connect Repository**: Connect your GitHub repository to Railway
2. **Set Environment Variables**:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `MCP_BASE_URL`: URL of your MCP server (if different from default)
   - `PORT`: Will be automatically set by Railway

3. **Deploy**: Railway will automatically build and deploy using the Dockerfile

4. **Configure MCP Webhook**: Update your MCP configuration to use the Railway HTTPS URL:
   ```
   https://your-app-name.railway.app/webhook
   ```

### Fly.io Deployment

1. **Install Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Login to Fly.io**:
```bash
flyctl auth login
```

3. **Launch Application**:
```bash
flyctl launch
```

4. **Set Environment Variables**:
```bash
flyctl secrets set OPENAI_API_KEY=your_openai_api_key_here
flyctl secrets set MCP_BASE_URL=https://your-mcp-server.com
```

5. **Deploy**:
```bash
flyctl deploy
```

6. **Configure MCP Webhook**: Update your MCP configuration to use the Fly.io HTTPS URL:
   ```
   https://your-app-name.fly.dev/webhook
   ```

### Environment Variables

Required environment variables for production:

- `OPENAI_API_KEY`: Your OpenAI API key for GPT responses
- `MCP_BASE_URL`: Base URL of your MCP server (defaults to http://localhost:3000)
- `PORT`: Server port (automatically set by hosting platforms)
- `DATABASE_PATH`: SQLite database file path (defaults to ./messages.db)

## Docker

Build and run with Docker:

```bash
# Build the image
docker build -t whatsapp-ai-assistant .

# Run the container
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -e MCP_BASE_URL=https://your-mcp-server.com \
  -v $(pwd)/data:/app/data \
  whatsapp-ai-assistant
```

## MCP Integration

To integrate with whatsapp-mcp:

1. **Deploy this backend** to Railway or Fly.io to get an HTTPS URL
2. **Configure MCP webhook** to point to your deployment:
   ```
   https://your-deployment-url.com/webhook
   ```
3. **Set up MCP base URL** in environment variables so this backend can send messages back

### Webhook Payload Format

The webhook expects JSON payloads with the following structure:

```json
{
  "chat_id": "chat_identifier",
  "sender": "sender_name_or_id", 
  "text": "message content"
}
```

Alternative field names are supported:
- `chat_id` can be `from`
- `text` can be `message` or `content`
- `sender` can be `sender_id`

## Bot Commands

- `help` or `/help`: Show help message
- `summary` or `/summary`: Generate summary of recent conversation
- Messages containing "urgent", "asap", "emergency", or "help!" are flagged as urgent

## Database Schema

SQLite table structure:

```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id TEXT NOT NULL,
    sender TEXT NOT NULL,
    timestamp DATETIME NOT NULL,
    content TEXT NOT NULL,
    message_type TEXT DEFAULT 'text'
);
```

## Health Monitoring

The `/health` endpoint returns:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-01T12:00:00.000000"
}
```

## Security Considerations

- Application runs as non-root user in container
- Database is stored in a mounted volume for persistence
- HTTPS is enforced on both platforms for webhook security
- Environment variables are used for sensitive configuration

## Troubleshooting

### Common Issues

1. **OpenAI API errors**: Verify your API key is valid and has sufficient credits
2. **MCP connection issues**: Check that MCP_BASE_URL is correct and accessible
3. **Database permissions**: Ensure the data directory is writable
4. **Webhook not receiving messages**: Verify MCP is configured with the correct HTTPS URL

### Logs

Check application logs for debugging:

**Railway**: View logs in the Railway dashboard
**Fly.io**: Use `flyctl logs` command

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.