#!/usr/bin/env python3
"""
ngrok Tunnel Manager for WhatsApp AI Assistant
Automatically starts ngrok tunnel and configures MCP webhook URL
"""

import os
import sys
import time
import json
import requests
import logging
from pyngrok import ngrok, conf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NgrokTunnelManager:
    def __init__(self):
        self.webhook_port = int(os.getenv('WEBHOOK_PORT', 5000))
        self.mcp_server_url = os.getenv('MCP_SERVER_URL', 'http://localhost:3000')
        self.ngrok_auth_token = os.getenv('NGROK_AUTH_TOKEN')
        self.ngrok_subdomain = os.getenv('NGROK_SUBDOMAIN')
        self.tunnel = None
        
    def setup_ngrok(self):
        """Configure ngrok with auth token"""
        if self.ngrok_auth_token:
            conf.get_default().auth_token = self.ngrok_auth_token
            logger.info("ngrok auth token configured")
        else:
            logger.warning("No ngrok auth token found. Using free tier limitations.")
    
    def start_tunnel(self):
        """Start ngrok tunnel for the webhook port"""
        try:
            # Configure tunnel options
            tunnel_options = {
                "addr": self.webhook_port,
                "proto": "http"
            }
            
            # Add subdomain if specified (requires paid plan)
            if self.ngrok_subdomain:
                tunnel_options["subdomain"] = self.ngrok_subdomain
                
            # Start the tunnel
            self.tunnel = ngrok.connect(**tunnel_options)
            public_url = self.tunnel.public_url
            
            logger.info(f"ngrok tunnel started: {public_url}")
            logger.info(f"Webhook endpoint: {public_url}/webhook")
            
            return public_url
            
        except Exception as e:
            logger.error(f"Failed to start ngrok tunnel: {str(e)}")
            return None
    
    def update_mcp_webhook(self, webhook_url):
        """Update MCP server with the new webhook URL"""
        try:
            webhook_endpoint = f"{webhook_url}/webhook"
            
            # Attempt to update MCP webhook configuration
            # This is a placeholder - actual MCP API may differ
            mcp_config_url = f"{self.mcp_server_url}/config/webhook"
            
            payload = {
                "webhook_url": webhook_endpoint,
                "events": ["message_received"]
            }
            
            response = requests.post(mcp_config_url, json=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"Successfully updated MCP webhook to: {webhook_endpoint}")
                return True
            else:
                logger.warning(f"MCP webhook update failed with status {response.status_code}: {response.text}")
                logger.info(f"Manual configuration required. Set webhook URL to: {webhook_endpoint}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.warning(f"Could not connect to MCP server: {str(e)}")
            logger.info(f"Manual configuration required. Set webhook URL to: {webhook_endpoint}")
            return False
    
    def stop_tunnel(self):
        """Stop the ngrok tunnel"""
        if self.tunnel:
            ngrok.disconnect(self.tunnel.public_url)
            logger.info("ngrok tunnel stopped")
    
    def get_tunnel_info(self):
        """Get information about active tunnels"""
        if self.tunnel:
            return {
                "public_url": self.tunnel.public_url,
                "webhook_endpoint": f"{self.tunnel.public_url}/webhook",
                "local_port": self.webhook_port
            }
        return None

def main():
    """Main function to start ngrok tunnel and configure MCP"""
    tunnel_manager = NgrokTunnelManager()
    
    try:
        # Setup ngrok
        tunnel_manager.setup_ngrok()
        
        # Start tunnel
        public_url = tunnel_manager.start_tunnel()
        if not public_url:
            logger.error("Failed to start ngrok tunnel. Exiting.")
            sys.exit(1)
        
        # Update MCP webhook configuration
        webhook_updated = tunnel_manager.update_mcp_webhook(public_url)
        
        # Display connection information
        tunnel_info = tunnel_manager.get_tunnel_info()
        print("\n" + "="*60)
        print("NGROK TUNNEL ACTIVE")
        print("="*60)
        print(f"Public URL: {tunnel_info['public_url']}")
        print(f"Webhook Endpoint: {tunnel_info['webhook_endpoint']}")
        print(f"Local Port: {tunnel_info['local_port']}")
        print(f"MCP Server: {tunnel_manager.mcp_server_url}")
        print(f"Webhook Updated: {'Yes' if webhook_updated else 'Manual setup required'}")
        print("="*60)
        
        if not webhook_updated:
            print("\nMANUAL SETUP REQUIRED:")
            print(f"Configure your MCP server to send webhooks to:")
            print(f"{tunnel_info['webhook_endpoint']}")
            print()
        
        print("Press Ctrl+C to stop the tunnel")
        
        # Keep the tunnel alive
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\nShutting down tunnel...")
            tunnel_manager.stop_tunnel()
            print("Tunnel stopped.")
            
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()