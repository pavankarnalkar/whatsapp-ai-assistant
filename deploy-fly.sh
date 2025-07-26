#!/bin/bash

# Deploy to Fly.io
# This script helps deploy the WhatsApp AI Assistant to Fly.io

echo "🛩️ Deploying WhatsApp AI Assistant to Fly.io..."

# Check if Fly CLI is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ Fly CLI not found. Please install it first:"
    echo "   curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# Check if user is logged in
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please login to Fly.io first:"
    echo "   flyctl auth login"
    exit 1
fi

# Launch the application (creates app if it doesn't exist)
if [ ! -f "fly.toml" ]; then
    echo "🚀 Creating new Fly.io application..."
    flyctl launch --no-deploy
fi

# Set environment variables
echo "🔧 Setting environment variables..."
echo "Please enter your OpenAI API key:"
read -s OPENAI_API_KEY
flyctl secrets set OPENAI_API_KEY="$OPENAI_API_KEY"

echo "Enter your MCP base URL (press Enter for default http://localhost:3000):"
read MCP_BASE_URL
if [ ! -z "$MCP_BASE_URL" ]; then
    flyctl secrets set MCP_BASE_URL="$MCP_BASE_URL"
fi

# Deploy the application
echo "🚀 Starting deployment..."
flyctl deploy

echo "✅ Deployment complete!"
echo ""
echo "🔗 Configure your MCP webhook to point to:"
flyctl info | grep "^Hostname" | awk '{print "   https://" $2 "/webhook"}'