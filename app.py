"""
WhatsApp AI Assistant - Main application with webhook listener and auto-reply.
"""
import os
from flask import Flask, request, jsonify
from mcp_client import MCPClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
mcp_client = MCPClient()

# Static replies for testing
STATIC_REPLIES = {
    'help': 'Hello! I am your WhatsApp AI Assistant. You can ask me anything!',
    'hello': 'Hi there! How can I help you today?',
    'hi': 'Hello! Nice to meet you!',
    'default': 'Thanks for your message! This is an automated reply from your AI Assistant.'
}


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook endpoint to receive incoming WhatsApp messages from MCP.
    Processes the message and sends an automatic reply.
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        # Extract message details
        sender_id = data.get('sender')
        chat_id = data.get('chat_id', sender_id)  # Use sender as fallback
        message_text = data.get('text', '').lower().strip()
        timestamp = data.get('timestamp')
        
        if not sender_id or not message_text:
            return jsonify({'error': 'Missing required fields: sender or text'}), 400
        
        print(f"Received message from {sender_id}: {message_text}")
        
        # Generate reply based on message content
        reply_text = generate_reply(message_text)
        
        # Send reply using MCP client
        success = mcp_client.send_reply(chat_id, reply_text)
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Reply sent successfully',
                'reply': reply_text
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to send reply'
            }), 500
            
    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({'error': str(e)}), 500


def generate_reply(message_text: str) -> str:
    """
    Generate a static reply based on the incoming message.
    
    Args:
        message_text: The incoming message text (lowercase)
        
    Returns:
        str: The reply text to send
    """
    # Check for specific keywords
    for keyword, reply in STATIC_REPLIES.items():
        if keyword != 'default' and keyword in message_text:
            return reply
    
    # Default reply
    return STATIC_REPLIES['default']


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'healthy', 'service': 'whatsapp-ai-assistant'})


@app.route('/send-message', methods=['POST'])
def send_message_endpoint():
    """
    Endpoint to manually send messages via MCP API.
    
    Expected JSON payload:
    {
        "recipient": "recipient_id",
        "text": "message text"
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        recipient = data.get('recipient')
        text = data.get('text')
        
        if not recipient or not text:
            return jsonify({'error': 'Missing required fields: recipient or text'}), 400
        
        # Send message using MCP client
        result = mcp_client.send_message(recipient, text)
        
        return jsonify({
            'status': 'success',
            'message': 'Message sent successfully',
            'result': result
        })
        
    except Exception as e:
        print(f"Error sending message: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    print(f"Starting WhatsApp AI Assistant on port {port}")
    print(f"MCP Base URL: {mcp_client.base_url}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)