# Quick Deployment Guide

## Overview
This WhatsApp AI Assistant is ready for deployment on Railway or Fly.io with HTTPS webhook support for MCP integration.

## Railway Deployment (Recommended)

1. **Fork/Clone** this repository to your GitHub account

2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub account
   - Create new project from your fork

3. **Set Environment Variables** in Railway dashboard:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MCP_BASE_URL=https://your-mcp-server.com (optional)
   ```

4. **Deploy**: Railway will automatically build using the Dockerfile

5. **Get Your Webhook URL**: 
   ```
   https://your-app-name.railway.app/webhook
   ```

## Fly.io Deployment

1. **Install Fly CLI**:
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Run Deployment Script**:
   ```bash
   ./deploy-fly.sh
   ```
   OR manually:
   ```bash
   flyctl launch
   flyctl secrets set OPENAI_API_KEY=your_key_here
   flyctl deploy
   ```

3. **Get Your Webhook URL**:
   ```
   https://your-app-name.fly.dev/webhook
   ```

## MCP Integration

Once deployed, configure your whatsapp-mcp server to send webhooks to your HTTPS URL:

### Expected Webhook Format
```json
{
  "chat_id": "chat_identifier",
  "sender": "sender_name", 
  "text": "message content"
}
```

### MCP Configuration
Update your MCP configuration to point to your deployed webhook:
```
webhook_url: https://your-deployment-url.com/webhook
```

## Testing Your Deployment

Use the included test script:
```bash
python test_webhook.py https://your-deployment-url.com
```

## API Endpoints

- `GET /health` - Health check
- `POST /webhook` - Receive messages from MCP  
- `POST /send` - Send messages manually
- `GET /messages/<chat_id>` - Get chat history

## Bot Commands

Users can send these commands via WhatsApp:
- `help` or `/help` - Show help
- `summary` or `/summary` - Get conversation summary
- Messages with "urgent", "asap", "emergency" are flagged

## Environment Variables

Required:
- `OPENAI_API_KEY` - Your OpenAI API key

Optional:
- `MCP_BASE_URL` - Your MCP server URL (default: http://localhost:3000)
- `PORT` - Server port (auto-set by platforms)
- `DATABASE_PATH` - SQLite file path (default: ./messages.db)

## Security Features

- ✅ HTTPS enforced on both platforms
- ✅ Non-root user in Docker container
- ✅ Health checks for monitoring
- ✅ Environment variable protection
- ✅ SQLite database persistence

## Troubleshooting

1. **Webhook not working**: Check MCP configuration points to correct HTTPS URL
2. **AI not responding**: Verify OPENAI_API_KEY is set correctly
3. **Database issues**: Check logs for SQLite permissions
4. **Connection errors**: Verify MCP_BASE_URL is accessible

Your WhatsApp AI Assistant is now ready for production use! 🚀