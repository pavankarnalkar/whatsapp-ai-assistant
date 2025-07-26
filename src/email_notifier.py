"""Email notification module for urgent messages."""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional, Dict, Any
from .config import Config


class EmailNotifier:
    """Handles email notifications for urgent messages."""
    
    def __init__(self):
        """Initialize the email notifier with configuration."""
        self.config = Config()
        self.logger = logging.getLogger(__name__)
    
    def send_urgent_alert(self, message_data: Dict[str, Any]) -> bool:
        """Send an email alert for an urgent message.
        
        Args:
            message_data: Dictionary containing message information with keys:
                - text: The message text
                - sender: Sender identifier (optional)
                - chat_id: Chat identifier (optional)
                - timestamp: Message timestamp (optional)
                - matched_keywords: List of matched urgency keywords (optional)
        
        Returns:
            True if email was sent successfully, False otherwise
        """
        if not self.config.is_smtp_configured():
            self.logger.error("SMTP configuration is incomplete")
            return False
        
        try:
            # Create the email message
            msg = self._create_email_message(message_data)
            
            # Send the email
            with smtplib.SMTP(self.config.SMTP_HOST, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                
                text = msg.as_string()
                server.sendmail(
                    self.config.SMTP_FROM_EMAIL,
                    self.config.SMTP_TO_EMAIL,
                    text
                )
            
            self.logger.info(f"Urgent message alert sent successfully to {self.config.SMTP_TO_EMAIL}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send urgent message alert: {str(e)}")
            return False
    
    def _create_email_message(self, message_data: Dict[str, Any]) -> MIMEMultipart:
        """Create the email message for the urgent alert.
        
        Args:
            message_data: Dictionary containing message information
            
        Returns:
            MIMEMultipart email message
        """
        msg = MIMEMultipart()
        msg['From'] = self.config.SMTP_FROM_EMAIL
        msg['To'] = self.config.SMTP_TO_EMAIL
        msg['Subject'] = "🚨 Urgent WhatsApp Message Alert"
        
        # Extract message details
        message_text = message_data.get('text', 'No message text')
        sender = message_data.get('sender', 'Unknown sender')
        chat_id = message_data.get('chat_id', 'Unknown chat')
        timestamp = message_data.get('timestamp', datetime.now())
        matched_keywords = message_data.get('matched_keywords', [])
        
        # Format timestamp if it's a datetime object
        if isinstance(timestamp, datetime):
            timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        else:
            timestamp_str = str(timestamp)
        
        # Create email body
        body = f"""
An urgent message has been detected in your WhatsApp AI Assistant.

📱 Message Details:
• Sender: {sender}
• Chat ID: {chat_id}
• Timestamp: {timestamp_str}
• Detected Keywords: {', '.join(matched_keywords) if matched_keywords else 'None specified'}

📄 Message Content:
{message_text}

---
This is an automated alert from your WhatsApp AI Assistant.
"""
        
        msg.attach(MIMEText(body, 'plain'))
        return msg
    
    def test_email_configuration(self) -> bool:
        """Test the email configuration by sending a test email.
        
        Returns:
            True if test email was sent successfully, False otherwise
        """
        if not self.config.is_smtp_configured():
            self.logger.error("SMTP configuration is incomplete")
            return False
        
        test_message_data = {
            'text': 'This is a test email to verify your SMTP configuration.',
            'sender': 'System Test',
            'chat_id': 'test_chat',
            'timestamp': datetime.now(),
            'matched_keywords': ['test']
        }
        
        try:
            # Create test email
            msg = MIMEMultipart()
            msg['From'] = self.config.SMTP_FROM_EMAIL
            msg['To'] = self.config.SMTP_TO_EMAIL
            msg['Subject'] = "🧪 WhatsApp AI Assistant - Email Configuration Test"
            
            body = """
This is a test email to verify your WhatsApp AI Assistant email configuration.

If you receive this email, your SMTP settings are configured correctly.

---
WhatsApp AI Assistant Configuration Test
"""
            msg.attach(MIMEText(body, 'plain'))
            
            # Send test email
            with smtplib.SMTP(self.config.SMTP_HOST, self.config.SMTP_PORT) as server:
                server.starttls()
                server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                
                text = msg.as_string()
                server.sendmail(
                    self.config.SMTP_FROM_EMAIL,
                    self.config.SMTP_TO_EMAIL,
                    text
                )
            
            self.logger.info("Test email sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send test email: {str(e)}")
            return False