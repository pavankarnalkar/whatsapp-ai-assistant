"""Main WhatsApp AI Assistant with streaming GPT responses."""

import asyncio
import logging
from typing import List, Dict
from config import Config
from typing_simulator import TypingSimulator
from whatsapp_client import WhatsAppMCPClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WhatsAppAIAssistant:
    """Main assistant class that handles incoming messages and generates responses."""
    
    def __init__(self):
        self.typing_simulator = TypingSimulator()
    
    def create_message_context(self, user_message: str, chat_history: List[str] = None) -> List[Dict[str, str]]:
        """Create conversation context for GPT."""
        messages = [
            {
                "role": "system",
                "content": "You are a helpful AI assistant for WhatsApp. Provide clear, concise, and friendly responses. Keep your responses conversational and appropriate for messaging."
            }
        ]
        
        # Add chat history if available
        if chat_history:
            for i, msg in enumerate(chat_history[-10:]):  # Last 10 messages for context
                role = "assistant" if i % 2 == 0 else "user"
                messages.append({"role": role, "content": msg})
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        return messages
    
    async def handle_message(
        self, 
        chat_id: str, 
        user_message: str, 
        chat_history: List[str] = None
    ) -> None:
        """Handle incoming message and generate streaming response."""
        logger.info(f"Handling message from chat {chat_id}: {user_message[:50]}...")
        
        try:
            # Create message context
            messages = self.create_message_context(user_message, chat_history)
            
            # Use WhatsApp client within async context
            async with WhatsAppMCPClient() as whatsapp_client:
                # Determine response strategy based on expected response length
                if self._should_use_streaming(user_message):
                    await self.typing_simulator.stream_response_with_typing(
                        chat_id, messages, whatsapp_client
                    )
                else:
                    await self.typing_simulator.handle_simple_response(
                        chat_id, messages, whatsapp_client
                    )
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
    
    def _should_use_streaming(self, user_message: str) -> bool:
        """Determine if streaming should be used based on message content."""
        # Use streaming for complex queries that likely need longer responses
        streaming_keywords = [
            "explain", "describe", "tell me about", "how to", "what is",
            "summary", "summarize", "analyze", "compare", "list",
            "write", "create", "generate", "help me with"
        ]
        
        message_lower = user_message.lower()
        return any(keyword in message_lower for keyword in streaming_keywords) or len(user_message) > 50

# Example usage functions
async def demo_streaming_response():
    """Demo function to show streaming response functionality."""
    assistant = WhatsAppAIAssistant()
    
    # Simulate receiving a complex query
    demo_chat_id = "demo_chat_123"
    demo_message = "Can you explain how machine learning works and give me some examples of its applications?"
    
    logger.info("=== Demo: Streaming Response ===")
    await assistant.handle_message(demo_chat_id, demo_message)

async def demo_simple_response():
    """Demo function to show simple response functionality."""
    assistant = WhatsAppAIAssistant()
    
    # Simulate receiving a simple query
    demo_chat_id = "demo_chat_456"
    demo_message = "Hello!"
    
    logger.info("=== Demo: Simple Response ===")
    await assistant.handle_message(demo_chat_id, demo_message)

if __name__ == "__main__":
    async def main():
        """Run demo scenarios."""
        if not Config.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not found. Please set it in .env file")
            return
        
        logger.info("Starting WhatsApp AI Assistant Demo")
        
        # Run demo scenarios
        await demo_simple_response()
        await asyncio.sleep(2)
        await demo_streaming_response()
        
        logger.info("Demo completed")
    
    asyncio.run(main())
"""Main entry point for WhatsApp AI Assistant."""

import logging
import time
from typing import Dict, Any

from message_handler import AutoReplyBot
from config import config

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    """Main function to demonstrate the auto-reply functionality."""
    logger.info("Starting WhatsApp AI Assistant")
    
    # Initialize the bot
    bot = AutoReplyBot()
    
    # Example usage - simulate incoming messages
    example_messages = [
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': 'help',
            'timestamp': time.time(),
            'message_id': 'msg_1'
        },
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': '/summary',
            'timestamp': time.time(),
            'message_id': 'msg_2'
        },
        {
            'chat_id': 'chat_123',
            'sender_id': 'user_456',
            'content': 'Hello there!',
            'timestamp': time.time(),
            'message_id': 'msg_3'
        }
    ]
    
    print("=" * 60)
    print("WhatsApp AI Assistant - Auto-Reply Demo")
    print("=" * 60)
    
    for i, message_data in enumerate(example_messages, 1):
        print(f"\n--- Test Message {i} ---")
        print(f"Input: {message_data['content']}")
        
        response = bot.handle_incoming_message(message_data)
        
        if response:
            print(f"✅ Auto-reply triggered:")
            print(response)
        else:
            print("❌ No auto-reply triggered")
        
        print("-" * 40)
    
    print("\n🎉 Demo completed successfully!")
    print("\nTo integrate with WhatsApp MCP:")
    print("1. Set up webhook endpoint to receive messages")
    print("2. Configure MCP_BASE_URL and MCP_API_KEY")
    print("3. Add OpenAI API key for summary functionality")

if __name__ == "__main__":
    main()
from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from models import MessagePayload, StoredMessage
from database import init_database, store_message, get_messages_by_chat, get_message_count

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    logger.info("Starting WhatsApp AI Assistant webhook listener...")
    init_database()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="WhatsApp AI Assistant Webhook",
    description="Webhook listener for MCP messages from WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WhatsApp AI Assistant Webhook",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/stats")
async def get_stats():
    """Get basic statistics about stored messages"""
    try:
        total_messages = get_message_count()
        return {
            "total_messages": total_messages,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/webhook/message")
async def receive_message(request: Request):
    """
    Webhook endpoint to receive new message payloads from whatsapp-mcp
    Parses sender ID, chat ID, timestamp, and message text
    Stores each message to SQLite
    """
    try:
        # Get raw payload
        payload = await request.json()
        logger.info(f"Received webhook payload: {payload}")
        
        # Parse the payload into our MessagePayload model
        # Note: The exact structure depends on whatsapp-mcp format
        # This is a reasonable assumption based on common webhook patterns
        message_data = {
            "sender_id": payload.get("sender_id") or payload.get("from") or payload.get("senderId"),
            "chat_id": payload.get("chat_id") or payload.get("chatId") or payload.get("chat"),
            "timestamp": payload.get("timestamp") or payload.get("time") or datetime.now(),
            "message_text": payload.get("message_text") or payload.get("text") or payload.get("body") or payload.get("message"),
            "message_id": payload.get("message_id") or payload.get("messageId") or payload.get("id")
        }
        
        # Validate required fields
        if not message_data["sender_id"]:
            raise HTTPException(status_code=400, detail="Missing sender_id in payload")
        if not message_data["chat_id"]:
            raise HTTPException(status_code=400, detail="Missing chat_id in payload")
        if not message_data["message_text"]:
            raise HTTPException(status_code=400, detail="Missing message_text in payload")
        
        # Handle timestamp conversion if it's a string
        if isinstance(message_data["timestamp"], str):
            try:
                message_data["timestamp"] = datetime.fromisoformat(message_data["timestamp"].replace('Z', '+00:00'))
            except ValueError:
                # If timestamp parsing fails, use current time
                message_data["timestamp"] = datetime.now()
        elif isinstance(message_data["timestamp"], (int, float)):
            # Handle Unix timestamp
            message_data["timestamp"] = datetime.fromtimestamp(message_data["timestamp"])
        elif not isinstance(message_data["timestamp"], datetime):
            message_data["timestamp"] = datetime.now()
        
        # Create and validate message payload
        message = MessagePayload(**message_data)
        
        # Store message to database
        message_id = store_message(message)
        
        logger.info(f"Successfully processed message from {message.sender_id} in chat {message.chat_id}")
        
        return {
            "status": "success",
            "message": "Message received and stored",
            "message_id": message_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/messages/{chat_id}")
async def get_chat_messages(chat_id: str, limit: int = 50):
    """Get messages for a specific chat ID"""
    try:
        if limit < 1 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        messages = get_messages_by_chat(chat_id, limit)
        return {
            "chat_id": chat_id,
            "messages": messages,
            "count": len(messages),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages for chat {chat_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
