"""Configuration management for the WhatsApp AI Assistant."""

import os
from typing import List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the WhatsApp AI Assistant."""
    
    # SMTP Configuration
    SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SMTP_FROM_EMAIL = os.getenv('SMTP_FROM_EMAIL', '')
    SMTP_TO_EMAIL = os.getenv('SMTP_TO_EMAIL', '')
    
    # Urgency Detection Settings
    URGENCY_KEYWORDS = os.getenv('URGENCY_KEYWORDS', 'urgent,asap,emergency,critical,immediate,help').split(',')
    
    @classmethod
    def get_urgency_keywords(cls) -> List[str]:
        """Get the list of urgency keywords."""
        return [keyword.strip().lower() for keyword in cls.URGENCY_KEYWORDS]
    
    @classmethod
    def is_smtp_configured(cls) -> bool:
        """Check if SMTP configuration is complete."""
        return all([
            cls.SMTP_USERNAME,
            cls.SMTP_PASSWORD,
            cls.SMTP_FROM_EMAIL,
            cls.SMTP_TO_EMAIL
        ])