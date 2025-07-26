from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MessagePayload(BaseModel):
    """Model for incoming WhatsApp message payload from MCP"""
    sender_id: str
    chat_id: str
    timestamp: datetime
    message_text: str
    message_id: Optional[str] = None


class StoredMessage(BaseModel):
    """Model for messages stored in database"""
    id: int
    sender_id: str
    chat_id: str
    timestamp: datetime
    message_text: str
    message_id: Optional[str] = None
    created_at: datetime