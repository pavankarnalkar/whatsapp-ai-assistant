"""Configuration settings for the WhatsApp AI Assistant."""

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
    
    # WhatsApp MCP settings
    MCP_BASE_URL = os.getenv('MCP_BASE_URL', 'http://localhost:3000')
    MCP_API_KEY = os.getenv('MCP_API_KEY')
    
    # Typing simulation settings
    TYPING_DELAY_PER_WORD = float(os.getenv('TYPING_DELAY_PER_WORD', '0.1'))
    CHUNK_SIZE = int(os.getenv('CHUNK_SIZE', '100'))
    TYPING_INDICATOR_DELAY = float(os.getenv('TYPING_INDICATOR_DELAY', '2.0'))
    
    # Message chunking settings
    MAX_MESSAGE_LENGTH = int(os.getenv('MAX_MESSAGE_LENGTH', '200'))
    MIN_CHUNK_SIZE = int(os.getenv('MIN_CHUNK_SIZE', '50'))