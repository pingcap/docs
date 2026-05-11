---
title: MCP Client Integration
summary: "{{{ .lake }}} MCP connects AI assistants to {{{ .lake }}} via Model Context Protocol. Works with Claude Code, Codex, Cursor, Claude Desktop, VS Code, and other MCP-compatible clients."
---

# MCP Client Integration

[{{{ .lake }}} MCP](https://github.com/databendlabs/mcp-databend) connects AI assistants to {{{ .lake }}} through the Model Context Protocol. It works with Codex, Kimi Code, Cursor, Claude Code, Claude Desktop, Gemini CLI, VS Code, and other MCP-compatible clients.

**What you can do:**

- Generate complex SQL queries from natural language requirements.
- Explore databases, tables, schemas, stages, and connections.
- Validate query syntax before running it.
- Build ETL workflows with COPY, MERGE, and Stage operations.
- Create and manage scheduled data pipeline tasks.

For example: "Create a scheduled task that copies parquet files from @my_stage to the orders table every minute, and verify that it is running correctly."

## Installation

### 1. Get a {{{ .lake }}} Connection

We recommend using **{{{ .lake }}}** for the best experience. You can obtain the DSN in two ways.

#### Option A: Use **Use with AI Tools** (recommended)

Generates a short-lived DSN with session sandbox safety in one click. Best for getting AI tools connected quickly.

1. Log in to [{{{ .lake }}}](https://app.lake.tidbcloud.com).
2. Click **Use with AI Tools**.
3. Choose the database and warehouse for the MCP server.
4. Keep **Session Sandbox Safety** enabled unless you explicitly need the agent to write to production objects.
5. Copy the DSN, which looks like `lake://user:password@host:443/database?warehouse=warehouse_name`.

![Use with AI Tools](/media/tidb-cloud-lake/ai-tools.png)

#### Option B: Build the DSN with your own SQL user

Use this when you want a stable account and permission set (for example, CI pipelines, sharing with teammates, or pairing with a least-privilege policy).

1. Create a SQL user in {{{ .lake }}} and grant the required privileges. See [CREATE USER](/tidb-cloud-lake/sql/create-user.md#example-1-full-access-across-all-databases).
2. Get your `tenant`, `region`, `database`, and `warehouse` values from **Overview → Connect**.
3. Assemble the DSN using this format:

    ```text
    lake://<username>:<password>@<tenant>.gw.<region>.default.tidbcloud.com:443/<database>?warehouse=<warehouse_name>
    ```

### 2. Configure Your MCP Client

Use `DATABEND_MCP_SAFE_MODE=true` by default. In safe mode, production data remains read-only for AI agents, while write operations are scoped to session sandbox objects.

<SimpleTab groupId="mcp-clients">

<div label="Codex" value="codex">

```bash
codex mcp add databend \
  --env DATABEND_DSN='lake://user:password@host:443/database?warehouse=your_warehouse' \
  --env DATABEND_MCP_SAFE_MODE=true \
  -- uv tool run --from mcp-databend@latest mcp-databend
```

Or add to `~/.codex/config.toml`:

```toml
[mcp_servers.databend]
command = "uv"
args = ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"]

[mcp_servers.databend.env]
DATABEND_DSN = "lake://user:password@host:443/database?warehouse=your_warehouse"
DATABEND_MCP_SAFE_MODE = "true"
```

</div>

<div label="Claude Code" value="claude-code">

```bash
claude mcp add databend \
  --env DATABEND_DSN='lake://user:password@host:443/database?warehouse=your_warehouse' \
  --env DATABEND_MCP_SAFE_MODE=true \
  -- uv tool run --from mcp-databend@latest mcp-databend
```

</div>

<div label="Kimi Code" value="kimi-code">

```bash
kimi mcp add --transport stdio databend \
  --env DATABEND_DSN='lake://user:password@host:443/database?warehouse=your_warehouse' \
  --env DATABEND_MCP_SAFE_MODE=true \
  -- uv tool run --from mcp-databend@latest mcp-databend
```

Or add to `~/.kimi/mcp.json`:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "lake://user:password@host:443/database?warehouse=your_warehouse",
        "DATABEND_MCP_SAFE_MODE": "true"
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
      "args": ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "lake://user:password@host:443/database?warehouse=your_warehouse",
        "DATABEND_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Gemini CLI" value="gemini-cli">

Add to `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "lake://user:password@host:443/database?warehouse=your_warehouse",
        "DATABEND_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Claude Desktop" value="claude-desktop">

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS, or `%APPDATA%\Claude\claude_desktop_config.json` on Windows:

```json
{
  "mcpServers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "lake://user:password@host:443/database?warehouse=your_warehouse",
        "DATABEND_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="VS Code" value="vscode">

Open **Preferences: Open User Settings (JSON)** and add:

```json
{
  "mcp.servers": {
    "databend": {
      "command": "uv",
      "args": ["tool", "run", "--from", "mcp-databend@latest", "mcp-databend"],
      "env": {
        "DATABEND_DSN": "lake://user:password@host:443/database?warehouse=your_warehouse",
        "DATABEND_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Manual" value="manual">

```bash
export DATABEND_DSN="lake://user:password@host:443/database?warehouse=your_warehouse"
export DATABEND_MCP_SAFE_MODE=true

uv tool run --from mcp-databend@latest mcp-databend
```

</div>
</SimpleTab>

## Session Sandbox Safety

`DATABEND_MCP_SAFE_MODE` controls whether the MCP server runs with session sandbox protection.

| Value | Behavior | Recommended usage |
| ----- | -------- | ----------------- |
| `true` | Production objects are read-only for the agent. Write operations are allowed only on session sandbox objects such as `mcp_sandbox_{session_id}_*`. | Default and recommended for AI tools. |
| `false` | The MCP server can write to objects allowed by the {{{ .lake }}} user permissions. | Use only with trusted agents and least-privilege {{{ .lake }}} users. |

Keep safe mode enabled for most workflows. Disable it only when the agent must modify real production objects and the {{{ .lake }}} user already has the minimum required permissions.

## Available Tools

### Database Operations

| Tool             | Description                                      |
| ---------------- | ------------------------------------------------ |
| `execute_sql`    | Execute SQL queries with timeout protection      |
| `show_databases` | List all databases                               |
| `show_tables`    | List tables in a database with optional filter   |
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

| Variable                 | Description                                    | Default  |
| ------------------------ | ---------------------------------------------- | -------- |
| `DATABEND_DSN`           | {{{ .lake }}} connection string                | Required |
| `DATABEND_MCP_SAFE_MODE` | Enable session sandbox protection for AI tools | `true`   |
| `DATABEND_QUERY_TIMEOUT` | Query timeout in seconds                       | `300`    |

For more details on building conversational BI tools, see [MCP Server Guide](/tidb-cloud-lake/guides/mcp-server.md).
