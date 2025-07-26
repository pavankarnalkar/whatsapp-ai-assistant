"""Tests for message processor functionality."""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.message_processor import MessageProcessor


class TestMessageProcessor(unittest.TestCase):
    """Test cases for the MessageProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = MessageProcessor()
    
    def test_process_urgent_message(self):
        """Test processing of urgent messages."""
        message_data = {
            'text': 'This is urgent, please help!',
            'sender': 'test_user',
            'chat_id': 'test_chat',
            'timestamp': datetime.now()
        }
        
        with patch.object(self.processor.email_notifier, 'send_urgent_alert', return_value=True):
            result = self.processor.process_message(message_data)
        
        self.assertTrue(result['is_urgent'])
        self.assertIn('urgent', result['matched_keywords'])
        self.assertTrue(result['email_sent'])
        self.assertIsInstance(result['processing_timestamp'], datetime)
    
    def test_process_normal_message(self):
        """Test processing of normal messages."""
        message_data = {
            'text': 'Hello, how are you doing today?',
            'sender': 'test_user',
            'chat_id': 'test_chat'
        }
        
        result = self.processor.process_message(message_data)
        
        self.assertFalse(result['is_urgent'])
        self.assertEqual(result['matched_keywords'], [])
        self.assertFalse(result['email_sent'])
        self.assertIsInstance(result['processing_timestamp'], datetime)
    
    def test_process_urgent_message_email_failure(self):
        """Test processing urgent message when email sending fails."""
        message_data = {
            'text': 'Emergency! Need immediate help!',
            'sender': 'test_user'
        }
        
        with patch.object(self.processor.email_notifier, 'send_urgent_alert', return_value=False):
            result = self.processor.process_message(message_data)
        
        self.assertTrue(result['is_urgent'])
        self.assertIn('emergency', result['matched_keywords'])
        self.assertIn('immediate', result['matched_keywords'])
        self.assertFalse(result['email_sent'])
    
    def test_process_invalid_message_data(self):
        """Test processing with invalid message data."""
        invalid_inputs = [
            None,
            {},
            {'sender': 'test_user'},  # Missing 'text'
            {'text': ''},  # Empty text
        ]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                result = self.processor.process_message(invalid_input)
                
                self.assertFalse(result['is_urgent'])
                self.assertEqual(result['matched_keywords'], [])
                self.assertFalse(result['email_sent'])
                self.assertIn('error', result)
    
    def test_system_test(self):
        """Test the system test functionality."""
        with patch.object(self.processor.email_notifier, 'test_email_configuration', return_value=True):
            result = self.processor.test_system()
        
        # Check structure of test results
        self.assertIn('urgency_detection_tests', result)
        self.assertIn('email_configuration_test', result)
        self.assertIn('test_timestamp', result)
        
        # Check urgency detection tests
        urgency_tests = result['urgency_detection_tests']
        self.assertIsInstance(urgency_tests, list)
        self.assertGreater(len(urgency_tests), 0)
        
        # Verify that some test messages are detected as urgent
        urgent_detected = any(test['is_urgent'] for test in urgency_tests)
        self.assertTrue(urgent_detected, "At least one test message should be detected as urgent")
        
        # Verify email configuration test
        self.assertTrue(result['email_configuration_test'])


if __name__ == "__main__":
    unittest.main()