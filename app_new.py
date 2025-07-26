#!/usr/bin/env python3
"""
WhatsApp AI Assistant - Main Application
Uses the integrated GPT message handler for intelligent responses.
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

from message_handler import AutoReplyBot, Message

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
MCP_BASE_URL = os.getenv('MCP_BASE_URL', 'http://localhost:3000')

# Initialize the AI bot
ai_bot = AutoReplyBot()

def send_message_via_mcp(chat_id, message):
    """Send message via MCP REST API"""
    try:
        url = f"{MCP_BASE_URL}/message"
        payload = {
            'recipient': chat_id,
            'text': message
        }
        
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"Message sent to {chat_id}: {message[:50]}...")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send message via MCP: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'timestamp': datetime.now().isoformat(),
        'service': 'whatsapp-ai-assistant-gpt'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint to receive messages from MCP"""
    try:
        # Parse the incoming webhook data
        data = request.get_json()
        
        if not data:
            logger.warning("Received empty webhook payload")
            return jsonify({'error': 'Empty payload'}), 400
        
        # Extract message details (support multiple formats)
        chat_id = data.get('chat_id') or data.get('chatId') or data.get('from')
        sender = data.get('sender') or data.get('sender_id') or data.get('senderId') or 'user'
        message_content = data.get('text') or data.get('message') or data.get('content')
        timestamp = data.get('timestamp', datetime.now().timestamp())
        
        if not chat_id or not message_content:
            return jsonify({'error': 'Missing required fields: chat_id and message content'}), 400
        
        logger.info(f"Received message from {sender} in chat {chat_id}: {message_content}")
        
        # Create message data structure for the bot
        message_data = {
            'chat_id': chat_id,
            'sender_id': sender,
            'content': message_content,
            'timestamp': timestamp
        }
        
        # Process the message and get response
        response_message = ai_bot.handle_incoming_message(message_data)
        
        if response_message:
            # Send response back via MCP
            if send_message_via_mcp(chat_id, response_message):
                return jsonify({
                    'status': 'success',
                    'response': response_message,
                    'response_type': 'gpt_integrated'
                })
            else:
                return jsonify({
                    'status': 'partial_success',
                    'response': response_message,
                    'warning': 'Failed to send via MCP'
                })
        else:
            return jsonify({
                'status': 'success',
                'message': 'No response generated'
            })
            
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/send', methods=['POST'])
def send_message():
    """Manual endpoint to send messages"""
    try:
        data = request.get_json()
        chat_id = data.get('chat_id')
        message = data.get('message')
        
        if not chat_id or not message:
            return jsonify({'error': 'Missing chat_id or message'}), 400
        
        if send_message_via_mcp(chat_id, message):
            # Store the manually sent message as a bot message
            from message_handler import Message
            import time
            bot_message = Message(
                chat_id=chat_id,
                sender_id="bot",
                content=message,
                timestamp=time.time()
            )
            ai_bot.message_handler.store_message(bot_message)
            
            return jsonify({'status': 'success'})
        else:
            return jsonify({'error': 'Failed to send message'}), 500
            
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/messages/<chat_id>', methods=['GET'])
def get_messages(chat_id):
    """Get recent messages for a chat"""
    try:
        limit = request.args.get('limit', 50, type=int)
        limit = min(limit, 1000)  # Cap at 1000 messages
        
        messages = ai_bot.message_handler.chat_db.get_recent_messages(chat_id, limit)
        
        # Format messages for response
        formatted_messages = []
        for sender, timestamp, content, msg_id in messages:
            formatted_messages.append({
                'id': msg_id,
                'sender': sender,
                'content': content,
                'timestamp': timestamp
            })
        
        return jsonify({
            'messages': formatted_messages,
            'count': len(formatted_messages),
            'chat_id': chat_id
        })
        
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/stats', methods=['GET'])
def get_stats():
    """Get bot statistics"""
    try:
        # This is a simple implementation - could be expanded
        return jsonify({
            'status': 'active',
            'features': [
                'GPT-3.5 integration',
                'Chat history storage',
                'Summary generation',
                'Q&A responses',
                'Help commands'
            ],
            'endpoints': [
                '/health',
                '/webhook',
                '/send',
                '/messages/<chat_id>',
                '/stats'
            ]
        })
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    logger.info("Starting WhatsApp AI Assistant with GPT integration")
    logger.info(f"MCP Base URL: {MCP_BASE_URL}")
    logger.info(f"OpenAI API Key configured: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=debug)