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