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

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the WhatsApp AI Assistant implementation for issue #16.