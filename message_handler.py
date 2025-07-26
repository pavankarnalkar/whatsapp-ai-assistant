"""Message handler for WhatsApp AI Assistant auto-reply functionality."""

import re
import time
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from config import config
from responses import PredefinedResponses

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Message:
    """Represents a WhatsApp message."""
    chat_id: str
    sender_id: str
    content: str
    timestamp: float
    message_id: Optional[str] = None

@dataclass
class TriggerResponse:
    """Represents a response to a trigger."""
    response_text: str
    requires_gpt: bool = False
    response_type: str = "text"

class MessageHandler:
    """Handles incoming messages and generates appropriate responses."""
    
    def __init__(self):
        """Initialize the message handler."""
        self.predefined_responses = PredefinedResponses()
        
    def detect_trigger(self, message_content: str) -> Optional[str]:
        """
        Detect if a message contains any trigger keywords.
        
        Args:
            message_content: The content of the message to check
            
        Returns:
            The trigger type if found, None otherwise
        """
        # Normalize message content (lowercase, strip whitespace)
        content = message_content.strip().lower()
        
        # Split content into words for exact word matching
        words = re.split(r'\W+', content)
        
        # Check for help triggers
        for trigger in config.HELP_TRIGGERS:
            trigger_lower = trigger.lower()
            # Check for exact word match or command match
            if trigger_lower.startswith('/'):
                # For commands like /help, check exact substring match
                if trigger_lower in content:
                    return "help"
            else:
                # For regular words like "help", check word boundaries
                if trigger_lower in words:
                    return "help"
                
        # Check for summary triggers  
        for trigger in config.SUMMARY_TRIGGERS:
            trigger_lower = trigger.lower()
            # Check for exact word match or command match
            if trigger_lower.startswith('/'):
                # For commands like /summary, check exact substring match
                if trigger_lower in content:
                    return "summary"
            else:
                # For regular words like "summary", check word boundaries
                if trigger_lower in words or re.search(r'\b' + re.escape(trigger_lower) + r'\b', content):
                    return "summary"
                
        return None
    
    def generate_help_response(self, message: Message) -> TriggerResponse:
        """
        Generate a help response.
        
        Args:
            message: The incoming message
            
        Returns:
            TriggerResponse with help content
        """
        logger.info(f"Generating help response for chat {message.chat_id}")
        return TriggerResponse(
            response_text=self.predefined_responses.get_help_response(),
            requires_gpt=False,
            response_type="help"
        )
    
    def generate_summary_response(self, message: Message) -> TriggerResponse:
        """
        Generate a summary response (placeholder for GPT integration).
        
        Args:
            message: The incoming message
            
        Returns:
            TriggerResponse with summary content
        """
        logger.info(f"Generating summary response for chat {message.chat_id}")
        
        # For now, return a placeholder response
        # In a full implementation, this would:
        # 1. Fetch recent messages from database
        # 2. Send to GPT for summarization
        # 3. Return the generated summary
        
        summary_text = """📊 **Chat Summary**

🔄 *This is a placeholder summary response.*

In a full implementation, this would:
• Analyze the last 20 messages in this chat
• Use GPT to generate an intelligent summary
• Highlight key topics and important information

To enable full functionality, configure:
• OpenAI API key in environment variables
• Message storage database
• WhatsApp MCP integration"""

        return TriggerResponse(
            response_text=summary_text,
            requires_gpt=True,
            response_type="summary"
        )
    
    def process_message(self, message: Message) -> Optional[TriggerResponse]:
        """
        Process an incoming message and generate a response if triggered.
        
        Args:
            message: The incoming message to process
            
        Returns:
            TriggerResponse if a trigger was detected, None otherwise
        """
        logger.info(f"Processing message from {message.sender_id} in chat {message.chat_id}")
        
        # Detect trigger in message
        trigger_type = self.detect_trigger(message.content)
        
        if not trigger_type:
            logger.debug("No trigger detected in message")
            return None
            
        logger.info(f"Trigger detected: {trigger_type}")
        
        # Generate appropriate response based on trigger type
        if trigger_type == "help":
            return self.generate_help_response(message)
        elif trigger_type == "summary":
            return self.generate_summary_response(message)
        else:
            logger.warning(f"Unknown trigger type: {trigger_type}")
            return None
    
    def should_respond_to_message(self, message: Message) -> bool:
        """
        Determine if we should respond to a message.
        
        Args:
            message: The message to check
            
        Returns:
            True if we should respond, False otherwise
        """
        # Don't respond to our own messages (assuming we have a bot ID)
        # This would need to be configured with the actual bot ID
        # if message.sender_id == config.BOT_ID:
        #     return False
            
        # Don't respond to very old messages (older than 5 minutes)
        if time.time() - message.timestamp > 300:
            logger.debug("Message too old, not responding")
            return False
            
        return True

class AutoReplyBot:
    """Main bot class that orchestrates auto-reply functionality."""
    
    def __init__(self):
        """Initialize the auto-reply bot."""
        self.message_handler = MessageHandler()
        
    def handle_incoming_message(self, message_data: Dict[str, Any]) -> Optional[str]:
        """
        Handle an incoming message and return a response if appropriate.
        
        Args:
            message_data: Raw message data from WhatsApp MCP
            
        Returns:
            Response text if a trigger was detected, None otherwise
        """
        try:
            # Validate that we have minimum required fields
            if not isinstance(message_data, dict):
                logger.error("Message data is not a dictionary")
                return PredefinedResponses.get_error_response()
                
            # Parse message data into Message object
            message = Message(
                chat_id=message_data.get('chat_id', ''),
                sender_id=message_data.get('sender_id', ''),
                content=message_data.get('content', ''),
                timestamp=message_data.get('timestamp', time.time()),
                message_id=message_data.get('message_id')
            )
            
            # Validate that we have minimum required fields
            if not message.content:
                logger.warning("Message has no content, skipping")
                return None
            
            # Check if we should respond to this message
            if not self.message_handler.should_respond_to_message(message):
                return None
                
            # Process the message for triggers
            response = self.message_handler.process_message(message)
            
            if response:
                logger.info(f"Generated {response.response_type} response")
                # Add a small delay to simulate natural response timing
                time.sleep(config.RESPONSE_DELAY)
                return response.response_text
                
            return None
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return PredefinedResponses.get_error_response()