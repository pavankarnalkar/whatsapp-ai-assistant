"""Main message processor for WhatsApp AI Assistant."""

import logging
from datetime import datetime
from typing import Dict, Any, Optional
from .urgency_detector import UrgencyDetector
from .email_notifier import EmailNotifier


class MessageProcessor:
    """Processes incoming WhatsApp messages and handles urgent message alerts."""
    
    def __init__(self):
        """Initialize the message processor with urgency detector and email notifier."""
        self.urgency_detector = UrgencyDetector()
        self.email_notifier = EmailNotifier()
        self.logger = logging.getLogger(__name__)
        
        # Set up basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    
    def process_message(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process an incoming WhatsApp message.
        
        Args:
            message_data: Dictionary containing message information with keys:
                - text: The message text (required)
                - sender: Sender identifier (optional)
                - chat_id: Chat identifier (optional)
                - timestamp: Message timestamp (optional)
        
        Returns:
            Dictionary with processing results including:
                - is_urgent: Boolean indicating if message was detected as urgent
                - matched_keywords: List of matched urgency keywords
                - email_sent: Boolean indicating if email alert was sent
                - processing_timestamp: When the message was processed
        """
        # Validate input
        if not message_data or 'text' not in message_data or not message_data['text'] or not message_data['text'].strip():
            self.logger.error("Invalid message data: missing 'text' field")
            return {
                'is_urgent': False,
                'matched_keywords': [],
                'email_sent': False,
                'processing_timestamp': datetime.now(),
                'error': 'Invalid message data'
            }
        
        message_text = message_data['text']
        self.logger.info(f"Processing message from {message_data.get('sender', 'unknown')}")
        
        # Check for urgency
        is_urgent = self.urgency_detector.is_urgent(message_text)
        matched_keywords = self.urgency_detector.get_matched_keywords(message_text)
        
        result = {
            'is_urgent': is_urgent,
            'matched_keywords': matched_keywords,
            'email_sent': False,
            'processing_timestamp': datetime.now()
        }
        
        # If urgent, send email alert
        if is_urgent:
            self.logger.warning(f"Urgent message detected with keywords: {matched_keywords}")
            
            # Add matched keywords to message data for email
            enhanced_message_data = message_data.copy()
            enhanced_message_data['matched_keywords'] = matched_keywords
            
            # Attempt to send email
            email_sent = self.email_notifier.send_urgent_alert(enhanced_message_data)
            result['email_sent'] = email_sent
            
            if email_sent:
                self.logger.info("Urgent message alert email sent successfully")
            else:
                self.logger.error("Failed to send urgent message alert email")
        
        return result
    
    def test_system(self) -> Dict[str, Any]:
        """Test the urgency detection and email notification system.
        
        Returns:
            Dictionary with test results
        """
        self.logger.info("Running system test...")
        
        # Test urgency detection
        test_messages = [
            "This is urgent, please help!",
            "ASAP response needed",
            "Emergency situation here",
            "Just a regular message",
            "This is critical and immediate"
        ]
        
        urgency_test_results = []
        for msg in test_messages:
            is_urgent = self.urgency_detector.is_urgent(msg)
            keywords = self.urgency_detector.get_matched_keywords(msg)
            urgency_test_results.append({
                'message': msg,
                'is_urgent': is_urgent,
                'keywords': keywords
            })
        
        # Test email configuration
        email_test_result = self.email_notifier.test_email_configuration()
        
        return {
            'urgency_detection_tests': urgency_test_results,
            'email_configuration_test': email_test_result,
            'test_timestamp': datetime.now()
        }