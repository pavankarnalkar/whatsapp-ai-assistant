"""Predefined responses for WhatsApp AI Assistant triggers."""

from typing import Dict, List

class PredefinedResponses:
    """Container for predefined responses to various triggers."""
    
    HELP_RESPONSE = """🤖 **WhatsApp AI Assistant - Commands**

Available commands:
• `help` or `/help` - Show this help message
• `/summary` - Get a summary of recent chat messages
• `commands` - List all available commands

I can also:
✅ Answer questions about our chat history
✅ Provide intelligent responses using AI
✅ Detect urgent messages and send notifications

Just send me a message and I'll do my best to help! 😊"""

    WELCOME_RESPONSE = """👋 Welcome! I'm your WhatsApp AI Assistant.

Type `help` to see what I can do for you."""

    ERROR_RESPONSE = """❌ Sorry, I encountered an error processing your request. Please try again later."""

    NO_HISTORY_RESPONSE = """📝 No recent messages found to summarize."""

    SUMMARY_PROCESSING_RESPONSE = """🔄 Generating summary of recent messages... Please wait a moment."""

    @classmethod
    def get_help_response(cls) -> str:
        """Get the help response message."""
        return cls.HELP_RESPONSE
    
    @classmethod
    def get_welcome_response(cls) -> str:
        """Get the welcome response message."""
        return cls.WELCOME_RESPONSE
    
    @classmethod
    def get_error_response(cls) -> str:
        """Get the error response message."""
        return cls.ERROR_RESPONSE
    
    @classmethod
    def get_no_history_response(cls) -> str:
        """Get the no history response message."""
        return cls.NO_HISTORY_RESPONSE
    
    @classmethod
    def get_summary_processing_response(cls) -> str:
        """Get the summary processing response message."""
        return cls.SUMMARY_PROCESSING_RESPONSE