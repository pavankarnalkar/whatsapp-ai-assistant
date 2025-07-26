#!/bin/bash

# Deploy to Railway
# This script helps deploy the WhatsApp AI Assistant to Railway

echo "🚂 Deploying WhatsApp AI Assistant to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Please install it first:"
    echo "   npm install -g @railway/cli"
    exit 1
fi

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway first:"
    echo "   railway login"
    exit 1
fi

# Deploy the application
echo "🚀 Starting deployment..."
railway up

echo "✅ Deployment initiated!"
echo ""
echo "📋 Don't forget to set these environment variables in Railway:"
echo "   - OPENAI_API_KEY: Your OpenAI API key"
echo "   - MCP_BASE_URL: Your MCP server URL (if different from default)"
echo ""
echo "🔗 Configure your MCP webhook to point to:"
echo "   https://your-app-name.railway.app/webhook"