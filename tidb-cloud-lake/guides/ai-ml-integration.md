---
title: AI & ML Integration
summary: Databend enables powerful AI and ML capabilities through two complementary approaches build custom AI functions with your own infrastructure, or create conversational data experiences using natural language.
---
# AI & ML Integration

Databend enables powerful AI and ML capabilities through two complementary approaches: build custom AI functions with your own infrastructure, or create conversational data experiences using natural language.

## External Functions - The Recommended Approach

External functions enable you to connect your data with custom AI/ML infrastructure, providing maximum flexibility and performance for AI workloads.

| Feature | Benefits |
|---------|----------|
| **Custom Models** | Use any open-source or proprietary AI/ML models |
| **GPU Acceleration** | Deploy on GPU-equipped machines for faster inference |
| **Data Privacy** | Keep your data within your infrastructure |
| **Scalability** | Independent scaling and resource optimization |
| **Flexibility** | Support for any programming language and ML framework |

## MCP Server - Natural Language Data Interaction

The Model Context Protocol (MCP) server enables AI assistants to interact with your Databend database using natural language, perfect for building conversational BI tools.

| Feature | Benefits |
|---------|----------|
| **Natural Language** | Query your data using plain English |
| **AI Assistant Integration** | Works with Claude, ChatGPT, and custom agents |
| **Real-time Analysis** | Get instant insights from your data |

## Getting Started

**[External Functions Guide](/tidb-cloud-lake/guides/external-ai-functions.md)** - Learn how to create and deploy custom AI functions with practical examples and implementation guidance

**[MCP Server Guide](/tidb-cloud-lake/guides/mcp-server.md)** - Build a conversational BI tool using mcp-databend and natural language queries

**[MCP Client Integration](/tidb-cloud-lake/guides/mcp-client-integration.md)** - Configure generic MCP clients (like Codex) to connect to Databend
