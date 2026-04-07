---
title: TiDB Docs MCP Server
summary: Connect AI clients to TiDB documentation through an MCP server with version routing, layered tools, and citation-aware answers.
---

# TiDB Docs MCP Server

TiDB Docs MCP Server exposes TiDB documentation to MCP-compatible AI clients such as Claude Code, Claude Desktop, VS Code, Cursor, and other tools.

It supports:

- **STDIO transport** for local development
- **HTTP transport** for shared environments (for example, staging)
- **Bearer token authentication**
- **Source isolation** (for example, `staging` vs `prod`)
- **Version routing** (default to latest LTS stable docs)

## What you get

The server provides structured tools and resources for docs access:

- Search and retrieve docs by intent (search, page, procedure, reference, concept)
- Enforce version-aware retrieval
- Return per-answer source citation for trust and traceability
- Reload index after docs updates

## Version routing (required)

Each tool call accepts:

- `version` (optional)

Routing behavior:

- If `version` is provided, the server routes to that documentation version.
- If `version` is omitted, the server routes to the **latest LTS stable** version by default.
- The resolved version must be returned in each result payload.

This behavior is mandatory to avoid mixing content across documentation versions.

## Chunk metadata

Each indexed and returned chunk must include:

- `version`
- `category` (`tuning` | `deploy` | `reference`)
- `doc_type` (`concept` | `task` | `reference`)

Example:

```json
{
  "chunk_id": "tidb-v8.5:/tuning/sql-performance.md#chunk-03",
  "version": "v8.5",
  "category": "tuning",
  "doc_type": "task",
  "source": "/tuning/sql-performance.md",
  "content": "..."
}
```

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

## Tool layering (required)

Expose at least these tools:

| Tool | Purpose |
| --- | --- |
| `search_docs` | Fuzzy retrieval by keyword, topic, or intent |
| `get_doc_page` | Fetch one exact document by path |
| `get_procedure` | Extract ordered steps from task-style docs |
| `get_reference` | Return parameter, variable, option, or field reference entries |
| `explain_concept` | Return concept-focused explanations from concept docs |

`reload_docs_index` remains an admin tool.

## Supported tools

### Read-only tools

- `search_docs`
- `get_doc_page`
- `get_procedure`
- `get_reference`
- `explain_concept`

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

## HTTP JSON-RPC examples

Search example:

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
      "arguments":{
        "query":"tidb_max_dist_task_nodes",
        "version":"v8.5",
        "limit":3
      }
    }
  }'
```

Exact page example:

```bash
curl -X POST "http://127.0.0.1:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <your-token>" \
  -d '{
    "jsonrpc":"2.0",
    "id":2,
    "method":"tools/call",
    "params":{
      "name":"get_doc_page",
      "arguments":{
        "path":"/tuning/sql-performance.md",
        "version":"v8.5"
      }
    }
  }'
```

## Answer constraint template (required)

Use this template in your MCP client system prompt:

```text
You are a TiDB docs assistant.
Only answer using the provided MCP context.
Do not use prior knowledge.
If the answer is not found in context, reply exactly: "not documented".
Always include a source citation for each key statement.
```

## Citation output (strongly recommended)

Each answer payload should include `source` for traceability:

```json
{
  "answer": "Set this variable to ...",
  "version": "v8.5",
  "citations": [
    {
      "source": "/tuning/sql-performance.md",
      "section": "Tune SQL execution performance"
    }
  ]
}
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
- `get_doc_page`
- `get_procedure`
- `get_reference`
- `explain_concept`
- `reload_docs_index`

### 3. Verify staging source and metadata

```bash
curl -s -X POST "http://<host>:3100/mcp" \
  -H "content-type: application/json" \
  -H "authorization: Bearer <your-token>" \
  -H "x-docs-source: staging" \
  -d '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"search_docs","arguments":{"query":"backup and restore serverless","version":"v8.5","limit":1}}}'
```

Check:

- `meta.sourceKey` is `staging`
- Returned chunk metadata includes `version`, `category`, and `doc_type`
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
- Use `get_doc_page` when full markdown is required.
- Enforce version routing on every query. If `version` is missing, resolve to latest LTS stable.
- Include `source` in outputs to improve answer trust.
- Template variables (for example, `{{{ .starter }}}`) are resolved via `variables.json` in the selected source directory.
