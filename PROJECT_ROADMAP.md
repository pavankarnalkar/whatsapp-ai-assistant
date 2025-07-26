# WhatsApp AI Assistant - Project Roadmap

This document tracks the implementation progress of all features for the WhatsApp AI assistant project.

## Phase 1: Foundation Setup ✅

- [x] **Set up whatsapp-mcp server locally**
  - [x] Clone the whatsapp-mcp repository
  - [x] Install dependencies (Go, Python, uv)
  - [x] Create setup scripts and documentation
  - [x] Test WhatsApp bridge can start
  - [x] Test MCP server can start
  - [x] Generate Claude Desktop configuration

## Phase 2: Backend Integration (Planned)

- [ ] **Build webhook listener for MCP messages**
  - [ ] Create Flask/FastAPI endpoint
  - [ ] Parse sender ID, chat ID, timestamp, and message text
  - [ ] Store each message to SQLite

- [ ] **Send message replies using MCP REST API**
  - [ ] Create function to send messages via MCP `/message` endpoint
  - [ ] Support recipient ID and text body
  - [ ] Test with static reply to incoming messages

- [ ] **Store and retrieve chat history from SQLite**
  - [ ] Set up SQLite table for messages (chat_id, sender, timestamp, content)
  - [ ] Add functions to fetch last 50 messages by chat_id

## Phase 3: AI Integration (Planned)

- [ ] **Integrate OpenAI GPT for summarization and Q&A**
  - [ ] Create LLM client for GPT-3.5 via OpenAI API
  - [ ] Use it to summarize recent messages or answer questions

- [ ] **Auto-reply to specific triggers**
  - [ ] Detect keywords in incoming messages ('help', 'summary')
  - [ ] Reply with predefined or GPT-generated responses
  - [ ] Support '/summary' command to summarize chat

## Phase 4: Advanced Features (Planned)

- [ ] **Detect urgent messages and trigger email notifications**
  - [ ] Implement urgency detector using keywords ('urgent', 'asap', etc)
  - [ ] Send email alerts using SMTP for urgent messages

- [ ] **Stream responses from GPT to simulate typing**
  - [ ] Send multiple parts for long messages
  - [ ] Add typing indicator via MCP (if supported)

## Phase 5: Deployment (Planned)

- [ ] **Run ngrok tunnel and connect webhook to MCP**
  - [ ] Use ngrok to expose local webhook
  - [ ] Update MCP config to use ngrok URL as webhook target

- [ ] **Deploy backend on Railway or Fly.io**
  - [ ] Prepare Dockerfile
  - [ ] Deploy assistant backend to cloud platform
  - [ ] Ensure MCP can reach it via HTTPS webhook

## Current Status

✅ **COMPLETED**: Phase 1 - Foundation Setup
- WhatsApp MCP server is ready to use locally
- All setup scripts and documentation created
- Ready for authentication with WhatsApp
- Claude Desktop integration configured

🚧 **NEXT UP**: Phase 2 - Backend Integration
- The foundation is now in place to build the webhook listener and message processing system

## Quick Start (Current)

1. Run `./setup.sh` to install dependencies
2. Run `./start-bridge.sh` and scan QR code with WhatsApp
3. Run `./start-mcp-server.sh` to start the MCP server
4. Run `./generate-claude-config.sh` to configure Claude Desktop
5. Start building the webhook integration (next phase)

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   WhatsApp      │    │  Go Bridge       │    │  Python MCP     │
│   Mobile App    │◄──►│  (Authentication │◄──►│  Server         │
│                 │    │   & Storage)     │    │  (Tools)        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  SQLite Database │    │  Claude Desktop │
                       │  (Messages)      │    │  (AI Assistant) │
                       └──────────────────┘    └─────────────────┘
```

The foundation is complete and ready for the next development phase!