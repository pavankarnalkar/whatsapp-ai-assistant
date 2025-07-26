#!/bin/bash

# Generate Claude Desktop Configuration
# This script generates the configuration needed for Claude Desktop integration

echo "🔧 Generating Claude Desktop Configuration..."
echo ""

# Get current directory
CURRENT_DIR=$(pwd)
UV_PATH=$(which uv)

if [ -z "$UV_PATH" ]; then
    echo "❌ Error: uv not found. Please run ./setup.sh first"
    exit 1
fi

echo "📍 Detected paths:"
echo "   uv path: $UV_PATH"
echo "   project path: $CURRENT_DIR"
echo ""

# Generate configuration
cat > claude_config.json << EOF
{
  "mcpServers": {
    "whatsapp": {
      "command": "$UV_PATH",
      "args": [
        "--directory",
        "$CURRENT_DIR/whatsapp-mcp/whatsapp-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
EOF

echo "✅ Configuration generated in 'claude_config.json'"
echo ""
echo "📋 To configure Claude Desktop:"
echo ""
echo "1. Copy the configuration file to the appropriate location:"
echo "   macOS: ~/Library/Application Support/Claude/claude_desktop_config.json"
echo "   Linux: ~/.config/claude/claude_desktop_config.json"
echo ""
echo "2. Run this command to copy it:"
echo "   # For macOS:"
echo "   mkdir -p \"~/Library/Application Support/Claude\" && cp claude_config.json \"~/Library/Application Support/Claude/claude_desktop_config.json\""
echo ""
echo "   # For Linux:"
echo "   mkdir -p ~/.config/claude && cp claude_config.json ~/.config/claude/claude_desktop_config.json"
echo ""
echo "3. Restart Claude Desktop"
echo ""
echo "📄 Configuration content:"
cat claude_config.json