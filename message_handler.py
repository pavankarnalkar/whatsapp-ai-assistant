"""Message handler for WhatsApp AI Assistant auto-reply functionality."""

import re
import time
import logging
import asyncio
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

from config import config
from responses import PredefinedResponses
from gpt_client import StreamingGPTClient
from chat_history import ChatHistoryDB

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
    
    def __init__(self, db_path: str = "chat_history.db"):
        """Initialize the message handler."""
        self.predefined_responses = PredefinedResponses()
        self.gpt_client = StreamingGPTClient()
        self.chat_db = ChatHistoryDB(db_path)
        
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
        Generate a summary response using GPT and recent chat history.
        
        Args:
            message: The incoming message
            
        Returns:
            TriggerResponse with summary content
        """
        logger.info(f"Generating summary response for chat {message.chat_id}")
        
        try:
            # Fetch recent messages from database
            recent_messages = self.chat_db.get_recent_messages(message.chat_id, limit=config.MAX_SUMMARY_MESSAGES)
            
            if not recent_messages:
                return TriggerResponse(
                    response_text="📊 **Chat Summary**\n\nNo recent messages found to summarize.",
                    requires_gpt=True,
                    response_type="summary"
                )
            
            # Prepare conversation for GPT
            conversation_text = []
            for sender, timestamp, content, msg_id in recent_messages:
                conversation_text.append(f"{sender}: {content}")
            
            # Reverse to get chronological order (oldest first)
            conversation_text.reverse()
            conversation_str = "\n".join(conversation_text)
            
            # Create GPT prompt for summarization
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant that creates concise summaries of WhatsApp conversations. Provide a brief, organized summary highlighting key topics, decisions, and important information."
                },
                {
                    "role": "user", 
                    "content": f"Please summarize this WhatsApp conversation:\n\n{conversation_str}"
                }
            ]
            
            # Get GPT summary (using async function in sync context)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                summary = loop.run_until_complete(self.gpt_client.get_completion(messages))
            finally:
                loop.close()
            
            return TriggerResponse(
                response_text=f"📊 **Chat Summary**\n\n{summary}",
                requires_gpt=True,
                response_type="summary"
            )
            
        except Exception as e:
            logger.error(f"Error generating GPT summary: {e}")
            return TriggerResponse(
                response_text=f"📊 **Chat Summary**\n\nI found {len(recent_messages) if 'recent_messages' in locals() else 0} recent messages, but I'm having trouble generating a summary right now. Please check that your OpenAI API key is configured correctly.",
                requires_gpt=True,
                response_type="summary"
            )
    
    def generate_qa_response(self, message: Message) -> TriggerResponse:
        """
        Generate a Q&A response using GPT for general questions.
        
        Args:
            message: The incoming message
            
        Returns:
            TriggerResponse with Q&A content
        """
        logger.info(f"Generating Q&A response for chat {message.chat_id}")
        
        try:
            # Get some recent context for better responses
            recent_messages = self.chat_db.get_recent_messages(message.chat_id, limit=5)
            
            # Prepare context from recent messages
            context_messages = []
            for sender, timestamp, content, msg_id in recent_messages:
                role = "assistant" if sender.lower() in ["bot", "assistant", "ai"] else "user"
                context_messages.append({"role": role, "content": content})
            
            # Reverse to get chronological order
            context_messages.reverse()
            
            # Create GPT conversation with context
            messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful WhatsApp AI assistant. Provide concise, friendly, and useful responses. Keep your answers brief but informative."
                }
            ]
            
            # Add recent context (last few messages)
            messages.extend(context_messages[-4:])  # Only use last 4 messages for context
            
            # Add current message
            messages.append({"role": "user", "content": message.content})
            
            # Get GPT response
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(self.gpt_client.get_completion(messages))
            finally:
                loop.close()
            
            return TriggerResponse(
                response_text=response,
                requires_gpt=True,
                response_type="qa"
            )
            
        except Exception as e:
            logger.error(f"Error generating GPT Q&A response: {e}")
            return TriggerResponse(
                response_text="I'm having trouble processing your question right now. Please check that the OpenAI API is configured correctly.",
                requires_gpt=True,
                response_type="qa"
            )
    
    def store_message(self, message: Message) -> bool:
        """
        Store a message in the chat history database.
        
        Args:
            message: The message to store
            
        Returns:
            True if stored successfully, False otherwise
        """
        try:
            from datetime import datetime
            timestamp_str = datetime.fromtimestamp(message.timestamp).isoformat()
            return self.chat_db.store_message(
                chat_id=message.chat_id,
                sender=message.sender_id,
                timestamp=timestamp_str,
                content=message.content
            )
        except Exception as e:
            logger.error(f"Error storing message: {e}")
            return False
    
    def process_message(self, message: Message) -> Optional[TriggerResponse]:
        """
        Process an incoming message and generate a response if triggered.
        
        Args:
            message: The incoming message to process
            
        Returns:
            TriggerResponse if a trigger was detected, None otherwise
        """
        logger.info(f"Processing message from {message.sender_id} in chat {message.chat_id}")
        
        # Store the incoming message in chat history
        self.store_message(message)
        
        # Detect trigger in message
        trigger_type = self.detect_trigger(message.content)
        
        if trigger_type:
            logger.info(f"Trigger detected: {trigger_type}")
            
            # Generate appropriate response based on trigger type
            if trigger_type == "help":
                return self.generate_help_response(message)
            elif trigger_type == "summary":
                return self.generate_summary_response(message)
            else:
                logger.warning(f"Unknown trigger type: {trigger_type}")
                return None
        else:
            # No specific trigger detected - check if we should provide Q&A response
            # For now, only respond to questions (containing ?) or specific keywords
            content_lower = message.content.lower().strip()
            
            # Simple heuristic for when to provide Q&A responses
            should_respond_qa = (
                "?" in message.content or  # Questions
                any(word in content_lower for word in ["what", "how", "why", "when", "where", "who", "explain", "tell me"]) or
                (len(message.content.split()) > 5 and any(word in content_lower for word in ["help", "problem", "issue", "understand"]))  # Longer messages with help keywords
            )
            
            if should_respond_qa:
                logger.info("Generating Q&A response for non-trigger message")
                return self.generate_qa_response(message)
            else:
                logger.debug("No trigger detected and message doesn't warrant Q&A response")
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
                
                # Store the bot response in chat history
                bot_message = Message(
                    chat_id=message.chat_id,
                    sender_id="bot",
                    content=response.response_text,
                    timestamp=time.time()
                )
                self.message_handler.store_message(bot_message)
                
                # Add a small delay to simulate natural response timing
                time.sleep(config.RESPONSE_DELAY)
                return response.response_text
                
            return None
            
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return PredefinedResponses.get_error_response()