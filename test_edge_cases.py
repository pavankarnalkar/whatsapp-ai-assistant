#!/usr/bin/env python3
"""Edge case tests for the streaming functionality."""

import asyncio
from typing_simulator import TypingSimulator
from test_streaming import MockWhatsAppClient

async def test_edge_cases():
    """Test edge cases and error scenarios."""
    print("🧪 Testing Edge Cases")
    print("=" * 40)
    
    simulator = TypingSimulator()
    mock_client = MockWhatsAppClient()
    
    # Test cases
    test_cases = [
        {
            "name": "Empty message",
            "text": ""
        },
        {
            "name": "Very short message", 
            "text": "Hi"
        },
        {
            "name": "Single sentence without punctuation",
            "text": "This is a sentence without any punctuation marks at the end"
        },
        {
            "name": "Multiple punctuation",
            "text": "Really?! Are you sure??? Yes!!!"
        },
        {
            "name": "Long single sentence",
            "text": "This is an extremely long sentence that goes on and on without any punctuation marks to break it up into natural chunks so the chunking algorithm will need to handle it gracefully by splitting at word boundaries when it exceeds the maximum length limit"
        },
        {
            "name": "Mixed content with newlines",
            "text": "First paragraph.\n\nSecond paragraph! Third sentence? Final sentence."
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i}: {test_case['name']} ---")
        print(f"Input: '{test_case['text']}'")
        
        # Test chunking
        chunks = simulator.chunk_message(test_case['text'])
        print(f"Chunks ({len(chunks)}):")
        for j, chunk in enumerate(chunks, 1):
            print(f"  {j}. '{chunk}'")
        
        # Test delay calculation
        if test_case['text']:
            delay = simulator.calculate_typing_delay(test_case['text'])
            word_count = len(test_case['text'].split())
            print(f"Typing delay: {delay:.2f}s ({word_count} words)")
        
        print("-" * 40)

async def test_streaming_with_errors():
    """Test streaming behavior with simulated errors."""
    print("\n🔥 Testing Error Scenarios")
    print("=" * 40)
    
    simulator = TypingSimulator()
    
    # Mock client that fails operations
    class FailingMockClient:
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        
        async def send_typing_indicator(self, chat_id: str) -> bool:
            print(f"❌ Failed to send typing indicator to {chat_id}")
            return False
        
        async def stop_typing_indicator(self, chat_id: str) -> bool:
            print(f"❌ Failed to stop typing indicator for {chat_id}")
            return False
        
        async def send_message(self, chat_id: str, message: str) -> bool:
            print(f"❌ Failed to send message to {chat_id}: {message[:30]}...")
            return False
    
    failing_client = FailingMockClient()
    test_messages = [{"role": "user", "content": "Test message"}]
    
    print("Testing with failing WhatsApp client:")
    async with failing_client:
        await simulator.handle_simple_response(
            "test_chat_error",
            test_messages,
            failing_client
        )

if __name__ == "__main__":
    async def main():
        await test_edge_cases()
        await test_streaming_with_errors()
        print("\n✅ Edge case tests completed!")
    
    asyncio.run(main())