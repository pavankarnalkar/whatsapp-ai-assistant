"""Tests for message handler trigger detection and responses."""

import unittest
import time
from unittest.mock import patch

from message_handler import MessageHandler, AutoReplyBot, Message, TriggerResponse
from responses import PredefinedResponses

class TestMessageHandler(unittest.TestCase):
    """Test cases for MessageHandler class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.handler = MessageHandler()
    
    def test_detect_help_triggers(self):
        """Test detection of help triggers."""
        help_messages = [
            "help",
            "Help",
            "HELP",
            "/help",
            "commands", 
            "/commands",
            "I need help",
            "Can you help me?",
            "What commands do you have?"
        ]
        
        for message in help_messages:
            with self.subTest(message=message):
                trigger = self.handler.detect_trigger(message)
                self.assertEqual(trigger, "help", f"Failed to detect help trigger in: {message}")
    
    def test_detect_summary_triggers(self):
        """Test detection of summary triggers."""
        summary_messages = [
            "/summary",
            "summary",
            "Summary",
            "SUMMARY",
            "/summarize",
            "Can you summarize this chat?",
            "Give me a summary"
        ]
        
        for message in summary_messages:
            with self.subTest(message=message):
                trigger = self.handler.detect_trigger(message)
                self.assertEqual(trigger, "summary", f"Failed to detect summary trigger in: {message}")
    
    def test_no_trigger_detection(self):
        """Test that non-trigger messages return None."""
        non_trigger_messages = [
            "Hello there",
            "How are you?",
            "What's the weather like?",
            "Random message",
            "",
            "   ",
            "helpless",  # Contains 'help' but not as trigger
            "summarizer"  # Contains 'summary' but not as trigger
        ]
        
        for message in non_trigger_messages:
            with self.subTest(message=message):
                trigger = self.handler.detect_trigger(message)
                self.assertIsNone(trigger, f"Incorrectly detected trigger in: {message}")
    
    def test_generate_help_response(self):
        """Test help response generation."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user",
            content="help",
            timestamp=time.time()
        )
        
        response = self.handler.generate_help_response(message)
        
        self.assertIsInstance(response, TriggerResponse)
        self.assertFalse(response.requires_gpt)
        self.assertEqual(response.response_type, "help")
        self.assertIn("WhatsApp AI Assistant", response.response_text)
        self.assertIn("help", response.response_text)
        self.assertIn("/summary", response.response_text)
    
    def test_generate_summary_response(self):
        """Test summary response generation."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user", 
            content="/summary",
            timestamp=time.time()
        )
        
        response = self.handler.generate_summary_response(message)
        
        self.assertIsInstance(response, TriggerResponse)
        self.assertTrue(response.requires_gpt)
        self.assertEqual(response.response_type, "summary")
        self.assertIn("Chat Summary", response.response_text)
    
    def test_process_message_with_trigger(self):
        """Test processing a message with a trigger."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user",
            content="help",
            timestamp=time.time()
        )
        
        response = self.handler.process_message(message)
        
        self.assertIsNotNone(response)
        self.assertEqual(response.response_type, "help")
    
    def test_process_message_without_trigger(self):
        """Test processing a message without a trigger."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user",
            content="Hello there",
            timestamp=time.time()
        )
        
        response = self.handler.process_message(message)
        
        self.assertIsNone(response)
    
    def test_should_respond_to_recent_message(self):
        """Test that we respond to recent messages."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user",
            content="help",
            timestamp=time.time()
        )
        
        should_respond = self.handler.should_respond_to_message(message)
        self.assertTrue(should_respond)
    
    def test_should_not_respond_to_old_message(self):
        """Test that we don't respond to old messages."""
        message = Message(
            chat_id="test_chat",
            sender_id="test_user",
            content="help",
            timestamp=time.time() - 400  # 6+ minutes ago
        )
        
        should_respond = self.handler.should_respond_to_message(message)
        self.assertFalse(should_respond)

class TestAutoReplyBot(unittest.TestCase):
    """Test cases for AutoReplyBot class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.bot = AutoReplyBot()
    
    def test_handle_help_message(self):
        """Test handling a help message."""
        message_data = {
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'help',
            'timestamp': time.time(),
            'message_id': 'test_msg'
        }
        
        response = self.bot.handle_incoming_message(message_data)
        
        self.assertIsNotNone(response)
        self.assertIn("WhatsApp AI Assistant", response)
    
    def test_handle_summary_message(self):
        """Test handling a summary message."""
        message_data = {
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': '/summary',
            'timestamp': time.time(),
            'message_id': 'test_msg'
        }
        
        response = self.bot.handle_incoming_message(message_data)
        
        self.assertIsNotNone(response)
        self.assertIn("Chat Summary", response)
    
    def test_handle_non_trigger_message(self):
        """Test handling a non-trigger message."""
        message_data = {
            'chat_id': 'test_chat',
            'sender_id': 'test_user',
            'content': 'Hello there',
            'timestamp': time.time(),
            'message_id': 'test_msg'
        }
        
        response = self.bot.handle_incoming_message(message_data)
        
        self.assertIsNone(response)
    
    def test_handle_malformed_message(self):
        """Test handling malformed message data."""
        # Test with missing content field
        message_data = {
            'invalid': 'data'
        }
        
        response = self.bot.handle_incoming_message(message_data)
        
        # Should return None since there's no content, not an error
        self.assertIsNone(response)
        
        # Test with non-dict input to trigger error handling
        response2 = self.bot.handle_incoming_message("not a dict")
        
        # Should return error response for completely invalid input
        self.assertIsNotNone(response2)
        self.assertIn("error", response2.lower())

if __name__ == '__main__':
    unittest.main()