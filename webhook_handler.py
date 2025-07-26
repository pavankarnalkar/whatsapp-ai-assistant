"""Webhook handler for receiving messages from WhatsApp MCP server."""

import asyncio
import json
import logging
from typing import Dict, Any
from aiohttp import web, ClientSession
from main import WhatsAppAIAssistant

logger = logging.getLogger(__name__)

class WebhookHandler:
    """Handles incoming webhooks from WhatsApp MCP server."""
    
    def __init__(self):
        self.assistant = WhatsAppAIAssistant()
        self.app = web.Application()
        self.setup_routes()
    
    def setup_routes(self):
        """Setup webhook routes."""
        self.app.router.add_post('/webhook/message', self.handle_incoming_message)
        self.app.router.add_get('/health', self.health_check)
    
    async def health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({"status": "healthy", "service": "whatsapp-ai-assistant"})
    
    async def handle_incoming_message(self, request: web.Request) -> web.Response:
        """Handle incoming message from WhatsApp MCP."""
        try:
            # Parse incoming webhook payload
            payload = await request.json()
            logger.info(f"Received webhook payload: {json.dumps(payload, indent=2)}")
            
            # Extract message details
            chat_id = payload.get('chat_id')
            sender_id = payload.get('sender_id') 
            message_text = payload.get('message', {}).get('text', '')
            timestamp = payload.get('timestamp')
            
            if not chat_id or not message_text:
                logger.warning("Missing required fields in webhook payload")
                return web.json_response(
                    {"error": "Missing chat_id or message text"}, 
                    status=400
                )
            
            # Skip messages from the bot itself
            if sender_id == 'bot' or payload.get('from_bot', False):
                logger.info("Skipping bot message")
                return web.json_response({"status": "skipped"})
            
            # Process message asynchronously to avoid blocking the webhook
            asyncio.create_task(
                self.assistant.handle_message(chat_id, message_text)
            )
            
            return web.json_response({"status": "received"})
            
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook payload")
            return web.json_response({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error handling webhook: {e}")
            return web.json_response(
                {"error": "Internal server error"}, 
                status=500
            )
    
    async def start_server(self, host: str = '0.0.0.0', port: int = 8000):
        """Start the webhook server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()
        logger.info(f"Webhook server started on {host}:{port}")
        return runner

if __name__ == "__main__":
    async def main():
        """Run the webhook server."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        handler = WebhookHandler()
        runner = await handler.start_server()
        
        logger.info("Webhook server is running. Press Ctrl+C to stop.")
        
        try:
            # Keep the server running
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down webhook server...")
            await runner.cleanup()
    
    asyncio.run(main())