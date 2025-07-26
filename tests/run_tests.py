"""Test runner for all WhatsApp AI Assistant tests."""

import unittest
import sys
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent
sys.path.insert(0, str(tests_dir))

from test_urgency_detector import TestUrgencyDetector
from test_email_notifier import TestEmailNotifier
from test_message_processor import TestMessageProcessor


def run_all_tests():
    """Run all test suites."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestUrgencyDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestEmailNotifier))
    suite.addTests(loader.loadTestsFromTestCase(TestMessageProcessor))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)