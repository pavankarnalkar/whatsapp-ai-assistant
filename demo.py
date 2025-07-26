#!/usr/bin/env python3
"""Demo script showing the complete streaming functionality."""

import asyncio
import logging
from typing_simulator import TypingSimulator
from test_streaming import MockWhatsAppClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def demo_complete_flow():
    """Demo the complete flow with mock WhatsApp client."""
    print("🚀 Demo: Complete Streaming Flow")
    print("=" * 50)
    
    simulator = TypingSimulator()
    mock_client = MockWhatsAppClient()
    
    # Test scenarios
    scenarios = [
        {
            "name": "Simple Greeting",
            "chat_id": "chat_001",
            "messages": [{"role": "user", "content": "Hello!"}]
        },
        {
            "name": "Complex Query", 
            "chat_id": "chat_002",
            "messages": [{"role": "user", "content": "Explain how machine learning works and give me examples"}]
        },
        {
            "name": "Long Explanation Request",
            "chat_id": "chat_003", 
            "messages": [{"role": "user", "content": "Can you write a detailed explanation about artificial intelligence, its history, current applications, and future prospects?"}]
        }
    ]
    
    async with mock_client:
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n--- Scenario {i}: {scenario['name']} ---")
            print(f"User: {scenario['messages'][-1]['content']}")
            print()
            
            # Use streaming for longer/complex queries
            if len(scenario['messages'][-1]['content']) > 50 or 'explain' in scenario['messages'][-1]['content'].lower():
                await simulator.stream_response_with_typing(
                    scenario['chat_id'],
                    scenario['messages'],
                    mock_client
                )
            else:
                await simulator.handle_simple_response(
                    scenario['chat_id'],
                    scenario['messages'], 
                    mock_client
                )
            
            print("\n" + "="*50)
            
            # Delay between scenarios
            if i < len(scenarios):
                await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(demo_complete_flow())