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