"""Core streaming response handler for simulating typing behavior."""

import asyncio
import logging
import re
from typing import List, AsyncGenerator
from config import Config
from gpt_client import StreamingGPTClient
from whatsapp_client import WhatsAppMCPClient

logger = logging.getLogger(__name__)

class TypingSimulator:
    """Handles streaming GPT responses with typing simulation."""
    
    def __init__(self):
        self.config = Config
        self.gpt_client = StreamingGPTClient() if Config.OPENAI_API_KEY else None
    
    def chunk_message(self, text: str) -> List[str]:
        """Split message into chunks at natural breakpoints."""
        if len(text) <= self.config.MAX_MESSAGE_LENGTH:
            return [text]
        
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        current_chunk = ""
        
        for sentence in sentences:
            # If adding this sentence would exceed max length, save current chunk
            if len(current_chunk) + len(sentence) > self.config.MAX_MESSAGE_LENGTH:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += " " + sentence if current_chunk else sentence
        
        # Add the last chunk if it exists
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        # Ensure no chunk is too small (merge small chunks)
        merged_chunks = []
        for chunk in chunks:
            if (merged_chunks and 
                len(chunk) < self.config.MIN_CHUNK_SIZE and 
                len(merged_chunks[-1]) + len(chunk) <= self.config.MAX_MESSAGE_LENGTH):
                merged_chunks[-1] += " " + chunk
            else:
                merged_chunks.append(chunk)
        
        return merged_chunks
    
    def calculate_typing_delay(self, text: str) -> float:
        """Calculate realistic typing delay based on text length."""
        word_count = len(text.split())
        base_delay = word_count * self.config.TYPING_DELAY_PER_WORD
        # Add some randomness for more natural feel (±20%)
        import random
        variation = base_delay * 0.2
        return base_delay + random.uniform(-variation, variation)
    
    async def stream_response_with_typing(
        self, 
        chat_id: str, 
        messages: List[dict],
        whatsapp_client: WhatsAppMCPClient
    ) -> None:
        """Stream GPT response with typing simulation."""
        logger.info(f"Starting streaming response for chat {chat_id}")
        
        try:
            # Show typing indicator
            await whatsapp_client.send_typing_indicator(chat_id)
            await asyncio.sleep(self.config.TYPING_INDICATOR_DELAY)
            
            # Collect the full response first
            if self.gpt_client:
                full_response = ""
                async for chunk in self.gpt_client.stream_completion(messages):
                    full_response += chunk
            else:
                full_response = "Mock response: This is a test response for demonstration purposes."
            
            # Stop typing indicator before sending messages
            await whatsapp_client.stop_typing_indicator(chat_id)
            
            # Split response into chunks
            message_chunks = self.chunk_message(full_response)
            
            logger.info(f"Sending response in {len(message_chunks)} chunks")
            
            # Send each chunk with appropriate delays
            for i, chunk in enumerate(message_chunks):
                if i > 0:  # Add typing delay between chunks
                    # Show typing indicator for subsequent chunks
                    await whatsapp_client.send_typing_indicator(chat_id)
                    typing_delay = self.calculate_typing_delay(chunk)
                    await asyncio.sleep(typing_delay)
                    await whatsapp_client.stop_typing_indicator(chat_id)
                
                # Send the message chunk
                success = await whatsapp_client.send_message(chat_id, chunk)
                if not success:
                    logger.error(f"Failed to send chunk {i+1} to chat {chat_id}")
                    break
                
                # Small delay between messages for natural feel
                if i < len(message_chunks) - 1:
                    await asyncio.sleep(0.5)
            
            logger.info(f"Completed streaming response for chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error in stream_response_with_typing: {e}")
            # Ensure typing indicator is stopped on error
            await whatsapp_client.stop_typing_indicator(chat_id)
            # Send error message
            await whatsapp_client.send_message(
                chat_id, 
                "Sorry, I encountered an error while processing your request."
            )
    
    async def handle_simple_response(
        self,
        chat_id: str,
        messages: List[dict],
        whatsapp_client: WhatsAppMCPClient
    ) -> None:
        """Handle simple response without streaming for short messages."""
        try:
            # Show typing indicator
            await whatsapp_client.send_typing_indicator(chat_id)
            
            # Get complete response
            if self.gpt_client:
                response = await self.gpt_client.get_completion(messages)
            else:
                response = "Mock response: Hello! This is a test response."
            
            # Calculate appropriate delay
            typing_delay = self.calculate_typing_delay(response)
            await asyncio.sleep(min(typing_delay, 3.0))  # Cap at 3 seconds
            
            # Stop typing and send message
            await whatsapp_client.stop_typing_indicator(chat_id)
            await whatsapp_client.send_message(chat_id, response)
            
        except Exception as e:
            logger.error(f"Error in handle_simple_response: {e}")
            await whatsapp_client.stop_typing_indicator(chat_id)
            await whatsapp_client.send_message(
                chat_id,
                "Sorry, I encountered an error while processing your request."
            )