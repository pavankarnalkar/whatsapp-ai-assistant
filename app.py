import os
import sqlite3
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
MCP_BASE_URL = os.getenv('MCP_BASE_URL', 'http://localhost:3000')
DATABASE_PATH = os.getenv('DATABASE_PATH', 'messages.db')

# Initialize OpenAI client (will be done in function calls)

def init_database():
    """Initialize SQLite database for storing messages"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id TEXT NOT NULL,
            sender TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            content TEXT NOT NULL,
            message_type TEXT DEFAULT 'text'
        )
    ''')
    
    conn.commit()
    conn.close()

def store_message(chat_id, sender, content, message_type='text'):
    """Store a message in the database"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO messages (chat_id, sender, timestamp, content, message_type)
        VALUES (?, ?, ?, ?, ?)
    ''', (chat_id, sender, datetime.now(), content, message_type))
    
    conn.commit()
    conn.close()

def get_recent_messages(chat_id, limit=50):
    """Retrieve recent messages for a chat"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT sender, content, timestamp FROM messages
        WHERE chat_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (chat_id, limit))
    
    messages = cursor.fetchall()
    conn.close()
    
    return [{'sender': msg[0], 'content': msg[1], 'timestamp': msg[2]} for msg in reversed(messages)]

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
        
        logger.info(f"Message sent to {chat_id}: {message}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send message via MCP: {e}")
        return False

def generate_ai_response(message_history, current_message):
    """Generate AI response using OpenAI"""
    if not OPENAI_API_KEY:
        return "AI service not configured. Please set OPENAI_API_KEY environment variable."
    
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        
        # Prepare conversation context
        messages = [
            {"role": "system", "content": "You are a helpful WhatsApp AI assistant. Keep responses concise and helpful."}
        ]
        
        # Add recent message history for context
        for msg in message_history[-10:]:  # Last 10 messages for context
            role = "assistant" if msg['sender'] == "bot" else "user"
            messages.append({"role": role, "content": msg['content']})
        
        # Add current message
        messages.append({"role": "user", "content": current_message})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Failed to generate AI response: {e}")
        return "Sorry, I'm having trouble processing your request right now."

def process_message(chat_id, sender, message_content):
    """Process incoming message and generate appropriate response"""
    # Store the incoming message
    store_message(chat_id, sender, message_content)
    
    message_lower = message_content.lower().strip()
    
    # Handle specific commands
    if message_lower in ['help', '/help']:
        response = "I'm your AI assistant! I can help with questions, provide summaries, and chat. Try '/summary' to get a chat summary."
        
    elif message_lower in ['summary', '/summary']:
        recent_messages = get_recent_messages(chat_id, 20)
        if recent_messages:
            # Create a summary of recent messages
            conversation = "\n".join([f"{msg['sender']}: {msg['content']}" for msg in recent_messages])
            summary_prompt = f"Summarize this conversation in 2-3 sentences:\n{conversation}"
            response = generate_ai_response([], summary_prompt)
        else:
            response = "No recent messages to summarize."
            
    elif any(urgent_word in message_lower for urgent_word in ['urgent', 'asap', 'emergency', 'help!']):
        # Handle urgent messages
        recent_messages = get_recent_messages(chat_id)
        response = generate_ai_response(recent_messages, message_content)
        response += "\n\n⚠️ This message has been flagged as urgent."
        
    else:
        # Generate AI response for general messages
        recent_messages = get_recent_messages(chat_id)
        response = generate_ai_response(recent_messages, message_content)
    
    # Store the bot response
    store_message(chat_id, "bot", response)
    
    return response

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook endpoint to receive messages from MCP"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        # Extract message details
        chat_id = data.get('chat_id') or data.get('from')
        sender = data.get('sender') or data.get('sender_id') or 'user'
        message_content = data.get('text') or data.get('message') or data.get('content')
        
        if not chat_id or not message_content:
            return jsonify({'error': 'Missing required fields: chat_id and message content'}), 400
        
        logger.info(f"Received message from {sender} in chat {chat_id}: {message_content}")
        
        # Process the message and generate response
        response_message = process_message(chat_id, sender, message_content)
        
        # Send response back via MCP
        if send_message_via_mcp(chat_id, response_message):
            return jsonify({'status': 'success', 'response': response_message})
        else:
            return jsonify({'status': 'partial_success', 'response': response_message, 'warning': 'Failed to send via MCP'})
            
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
            store_message(chat_id, "bot", message)
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
        messages = get_recent_messages(chat_id, limit)
        return jsonify({'messages': messages})
        
    except Exception as e:
        logger.error(f"Error retrieving messages: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Get port from environment variable or default to 5000
    port = int(os.getenv('PORT', 5000))
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG', 'False').lower() == 'true')