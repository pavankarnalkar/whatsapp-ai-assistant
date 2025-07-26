"""Urgency detection module for WhatsApp messages."""

import re
from typing import List
from .config import Config


class UrgencyDetector:
    """Detects urgent messages based on keywords and patterns."""
    
    def __init__(self, keywords: List[str] = None):
        """Initialize the urgency detector with keywords.
        
        Args:
            keywords: List of keywords to detect urgency. If None, uses config defaults.
        """
        self.keywords = keywords or Config.get_urgency_keywords()
        # Create regex pattern for case-insensitive matching
        self.pattern = self._create_pattern()
    
    def _create_pattern(self) -> re.Pattern:
        """Create a regex pattern from keywords."""
        # Escape special regex characters and join with OR
        escaped_keywords = [re.escape(keyword) for keyword in self.keywords]
        # Use negative lookbehind and lookahead to ensure the keyword is not part of a larger word
        # This handles cases like "non-urgent" where "urgent" should not match
        pattern = r'(?<![a-zA-Z\-])(' + '|'.join(escaped_keywords) + r')(?![a-zA-Z\-])'
        return re.compile(pattern, re.IGNORECASE)
    
    def is_urgent(self, message: str) -> bool:
        """Check if a message contains urgent keywords.
        
        Args:
            message: The message text to analyze
            
        Returns:
            True if the message is detected as urgent, False otherwise
        """
        if not message or not isinstance(message, str) or not message.strip():
            return False
            
        return bool(self.pattern.search(message))
    
    def get_matched_keywords(self, message: str) -> List[str]:
        """Get all urgency keywords found in the message.
        
        Args:
            message: The message text to analyze
            
        Returns:
            List of matched keywords (lowercased)
        """
        if not message or not isinstance(message, str) or not message.strip():
            return []
            
        matches = self.pattern.findall(message)
        return [match.lower() for match in matches]