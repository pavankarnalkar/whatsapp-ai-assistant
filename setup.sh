#!/bin/bash

# WhatsApp MCP Server Setup Script
# This script sets up the WhatsApp MCP server locally for the AI assistant project

set -e

echo "🚀 Setting up WhatsApp MCP Server..."

# Check if already cloned
if [ ! -d "whatsapp-mcp" ]; then
    echo "📥 Cloning whatsapp-mcp repository..."
    git clone https://github.com/lharries/whatsapp-mcp.git
else
    echo "✅ whatsapp-mcp repository already exists"
fi

cd whatsapp-mcp

echo "📦 Installing Go dependencies..."
cd whatsapp-bridge
go mod download
go mod tidy
cd ..

echo "🐍 Installing Python dependencies..."
cd whatsapp-mcp-server

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "📥 Installing uv package manager..."
    pip3 install uv
fi

uv sync
cd ..

echo "✅ Dependencies installed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Run './start-bridge.sh' to start the WhatsApp bridge"
echo "2. Scan the QR code with your WhatsApp mobile app"
echo "3. Run './start-mcp-server.sh' to start the MCP server"
echo "4. Configure Claude Desktop with the provided configuration"
echo ""
echo "📄 See README.md for detailed configuration instructions"