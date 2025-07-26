from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
import logging
from datetime import datetime
from models import MessagePayload, StoredMessage
from database import init_database, store_message, get_messages_by_chat, get_message_count

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    logger.info("Starting WhatsApp AI Assistant webhook listener...")
    init_database()
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="WhatsApp AI Assistant Webhook",
    description="Webhook listener for MCP messages from WhatsApp",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "WhatsApp AI Assistant Webhook",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/stats")
async def get_stats():
    """Get basic statistics about stored messages"""
    try:
        total_messages = get_message_count()
        return {
            "total_messages": total_messages,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/webhook/message")
async def receive_message(request: Request):
    """
    Webhook endpoint to receive new message payloads from whatsapp-mcp
    Parses sender ID, chat ID, timestamp, and message text
    Stores each message to SQLite
    """
    try:
        # Get raw payload
        payload = await request.json()
        logger.info(f"Received webhook payload: {payload}")
        
        # Parse the payload into our MessagePayload model
        # Note: The exact structure depends on whatsapp-mcp format
        # This is a reasonable assumption based on common webhook patterns
        message_data = {
            "sender_id": payload.get("sender_id") or payload.get("from") or payload.get("senderId"),
            "chat_id": payload.get("chat_id") or payload.get("chatId") or payload.get("chat"),
            "timestamp": payload.get("timestamp") or payload.get("time") or datetime.now(),
            "message_text": payload.get("message_text") or payload.get("text") or payload.get("body") or payload.get("message"),
            "message_id": payload.get("message_id") or payload.get("messageId") or payload.get("id")
        }
        
        # Validate required fields
        if not message_data["sender_id"]:
            raise HTTPException(status_code=400, detail="Missing sender_id in payload")
        if not message_data["chat_id"]:
            raise HTTPException(status_code=400, detail="Missing chat_id in payload")
        if not message_data["message_text"]:
            raise HTTPException(status_code=400, detail="Missing message_text in payload")
        
        # Handle timestamp conversion if it's a string
        if isinstance(message_data["timestamp"], str):
            try:
                message_data["timestamp"] = datetime.fromisoformat(message_data["timestamp"].replace('Z', '+00:00'))
            except ValueError:
                # If timestamp parsing fails, use current time
                message_data["timestamp"] = datetime.now()
        elif isinstance(message_data["timestamp"], (int, float)):
            # Handle Unix timestamp
            message_data["timestamp"] = datetime.fromtimestamp(message_data["timestamp"])
        elif not isinstance(message_data["timestamp"], datetime):
            message_data["timestamp"] = datetime.now()
        
        # Create and validate message payload
        message = MessagePayload(**message_data)
        
        # Store message to database
        message_id = store_message(message)
        
        logger.info(f"Successfully processed message from {message.sender_id} in chat {message.chat_id}")
        
        return {
            "status": "success",
            "message": "Message received and stored",
            "message_id": message_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/messages/{chat_id}")
async def get_chat_messages(chat_id: str, limit: int = 50):
    """Get messages for a specific chat ID"""
    try:
        if limit < 1 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        messages = get_messages_by_chat(chat_id, limit)
        return {
            "chat_id": chat_id,
            "messages": messages,
            "count": len(messages),
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving messages for chat {chat_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)