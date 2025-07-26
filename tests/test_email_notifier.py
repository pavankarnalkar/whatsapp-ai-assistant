"""Tests for email notification functionality."""

import unittest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.email_notifier import EmailNotifier


class TestEmailNotifier(unittest.TestCase):
    """Test cases for the EmailNotifier class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.notifier = EmailNotifier()
    
    def test_smtp_not_configured(self):
        """Test behavior when SMTP is not configured."""
        # Mock the is_smtp_configured method to return False
        with patch.object(self.notifier.config, 'is_smtp_configured', return_value=False):
            message_data = {
                'text': 'Test urgent message',
                'sender': 'test_user',
                'chat_id': 'test_chat'
            }
            
            result = self.notifier.send_urgent_alert(message_data)
            self.assertFalse(result)
    
    @patch('src.email_notifier.smtplib.SMTP')
    def test_successful_email_send(self, mock_smtp):
        """Test successful email sending."""
        # Mock configuration by setting attributes directly on the notifier's config
        self.notifier.config.SMTP_HOST = 'smtp.test.com'
        self.notifier.config.SMTP_PORT = 587
        self.notifier.config.SMTP_USERNAME = 'test@test.com'
        self.notifier.config.SMTP_PASSWORD = 'password'
        self.notifier.config.SMTP_FROM_EMAIL = 'from@test.com'
        self.notifier.config.SMTP_TO_EMAIL = 'to@test.com'
        
        # Mock the is_smtp_configured method
        with patch.object(self.notifier.config, 'is_smtp_configured', return_value=True):
            # Mock SMTP server
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server
            
            message_data = {
                'text': 'This is an urgent message!',
                'sender': 'test_user',
                'chat_id': 'test_chat',
                'timestamp': datetime.now(),
                'matched_keywords': ['urgent']
            }
            
            result = self.notifier.send_urgent_alert(message_data)
            
            # Verify result
            self.assertTrue(result)
            
            # Verify SMTP calls
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with('test@test.com', 'password')
            mock_server.sendmail.assert_called_once()
    
    @patch('src.email_notifier.smtplib.SMTP')
    def test_email_send_failure(self, mock_smtp):
        """Test email sending failure."""
        # Mock configuration
        with patch.object(self.notifier.config, 'is_smtp_configured', return_value=True):
            # Mock SMTP to raise exception
            mock_smtp.side_effect = Exception("SMTP Error")
            
            message_data = {
                'text': 'Test urgent message',
                'sender': 'test_user'
            }
            
            result = self.notifier.send_urgent_alert(message_data)
            self.assertFalse(result)
    
    def test_create_email_message(self):
        """Test email message creation."""
        message_data = {
            'text': 'This is urgent!',
            'sender': 'john_doe',
            'chat_id': 'family_chat',
            'timestamp': datetime(2024, 1, 15, 10, 30, 0),
            'matched_keywords': ['urgent']
        }
        
        # Access the private method for testing
        msg = self.notifier._create_email_message(message_data)
        
        # Check message properties
        self.assertEqual(msg['Subject'], "🚨 Urgent WhatsApp Message Alert")
        
        # Get the plain text content
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_payload(decode=True).decode('utf-8')
                self.assertIn('john_doe', content)
                self.assertIn('family_chat', content)
                self.assertIn('This is urgent!', content)
                self.assertIn('urgent', content)
                break
    
    def test_create_email_message_minimal_data(self):
        """Test email message creation with minimal data."""
        message_data = {
            'text': 'Help needed'
        }
        
        msg = self.notifier._create_email_message(message_data)
        
        # Should handle missing fields gracefully
        self.assertEqual(msg['Subject'], "🚨 Urgent WhatsApp Message Alert")
        
        # Get the plain text content
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                content = part.get_payload(decode=True).decode('utf-8')
                self.assertIn('Help needed', content)
                self.assertIn('Unknown sender', content)
                self.assertIn('Unknown chat', content)
                break


if __name__ == "__main__":
    unittest.main()