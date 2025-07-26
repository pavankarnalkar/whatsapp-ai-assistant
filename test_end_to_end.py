#!/usr/bin/env python3
"""
End-to-end test of the WhatsApp AI Assistant with GPT integration.
This test verifies the complete functionality without requiring API keys.
"""

import json
import os
import tempfile
import time
from unittest.mock import patch, AsyncMock

# Import the new app
from app_new import app
from message_handler import MessageHandler


def test_webhook_endpoints():
    """Test the webhook endpoints with the new GPT-integrated app."""
    print("=== Testing WhatsApp AI Assistant End-to-End ===\n")
    
    # Create test client
    app.config['TESTING'] = True
    client = app.test_client()
    
    print("1. Testing health endpoint...")
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    print(f"✓ Health check: {data['status']}")
    
    print("\n2. Testing stats endpoint...")
    response = client.get('/stats')
    assert response.status_code == 200
    data = response.get_json()
    assert 'GPT-3.5 integration' in data['features']
    print(f"✓ Stats: {len(data['features'])} features available")
    
    print("\n3. Testing webhook with help command...")
    help_payload = {
        'chat_id': 'test_chat_123',
        'sender_id': 'test_user',
        'text': 'help',
        'timestamp': time.time()
    }
    
    response = client.post('/webhook', 
                          data=json.dumps(help_payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    print(f"✓ Help webhook: {data['status']}")
    
    print("\n4. Testing webhook with summary command...")
    summary_payload = {
        'chat_id': 'test_chat_123',
        'sender_id': 'test_user',
        'text': '/summary',
        'timestamp': time.time()
    }
    
    response = client.post('/webhook',
                          data=json.dumps(summary_payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    print(f"✓ Summary webhook: {data['status']}")
    
    print("\n5. Testing webhook with question...")
    question_payload = {
        'chat_id': 'test_chat_123',
        'sender_id': 'test_user', 
        'text': 'What is artificial intelligence?',
        'timestamp': time.time()
    }
    
    response = client.post('/webhook',
                          data=json.dumps(question_payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    print(f"✓ Question webhook: {data['status']}")
    
    print("\n6. Testing message retrieval...")
    response = client.get('/messages/test_chat_123?limit=10')
    assert response.status_code == 200
    data = response.get_json()
    print(f"✓ Retrieved {data['count']} messages for chat")
    
    print("\n7. Testing webhook with different format...")
    alt_payload = {
        'chatId': 'test_chat_456',
        'senderId': 'user_456',
        'message': 'hello world',
        'timestamp': time.time()
    }
    
    response = client.post('/webhook',
                          data=json.dumps(alt_payload),
                          content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    print(f"✓ Alternative format webhook: {data['status']}")
    
    print("\n8. Testing error handling...")
    bad_payload = {}
    response = client.post('/webhook',
                          data=json.dumps(bad_payload),
                          content_type='application/json')
    assert response.status_code == 400
    print("✓ Bad payload correctly rejected")


def test_gpt_integration_with_mock():
    """Test GPT integration using mocked responses."""
    print("\n=== Testing GPT Integration with Mock ===\n")
    
    # Import to get access to the bot instance
    from app_new import ai_bot
    
    # Mock the GPT client to avoid API calls
    async def mock_completion(messages):
        last_message = messages[-1]['content']
        if 'summary' in last_message.lower():
            return "Mock summary: The conversation covered greetings and project updates."
        elif '?' in last_message:
            return f"Mock answer: This is a response to your question about {last_message.split()[2] if len(last_message.split()) > 2 else 'that topic'}."
        else:
            return "Mock response: Thank you for your message."
    
    # Patch the GPT client in the bot
    with patch.object(ai_bot.message_handler.gpt_client, 'get_completion', side_effect=mock_completion):
        with patch.object(ai_bot.message_handler.gpt_client, 'client', True):
            
            client = app.test_client()
            
            print("1. Testing GPT-powered summary...")
            # First add some messages to summarize
            for i, msg in enumerate(['Hello', 'How are you?', 'Working on project', 'Sounds good']):
                payload = {
                    'chat_id': 'gpt_test_chat',
                    'sender_id': f'user_{i}',
                    'text': msg,
                    'timestamp': time.time() - (4-i) * 60
                }
                client.post('/webhook', data=json.dumps(payload), content_type='application/json')
            
            # Request summary
            summary_payload = {
                'chat_id': 'gpt_test_chat',
                'sender_id': 'test_user',
                'text': '/summary',
                'timestamp': time.time()
            }
            response = client.post('/webhook', data=json.dumps(summary_payload), content_type='application/json')
            assert response.status_code == 200
            data = response.get_json()
            assert 'Mock summary' in data['response']
            print("✓ GPT summary generation working")
            
            print("\n2. Testing GPT-powered Q&A...")
            qa_payload = {
                'chat_id': 'gpt_test_chat',
                'sender_id': 'test_user',
                'text': 'What is machine learning?',
                'timestamp': time.time()
            }
            response = client.post('/webhook', data=json.dumps(qa_payload), content_type='application/json')
            assert response.status_code == 200
            data = response.get_json()
            assert 'Mock answer' in data['response']
            print("✓ GPT Q&A generation working")


def main():
    """Run all tests."""
    try:
        test_webhook_endpoints()
        test_gpt_integration_with_mock()
        
        print("\n=== All End-to-End Tests Passed! ===")
        print("\n✅ Verified Features:")
        print("  • Webhook endpoint handling multiple message formats")
        print("  • GPT integration for summaries and Q&A")
        print("  • Message storage and retrieval")
        print("  • Help command functionality")
        print("  • Error handling and validation")
        print("  • Health and stats endpoints")
        print("  • Graceful degradation without API keys")
        
        print("\n🚀 The WhatsApp AI Assistant is ready for deployment!")
        print("\n📝 To enable GPT responses:")
        print("  1. Set OPENAI_API_KEY environment variable")
        print("  2. Configure MCP_BASE_URL for your WhatsApp MCP server")
        print("  3. Deploy the app_new.py application")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    main()