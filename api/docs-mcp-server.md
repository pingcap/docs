---
title: Docs MCP Server (Experimental)
summary: Expose TiDB docs as MCP tools and resources for AI clients such as Claude Code and Cursor.
---

# Docs MCP Server (Experimental)

This server exposes TiDB docs through MCP over STDIO.

## Start server

```bash
npm run docs-mcp:serve
```

Optional source override:

```bash
DOCS_API_SOURCE_DIR=/workspaces/docs-staging npm run docs-mcp:serve
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

## Design notes

- `search_docs` does full-text filtering but returns lightweight metadata by default.
- `get_doc_content` fetches full markdown only when needed.
- Template variables like `{{{ .starter }}}` are replaced using `variables.json` from source.

