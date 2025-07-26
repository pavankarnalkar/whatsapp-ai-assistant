#!/usr/bin/env python3
"""Example usage of the WhatsApp AI Assistant streaming functionality."""

import asyncio
import os
from main import WhatsAppAIAssistant

async def example_usage():
    """Example of how to use the streaming assistant."""
    
    # Create assistant instance
    assistant = WhatsAppAIAssistant()
    
    # Example 1: Simple greeting (will use simple response)
    print("Example 1: Simple greeting")
    await assistant.handle_message(
        chat_id="example_chat_123",
        user_message="Hello!"
    )
    
    print("\n" + "="*50 + "\n")
    
    # Example 2: Complex query (will use streaming response)
    print("Example 2: Complex query")  
    await assistant.handle_message(
        chat_id="example_chat_456",
        user_message="Can you explain how artificial intelligence works?"
    )
    
    print("\n" + "="*50 + "\n")
    
    # Example 3: With chat history
    print("Example 3: With chat history")
    chat_history = [
        "Hi there!",
        "Hello! How can I help you today?",
        "I'm interested in learning about programming"
    ]
    
    await assistant.handle_message(
        chat_id="example_chat_789",
        user_message="What programming language should I start with?",
        chat_history=chat_history
    )

if __name__ == "__main__":
    print("🤖 WhatsApp AI Assistant - Streaming Examples")
    print("=" * 60)
    print()
    
    if not os.getenv('OPENAI_API_KEY'):
        print("ℹ️  Note: OPENAI_API_KEY not set - using mock responses")
        print("   Set OPENAI_API_KEY environment variable for real GPT responses")
        print()
    
    asyncio.run(example_usage())
    
    print("\n✅ Examples completed!")
    print("\nKey features demonstrated:")
    print("- ✅ Automatic response strategy selection")
    print("- ✅ Typing indicators and delays")
    print("- ✅ Message chunking for long responses")
    print("- ✅ Chat history integration")
    print("- ✅ Graceful handling of missing API keys")