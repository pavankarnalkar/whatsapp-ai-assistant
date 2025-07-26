#!/usr/bin/env python3
"""
WhatsApp AI Assistant Webhook Server
Receives webhook notifications from whatsapp-mcp and processes messages.
"""

import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'service': 'whatsapp-ai-assistant'
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive messages from whatsapp-mcp
    Expected payload format:
    {
        "chatId": "string",
        "senderId": "string", 
        "message": "string",
        "timestamp": "ISO8601"
    }
    """
    try:
        # Parse the incoming webhook data
        data = request.get_json()
        
        if not data:
            logger.warning("Received empty webhook payload")
            return jsonify({'error': 'Empty payload'}), 400
        
        # Extract message details
        chat_id = data.get('chatId')
        sender_id = data.get('senderId')
        message = data.get('message')
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())
        
        # Log the received message
        logger.info(f"Received message from {sender_id} in chat {chat_id}: {message}")
        
        # TODO: Process the message (store to database, generate AI response, etc.)
        # For now, just acknowledge receipt
        
        response = {
            'status': 'received',
            'chatId': chat_id,
            'senderId': sender_id,
            'processedAt': datetime.utcnow().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """
    Webhook verification endpoint for MCP setup
    Some webhook systems require GET verification
    """
    verify_token = request.args.get('verify_token')
    challenge = request.args.get('challenge')
    
    # For basic verification, return the challenge
    if challenge:
        logger.info(f"Webhook verification requested with challenge: {challenge}")
        return challenge
    
    return jsonify({'status': 'webhook_endpoint_active'}), 200

if __name__ == '__main__':
    port = int(os.getenv('WEBHOOK_PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting webhook server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)