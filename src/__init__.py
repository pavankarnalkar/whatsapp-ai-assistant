"""Package initialization for WhatsApp AI Assistant."""

from .urgency_detector import UrgencyDetector
from .email_notifier import EmailNotifier
from .message_processor import MessageProcessor
from .config import Config

__version__ = "1.0.0"
__all__ = ["UrgencyDetector", "EmailNotifier", "MessageProcessor", "Config"]