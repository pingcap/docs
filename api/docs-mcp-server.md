---
title: Docs MCP Server (Experimental)
summary: Expose TiDB docs as MCP tools and resources for AI clients such as Claude Code and Cursor.
---

# Docs MCP Server (Experimental)

This server exposes TiDB docs through MCP using:

- STDIO transport (local tool integration)
- HTTP transport (shared staging endpoint)

## Start server (STDIO)

```bash
npm run docs-mcp:serve
```

Optional source override:

```bash
DOCS_API_SOURCE_DIR=/workspaces/docs-staging npm run docs-mcp:serve
```

## Start server (HTTP)

```bash
DOCS_MCP_TRANSPORT=http DOCS_MCP_HTTP_HOST=0.0.0.0 DOCS_MCP_HTTP_PORT=3100 npm run docs-mcp:serve:http
```

MCP endpoint: `POST /mcp`  
Health endpoint: `GET /healthz`

## Authentication

Set bearer token:

```bash
DOCS_MCP_AUTH_TOKEN=<token>
```

Then call MCP with header:

```http
Authorization: Bearer <token>
```

## Source isolation (staging/prod)

You can map source keys to different docs directories:

```bash
DOCS_MCP_SOURCE_MAP='{"staging":"/workspaces/docs-staging","prod":"/workspaces/docs"}'
```

Clients can select source via header:

```http
x-docs-source: staging
```

## MCP tools

- `search_docs`
- `get_doc_content`
- `list_topics`
- `list_features`
- `reload_docs_index`

## MCP resources

- `docs://schema`
- `docs://index/meta`
- `docs://doc/<encoded path>`

Example:

- `docs://doc/tidb-cloud%2Fbackup-and-restore-serverless.md`

## Claude Code example (`.mcp.json`)

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

## HTTP JSON-RPC example

```bash
curl -X POST "http://127.0.0.1:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <token>" \
  -H "x-docs-source: staging" \
  -d '{
    "jsonrpc":"2.0",
    "id":1,
    "method":"tools/call",
    "params":{"name":"search_docs","arguments":{"feature":"tidb_max_dist_task_nodes","limit":3}}
  }'
```

## Validation and Testing

Use this section to validate your deployment locally and with remote teammates.

### 1) Start service for shared testing

```bash
DOCS_MCP_TRANSPORT=http \
DOCS_MCP_HTTP_HOST=0.0.0.0 \
DOCS_MCP_HTTP_PORT=3100 \
DOCS_MCP_AUTH_TOKEN=<your-token> \
DOCS_MCP_SOURCE_MAP='{"staging":"/workspaces/docs-staging","prod":"/workspaces/docs"}' \
npm run docs-mcp:serve:http
```

Health check:

```bash
curl http://<host>:3100/healthz
```

### 2) Core validation commands

Set variables:

```bash
BASE=http://<host>:3100/mcp
TOKEN=<your-token>
```

List tools:

```bash
curl -s -X POST "$BASE" \
  -H "content-type: application/json" \
  -H "authorization: Bearer $TOKEN" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
```

Search by feature from staging source:

```bash
curl -s -X POST "$BASE" \
  -H "content-type: application/json" \
  -H "authorization: Bearer $TOKEN" \
  -H "x-docs-source: staging" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"search_docs","arguments":{"feature":"tidb_max_dist_task_nodes","limit":3}}}'
```

Fetch full content of one doc:

```bash
curl -s -X POST "$BASE" \
  -H "content-type: application/json" \
  -H "authorization: Bearer $TOKEN" \
  -H "x-docs-source: staging" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"get_doc_content","arguments":{"path":"tidb-cloud/backup-and-restore-serverless.md"}}}'
```

Reload docs index:

```bash
curl -s -X POST "$BASE" \
  -H "content-type: application/json" \
  -H "authorization: Bearer $TOKEN" \
  -H "x-docs-source: staging" \
  -d '{"jsonrpc":"2.0","id":4,"method":"tools/call","params":{"name":"reload_docs_index","arguments":{}}}'
```

### 3) Expected results checklist

- `/healthz` returns `{ "ok": true }`.
- `tools/list` includes:
  - `search_docs`
  - `get_doc_content`
  - `list_topics`
  - `list_features`
  - `reload_docs_index`
- `search_docs` response includes `meta.sourceKey` and `meta.sourceDir`.
- `x-docs-source: staging` points to your `docs-staging` path.
- No unresolved placeholders like `{{{ .starter }}}` in returned titles/content.
- `search_docs` returns lightweight records by default.
- `get_doc_content` returns full markdown content.

### 4) Remote teammate test template

Ask teammates to report:

1. Environment: OS + time + endpoint tested.
2. Commands used (copy/paste).
3. Result summary:
   - status code
   - `meta.total`
   - `meta.sourceKey`
4. Pass/fail verdict.
5. If failed: error payload + reproduction steps.

## Design notes

- `search_docs` does full-text filtering but returns lightweight metadata by default.
- `get_doc_content` fetches full markdown only when needed.
- Template variables like `{{{ .starter }}}` are replaced using `variables.json` from source.
