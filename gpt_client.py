"""OpenAI GPT client with streaming capabilities."""

import asyncio
import openai
import logging
from typing import AsyncGenerator, List, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class StreamingGPTClient:
    """Client for streaming GPT responses."""
    
    def __init__(self):
        if not Config.OPENAI_API_KEY:
            logger.warning("OPENAI_API_KEY not set. GPT client will not be initialized.")
            self.client = None
            self.model = Config.OPENAI_MODEL
            return
        self.client = openai.AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = Config.OPENAI_MODEL
    
    async def stream_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> AsyncGenerator[str, None]:
        """Stream completion from GPT model."""
        if not self.client:
            yield "Error: OpenAI client not initialized. Please set OPENAI_API_KEY."
            return
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                **kwargs
            )
            
            async for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Error streaming GPT completion: {e}")
            yield f"Error: Unable to generate response"
    
    async def get_completion(
        self, 
        messages: List[Dict[str, str]], 
        **kwargs
    ) -> str:
        """Get complete response from GPT model."""
        if not self.client:
            return "Error: OpenAI client not initialized. Please set OPENAI_API_KEY."
            
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error getting GPT completion: {e}")
            return "Error: Unable to generate response"