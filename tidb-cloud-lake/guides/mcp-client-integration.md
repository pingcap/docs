---
title: Connect AI Tools to TiDB Cloud Lake Using MCP
summary: Learn how to connect MCP-compatible AI tools to TiDB Cloud Lake and use session sandbox protection for safe data exploration.
---

# Connect AI Tools to TiDB Cloud Lake Using MCP

The [TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) connects AI assistants to {{{ .lake }}} through the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/). With an MCP-compatible tool, you can explore database objects, inspect table schemas, and run SQL using natural-language instructions.

## Prerequisites

Before you begin, make sure that you have the following:

- Python 3.12 or later
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed
- An MCP-compatible AI tool
- A {{{ .lake }}} account, database, and warehouse

## Get a connection string

Get the host, username, password, database, and warehouse name from your {{{ .lake }}} warehouse. For more information, see [Connect to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

Build a DSN using the following format:

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

## Configure an MCP client

The following configurations run the latest `tidbcloudlake-mcp` package with `uv`. Safe mode is enabled explicitly in each example.

<SimpleTab groupId="lake-mcp-clients">

<div label="Codex" value="codex">

```shell
codex mcp add lake-mcp \
    --env LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>' \
    --env LAKE_MCP_SAFE_MODE=true \
    -- uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

</div>

<div label="Claude Code" value="claude-code">

```shell
claude mcp add lake-mcp \
    --env LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>' \
    --env LAKE_MCP_SAFE_MODE=true \
    -- uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

</div>

<div label="Cursor" value="cursor">

Add the following server to your Cursor MCP configuration:

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Gemini CLI" value="gemini-cli">

Add the following server to the `mcpServers` object in your Gemini CLI `settings.json` file:

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Other MCP Clients" value="other">

For an MCP client that accepts the standard JSON configuration, add the following server:

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

</SimpleTab>

Restart the AI tool after saving its MCP configuration. You can then ask the tool to list databases, inspect tables, or run a query.

## Session sandbox protection

`LAKE_MCP_SAFE_MODE` controls whether the server validates write operations against a session-specific sandbox.

| Value | Behavior |
| --- | --- |
| `true` | Production objects are read-only for the AI tool. Writes are limited to objects whose names start with the current `mcp_sandbox_{session_id}_*` prefix. This is the default and recommended setting. |
| `false` | The server allows any SQL operation permitted by the configured {{{ .lake }}} user. Use this setting only with a trusted tool and a least-privilege account. |

The MCP tool `get_session_sandbox_prefix` returns the prefix for the current session.

For server transports, configuration variables, and the available MCP tools, see [TiDB Cloud Lake MCP Server](/tidb-cloud-lake/guides/mcp-server.md).
