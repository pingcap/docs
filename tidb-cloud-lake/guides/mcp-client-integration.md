---
title: MCP Client Integration
summary: Databend MCP connects AI assistants to Databend via Model Context Protocol. Works with Claude Code, Codex, Cursor, Claude Desktop, VS Code, and other MCP-compatible clients.
---

# MCP Client Integration

## Overview

[Databend MCP](https://github.com/databendlabs/mcp-databend) connects AI assistants to Databend via Model Context Protocol. Works with Claude Code, Codex, Cursor, Claude Desktop, VS Code, and other MCP-compatible clients.

**What you can do:**

- Generate complex SQL queries based on your requirements
- Create and manage scheduled data pipeline tasks
- Explore database schemas and validate query syntax
- Build ETL workflows with COPY, MERGE, and Stage operations

For example: _"Create a scheduled task that copies parquet files from @my_stage to the orders table every minute, and verify it's running correctly."_

## Installation

### 1. Get Databend Connection

We recommend using **Databend Cloud** for the best experience.

1.  Log in to [Databend Cloud](https://app.databend.com).
2.  Click **Use with AI Tools** in the navigation bar.
3.  Select regular connection information (Host, User, Password, etc.).
4.  Copy your DSN, which looks like:
    `databend://user:pwd@host:443/database?warehouse=warehouse_name`

![Use with AI Tools](/media/tidb-cloud-lake/ai-tools.png)

### 2. Configure Your MCP Client

<SimpleTab groupId="mcp-clients">

<div label="Codex" value="codex">

```bash
codex mcp add databend \
  --env DATABEND_DSN='databend://user:password@host:port/database?warehouse=your_warehouse' \
  --env SAFE_MODE='false' \
  -- uv tool run mcp-databend
```

Or add to `~/.codex/config.toml`:

```toml
[mcp_servers.databend]
command = "uv"
args = ["tool", "run", "mcp-databend"]

[mcp_servers.databend.env]
DATABEND_DSN = "databend://user:password@host:port/database?warehouse=your_warehouse"
SAFE_MODE = "false"
```

</div>

<div label="Claude Code" value="claude-code">

```bash
claude mcp add databend \
  --env DATABEND_DSN='databend://user:password@host:port/database?warehouse=your_warehouse' \
  --env SAFE_MODE='false' \
  -- uv tool run mcp-databend
```

</div>

<div label="Gemini CLI" value="gemini-cli">

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "databend://user:password@host:port/database?warehouse=your_warehouse",
        "SAFE_MODE": "false"
      }
    }
  }
}
```

</div>

<div label="Cursor" value="cursor">

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "databend://user:password@host:port/database?warehouse=your_warehouse",
        "SAFE_MODE": "false"
      }
    }
  }
}
```

</div>

<div label="Claude Desktop" value="claude-desktop">

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "databend://user:password@host:port/database?warehouse=your_warehouse",
        "SAFE_MODE": "false"
      }
    }
  }
}
```

</div>

<div label="VS Code" value="vscode">

Add to `.vscode/mcp.json`:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "databend://user:password@host:port/database?warehouse=your_warehouse",
        "SAFE_MODE": "false"
      }
    }
  }
}
```

</div>

<div label="Manual" value="manual">

```bash
export DATABEND_DSN="databend://user:password@host:port/database?warehouse=your_warehouse"
export SAFE_MODE="false"

uv tool run mcp-databend
```

</div>
</SimpleTab>

## Available Tools

### Database Operations

| Tool             | Description                                      |
| ---------------- | ------------------------------------------------ |
| `execute_sql`    | Execute SQL queries with timeout protection      |
| `show_databases` | List all databases                               |
| `show_tables`    | List tables in a database (with optional filter) |
| `describe_table` | Get table schema information                     |

### Stage Management

| Tool               | Description                                |
| ------------------ | ------------------------------------------ |
| `show_stages`      | List all available stages                  |
| `list_stage_files` | List files in a specific stage             |
| `create_stage`     | Create a new stage with connection support |

### Connection Management

| Tool               | Description                    |
| ------------------ | ------------------------------ |
| `show_connections` | List all available connections |

## Configuration

| Variable                 | Description                                             | Default  |
| ------------------------ | ------------------------------------------------------- | -------- |
| `DATABEND_DSN`           | Connection string                                       | Required |
| `SAFE_MODE`              | Block dangerous SQL operations (`DROP`, `DELETE`, etc.) | `true`   |
| `DATABEND_QUERY_TIMEOUT` | Query timeout in seconds                                | `300`    |

For more details on building conversational BI tools, see [MCP Server Guide](/tidb-cloud-lake/guides/mcp-server.md).
