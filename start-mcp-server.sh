#!/bin/bash

# Start MCP Server Script
# This script starts the Python MCP server that provides tools for Claude

echo "🐍 Starting WhatsApp MCP Server..."
echo "🔧 This provides the MCP tools for Claude to interact with WhatsApp"
echo ""

cd whatsapp-mcp/whatsapp-mcp-server

echo "▶️  Running MCP server..."
uv run main.py