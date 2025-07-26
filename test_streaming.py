#!/usr/bin/env python3
"""Test script for the streaming GPT functionality."""

import asyncio
import logging
import sys
from typing import List, Dict
from config import Config
from typing_simulator import TypingSimulator
from whatsapp_client import WhatsAppMCPClient
from gpt_client import StreamingGPTClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MockWhatsAppClient:
    """Mock WhatsApp client for testing without actual MCP server."""
    
    def __init__(self):
        self.typing_active = False
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
    
    async def send_typing_indicator(self, chat_id: str) -> bool:
        """Mock typing indicator."""
        self.typing_active = True
        print(f"🔄 [Chat {chat_id}] Typing...")
        return True
    
    async def stop_typing_indicator(self, chat_id: str) -> bool:
        """Mock stop typing."""
        self.typing_active = False
        print(f"⏸️  [Chat {chat_id}] Stopped typing")
        return True
    
    async def send_message(self, chat_id: str, message: str) -> bool:
        """Mock send message."""
        print(f"📱 [Chat {chat_id}] {message}")
        return True

async def test_message_chunking():
    """Test message chunking functionality."""
    print("\n=== Testing Message Chunking ===")
    
    simulator = TypingSimulator()
    
    # Test short message
    short_msg = "Hello, how are you today?"
    chunks = simulator.chunk_message(short_msg)
    print(f"Short message chunks: {chunks}")
    
    # Test long message
    long_msg = """This is a very long message that should be split into multiple chunks. 
    It contains multiple sentences with various punctuation marks! Some sentences are longer than others. 
    The chunking algorithm should split this at natural breakpoints like sentence endings. 
    This helps maintain readability and simulates natural typing behavior. 
    Each chunk should be sent with appropriate delays to simulate realistic typing speed."""
    
    chunks = simulator.chunk_message(long_msg)
    print(f"\nLong message split into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"  Chunk {i}: {chunk}")

async def test_typing_delays():
    """Test typing delay calculation."""
    print("\n=== Testing Typing Delays ===")
    
    simulator = TypingSimulator()
    
    test_texts = [
        "Hi!",
        "How are you doing today?",
        "This is a longer message with more words to test delay calculation.",
        "A very comprehensive and detailed explanation with many technical terms and concepts."
    ]
    
    for text in test_texts:
        delay = simulator.calculate_typing_delay(text)
        word_count = len(text.split())
        print(f"Text: '{text[:30]}...' | Words: {word_count} | Delay: {delay:.2f}s")

async def test_streaming_simulation():
    """Test the complete streaming simulation."""
    print("\n=== Testing Streaming Simulation ===")
    
    if not Config.OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY not set. Using mock responses.")
        return
    
    simulator = TypingSimulator()
    mock_client = MockWhatsAppClient()
    
    test_messages = [
        {
            "role": "user",
            "content": "Explain the concept of artificial intelligence in simple terms."
        }
    ]
    
    print("Starting streaming simulation...")
    async with mock_client:
        await simulator.stream_response_with_typing(
            "test_chat_123", 
            test_messages, 
            mock_client
        )

async def test_simple_response():
    """Test simple response handling."""
    print("\n=== Testing Simple Response ===")
    
    if not Config.OPENAI_API_KEY:
        print("⚠️  OPENAI_API_KEY not set. Using mock responses.")
        return
    
    simulator = TypingSimulator()
    mock_client = MockWhatsAppClient()
    
    test_messages = [
        {
            "role": "user", 
            "content": "Hello!"
        }
    ]
    
    print("Starting simple response...")
    async with mock_client:
        await simulator.handle_simple_response(
            "test_chat_456",
            test_messages,
            mock_client
        )

async def main():
    """Run all tests."""
    print("🚀 Starting WhatsApp AI Assistant Tests")
    
    await test_message_chunking()
    await test_typing_delays()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--with-api":
        await test_simple_response()
        await test_streaming_simulation()
    else:
        print("\n💡 Run with --with-api to test OpenAI integration")
    
    print("\n✅ Tests completed!")

if __name__ == "__main__":
    asyncio.run(main())