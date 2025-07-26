"""Tests for urgency detection functionality."""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.urgency_detector import UrgencyDetector


class TestUrgencyDetector(unittest.TestCase):
    """Test cases for the UrgencyDetector class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.detector = UrgencyDetector()
    
    def test_urgent_keywords_detection(self):
        """Test detection of urgent keywords."""
        urgent_messages = [
            "This is urgent!",
            "URGENT: Please respond",
            "Need help ASAP",
            "Emergency situation",
            "This is critical",
            "Immediate response needed",
            "HELP me please"
        ]
        
        for message in urgent_messages:
            with self.subTest(message=message):
                self.assertTrue(
                    self.detector.is_urgent(message),
                    f"Message '{message}' should be detected as urgent"
                )
    
    def test_non_urgent_messages(self):
        """Test that normal messages are not detected as urgent."""
        normal_messages = [
            "Hello, how are you?",
            "Just checking in",
            "Have a great day",
            "Thanks for the update",
            "See you later",
            "Random message without keywords"
        ]
        
        for message in normal_messages:
            with self.subTest(message=message):
                self.assertFalse(
                    self.detector.is_urgent(message),
                    f"Message '{message}' should not be detected as urgent"
                )
    
    def test_case_insensitive_detection(self):
        """Test that detection is case insensitive."""
        test_cases = [
            "URGENT",
            "urgent",
            "Urgent",
            "uRgEnT",
            "ASAP",
            "asap",
            "AsCeP"  # This should not match
        ]
        
        expected_results = [True, True, True, True, True, True, False]
        
        for message, expected in zip(test_cases, expected_results):
            with self.subTest(message=message):
                result = self.detector.is_urgent(message)
                self.assertEqual(
                    result, expected,
                    f"Message '{message}' detection result should be {expected}"
                )
    
    def test_word_boundary_detection(self):
        """Test that keywords are detected only as whole words."""
        test_cases = [
            ("urgent", True),  # Whole word
            ("urgently", False),  # Part of word
            ("non-urgent", False),  # Part of compound word
            ("urgent!", True),  # With punctuation
            ("Is this urgent?", True),  # In sentence
            ("surgent", False),  # Similar but different word
        ]
        
        for message, expected in test_cases:
            with self.subTest(message=message):
                result = self.detector.is_urgent(message)
                self.assertEqual(
                    result, expected,
                    f"Message '{message}' detection result should be {expected}"
                )
    
    def test_get_matched_keywords(self):
        """Test getting matched keywords from messages."""
        test_cases = [
            ("This is urgent and critical", ["urgent", "critical"]),
            ("HELP! This is an emergency", ["help", "emergency"]),
            ("Just a normal message", []),
            ("urgent ASAP immediate", ["urgent", "asap", "immediate"]),
        ]
        
        for message, expected_keywords in test_cases:
            with self.subTest(message=message):
                result = self.detector.get_matched_keywords(message)
                self.assertEqual(
                    sorted(result), sorted(expected_keywords),
                    f"Message '{message}' should match keywords {expected_keywords}"
                )
    
    def test_empty_and_invalid_inputs(self):
        """Test handling of empty and invalid inputs."""
        invalid_inputs = [None, "", "   ", 123, [], {}]
        
        for invalid_input in invalid_inputs:
            with self.subTest(input=invalid_input):
                result = self.detector.is_urgent(invalid_input)
                self.assertFalse(
                    result,
                    f"Invalid input {invalid_input} should return False"
                )
                
                keywords = self.detector.get_matched_keywords(invalid_input)
                self.assertEqual(
                    keywords, [],
                    f"Invalid input {invalid_input} should return empty keyword list"
                )
    
    def test_custom_keywords(self):
        """Test detector with custom keywords."""
        custom_keywords = ["priority", "rush", "escalate"]
        detector = UrgencyDetector(custom_keywords)
        
        # Should detect custom keywords
        self.assertTrue(detector.is_urgent("This is priority"))
        self.assertTrue(detector.is_urgent("Rush this please"))
        self.assertTrue(detector.is_urgent("Need to escalate"))
        
        # Should not detect default keywords
        self.assertFalse(detector.is_urgent("This is urgent"))
        self.assertFalse(detector.is_urgent("ASAP please"))


if __name__ == "__main__":
    unittest.main()