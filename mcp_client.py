"""
MCP REST API Client for sending WhatsApp messages.
"""
import os
import requests
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class MCPClient:
    """Client for interacting with the WhatsApp MCP REST API."""
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize MCP client.
        
        Args:
            base_url: Base URL for the MCP server (defaults to env var MCP_BASE_URL)
            api_key: API key for authentication (defaults to env var MCP_API_KEY)
        """
        self.base_url = base_url or os.getenv('MCP_BASE_URL', 'http://localhost:3000')
        self.api_key = api_key or os.getenv('MCP_API_KEY')
        self.session = requests.Session()
        
        if self.api_key:
            self.session.headers.update({'Authorization': f'Bearer {self.api_key}'})
    
    def send_message(self, recipient_id: str, text: str) -> dict:
        """
        Send a message via the MCP /message endpoint.
        
        Args:
            recipient_id: The recipient's WhatsApp ID (phone number or chat ID)
            text: The message text to send
            
        Returns:
            dict: Response from the MCP API
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/message"
        payload = {
            "recipient": recipient_id,
            "text": text
        }
        
        try:
            response = self.session.post(url, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending message to {recipient_id}: {e}")
            raise
    
    def send_reply(self, recipient_id: str, text: str) -> bool:
        """
        Send a reply message and return success status.
        
        Args:
            recipient_id: The recipient's WhatsApp ID
            text: The reply text to send
            
        Returns:
            bool: True if message was sent successfully, False otherwise
        """
        try:
            result = self.send_message(recipient_id, text)
            print(f"Message sent successfully to {recipient_id}: {result}")
            return True
        except Exception as e:
            print(f"Failed to send message to {recipient_id}: {e}")
            return False