#!/bin/bash

# WhatsApp AI Assistant Setup Script
# Sets up ngrok tunnel and starts the webhook server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}WhatsApp AI Assistant - ngrok Tunnel Setup${NC}"
echo "=================================================="

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}Error: pip3 is not installed${NC}"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${YELLOW}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}Creating .env file from template...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your configuration${NC}"
    echo "Required: NGROK_AUTH_TOKEN (get from https://ngrok.com)"
    echo "Optional: MCP_SERVER_URL, WEBHOOK_PORT, NGROK_SUBDOMAIN"
    echo ""
    read -p "Press Enter when you've configured the .env file..."
fi

# Function to run webhook server in background
start_webhook_server() {
    echo -e "${YELLOW}Starting webhook server...${NC}"
    python3 app.py &
    WEBHOOK_PID=$!
    echo "Webhook server started with PID: $WEBHOOK_PID"
    
    # Wait a moment for server to start
    sleep 3
    
    # Check if server is running
    if ps -p $WEBHOOK_PID > /dev/null; then
        echo -e "${GREEN}Webhook server is running${NC}"
        return 0
    else
        echo -e "${RED}Failed to start webhook server${NC}"
        return 1
    fi
}

# Function to start ngrok tunnel
start_ngrok_tunnel() {
    echo -e "${YELLOW}Starting ngrok tunnel...${NC}"
    python3 ngrok_tunnel.py
}

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    if [ ! -z "$WEBHOOK_PID" ]; then
        kill $WEBHOOK_PID 2>/dev/null || true
        echo "Webhook server stopped"
    fi
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Set trap for cleanup
trap cleanup EXIT

# Main execution
echo -e "${YELLOW}Starting services...${NC}"

# Start webhook server
if start_webhook_server; then
    # Start ngrok tunnel (this will block until Ctrl+C)
    start_ngrok_tunnel
else
    echo -e "${RED}Failed to start webhook server. Exiting.${NC}"
    exit 1
fi