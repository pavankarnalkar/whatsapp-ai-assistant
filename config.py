"""Configuration settings for WhatsApp AI Assistant."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the WhatsApp AI Assistant."""
    
    # OpenAI API Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # WhatsApp MCP Configuration  
    MCP_BASE_URL = os.getenv('MCP_BASE_URL', 'http://localhost:8000')
    MCP_API_KEY = os.getenv('MCP_API_KEY')
    
    # Trigger Configuration
    HELP_TRIGGERS = ['help', '/help', 'commands', '/commands']
    SUMMARY_TRIGGERS = ['/summary', 'summary', '/summarize', 'summarize']
    
    # Response Configuration
    MAX_SUMMARY_MESSAGES = int(os.getenv('MAX_SUMMARY_MESSAGES', '20'))
    RESPONSE_DELAY = float(os.getenv('RESPONSE_DELAY', '1.0'))

# Create global config instance
config = Config()