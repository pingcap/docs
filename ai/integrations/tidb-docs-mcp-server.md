---
title: TiDB Docs MCP Server
summary: Connect AI clients to TiDB documentation through an MCP server with search tools and markdown resources.
---

# TiDB Docs MCP Server

TiDB Docs MCP Server exposes TiDB documentation to MCP-compatible AI clients such as Claude Code, Claude Desktop, VS Code, Cursor, and other tools.

It supports:

- **STDIO transport** for local development
- **HTTP transport** for shared environments (for example, staging)
- **Bearer token authentication**
- **Source isolation** (for example, `staging` vs `prod`)

## What you get

The server provides structured tools and resources for docs access:

- Search by feature, topic, path, and full-text
- Fetch full markdown for a single document on demand
- List topics and feature tokens
- Reload index after docs updates

## Prerequisites

- Node.js 18 or later
- TiDB docs repository cloned locally

## Start the server

### Start with STDIO transport

```bash
npm run docs-mcp:serve
```

Optionally use `docs-staging` as source:

```bash
DOCS_API_SOURCE_DIR=/workspaces/docs-staging npm run docs-mcp:serve
```

### Start with HTTP transport

```bash
DOCS_MCP_TRANSPORT=http \
DOCS_MCP_HTTP_HOST=0.0.0.0 \
DOCS_MCP_HTTP_PORT=3100 \
DOCS_MCP_AUTH_TOKEN=<your-token> \
DOCS_MCP_SOURCE_MAP='{"staging":"/workspaces/docs-staging","prod":"/workspaces/docs"}' \
npm run docs-mcp:serve:http
```

Endpoints:

- MCP endpoint: `POST /mcp`
- Health check: `GET /healthz`

## Authentication

If `DOCS_MCP_AUTH_TOKEN` is set, all MCP HTTP calls must include:

```http
Authorization: Bearer <your-token>
```

## Source isolation

Use `DOCS_MCP_SOURCE_MAP` to map source keys to directories:

```bash
DOCS_MCP_SOURCE_MAP='{"staging":"/workspaces/docs-staging","prod":"/workspaces/docs"}'
```

Then select source per request:

```http
x-docs-source: staging
```

## Supported tools

### Read-only tools

- `search_docs`
- `get_doc_content`
- `list_topics`
- `list_features`

### Admin tool

- `reload_docs_index`

## Supported resources

- `docs://schema`
- `docs://index/meta`
- `docs://doc/<encoded-doc-path>`

Example:

- `docs://doc/tidb-cloud%2Fbackup-and-restore-serverless.md`

## Client configuration examples

### Claude Code (`.mcp.json`, STDIO)

```json
{
  "mcpServers": {
    "tidb-docs": {
      "command": "node",
      "args": ["scripts/docs-mcp-server.js"],
      "env": {
        "DOCS_API_SOURCE_DIR": "/workspaces/docs-staging"
      }
    }
  }
}
```

### Generic MCP HTTP client

Use your MCP client's HTTP transport option with:

- URL: `https://docs-api-staging.pingcap.com/mcp` (or your own endpoint)
- Header: `Authorization: Bearer <token>`
- Header (optional): `x-docs-source: staging`

## HTTP JSON-RPC example

```bash
curl -X POST "http://127.0.0.1:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <your-token>" \
  -H "x-docs-source: staging" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/call",
    "params":{
      "name":"search_docs",
      "arguments":{"feature":"tidb_max_dist_task_nodes","limit":3}
    }
  }'
```

## Validate your deployment

### 1. Health check

```bash
curl http://<host>:3100/healthz
```

Expected:

- `{"ok":true}`

### 2. Check available tools

```bash
curl -s -X POST "http://<host>:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <your-token>" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Expected tools:

- `search_docs`
- `get_doc_content`
- `list_topics`
- `list_features`
- `reload_docs_index`

### 3. Verify staging source and placeholder replacement

```bash
curl -s -X POST "http://<host>:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <your-token>" \
  -H "x-docs-source: staging" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_docs","arguments":{"path":"tidb-cloud/backup-and-restore-serverless.md","limit":1}}}'
```

Check:

- `meta.sourceKey` is `staging`
- Returned title/content does not include unresolved placeholders like `{{{ .starter }}}`

## Troubleshooting

- **401 Unauthorized**
  - Verify `Authorization: Bearer <token>` and `DOCS_MCP_AUTH_TOKEN`.
- **Wrong docs source**
  - Verify `x-docs-source` and `DOCS_MCP_SOURCE_MAP`.
- **No results for expected queries**
  - Run `reload_docs_index` after docs updates.
- **Cannot connect**
  - Check host/port and network access to `/mcp`.

## Design notes

- `search_docs` is optimized for lightweight response by default.
- Use `get_doc_content` when full markdown is required.
- Template variables (for example, `{{{ .starter }}}`) are resolved via `variables.json` in the selected source directory.

