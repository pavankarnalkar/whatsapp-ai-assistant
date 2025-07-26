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