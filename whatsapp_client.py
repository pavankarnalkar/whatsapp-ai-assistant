"""WhatsApp MCP client for sending messages and typing indicators."""

import asyncio
import aiohttp
import logging
from typing import Optional
from config import Config

logger = logging.getLogger(__name__)

class WhatsAppMCPClient:
    """Client for interacting with WhatsApp MCP server."""
    
    def __init__(self):
        self.base_url = Config.MCP_BASE_URL
        self.api_key = Config.MCP_API_KEY
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def send_typing_indicator(self, chat_id: str) -> bool:
        """Send typing indicator to chat."""
        try:
            url = f"{self.base_url}/typing"
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            data = {"chat_id": chat_id, "typing": True}
            
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    logger.info(f"Typing indicator sent to chat {chat_id}")
                    return True
                else:
                    logger.error(f"Failed to send typing indicator: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error sending typing indicator: {e}")
            return False
    
    async def stop_typing_indicator(self, chat_id: str) -> bool:
        """Stop typing indicator in chat."""
        try:
            url = f"{self.base_url}/typing"
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            data = {"chat_id": chat_id, "typing": False}
            
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    logger.info(f"Typing indicator stopped for chat {chat_id}")
                    return True
                else:
                    logger.error(f"Failed to stop typing indicator: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error stopping typing indicator: {e}")
            return False
    
    async def send_message(self, chat_id: str, message: str) -> bool:
        """Send a message to a chat."""
        try:
            url = f"{self.base_url}/message"
            headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
            data = {
                "chat_id": chat_id,
                "message": message
            }
            
            async with self.session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    logger.info(f"Message sent to chat {chat_id}: {message[:50]}...")
                    return True
                else:
                    logger.error(f"Failed to send message: {response.status}")
                    return False
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            return False