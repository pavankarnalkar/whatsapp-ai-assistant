#!/bin/bash

# Start WhatsApp Bridge Script
# This script starts the Go WhatsApp bridge that handles authentication and message storage

echo "🔗 Starting WhatsApp Bridge..."
echo "📱 You will be prompted to scan a QR code with your WhatsApp mobile app"
echo "🔒 After scanning, your session will be saved for future use"
echo ""

cd whatsapp-mcp/whatsapp-bridge

# Create store directory if it doesn't exist
mkdir -p store

echo "▶️  Running WhatsApp bridge..."
go run main.go