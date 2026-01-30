---
title: Get started with Claude Desktop and TiDB MCP Server
summary: This guide shows you how to configure the TiDB MCP Server in Claude Desktop.
---

# Integrate TiDB MCP Server with Claude Desktop

This guide shows you how to configure the TiDB MCP Server in Claude Desktop.

## Prerequisites

Before you begin, ensure you have the following:

- **Claude Desktop**: Download and install Claude Desktop from [claude.ai](https://claude.ai/download).
- **Python (>=3.10) and uv**: Ensure Python (version 3.10 or later) and uv is installed. Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install uv.
- **A TiDB Cloud Starter Cluster**: You can create a free TiDB cluster here [tidbcloud.com](https://tidbcloud.com/free-trial).

## Setup steps

You can follow the steps below to set up the TiDB MCP Server in Claude Desktop:

1. Open the **Settings** dialog.
2. Click the **Developers** tab in the dialog.
3. Click the **Edit Config** button to open the MCP config file `claude_desktop_config.json`.
4. Copy the following configuration into the `claude_desktop_config.json` file.

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "command": "uvx --from pytidb[mcp] tidb-mcp-server",
          "env": {
            "TIDB_HOST": "localhost",
            "TIDB_PORT": "4000",
            "TIDB_USERNAME": "root",
            "TIDB_PASSWORD": "",
            "TIDB_DATABASE": "test"
          }
        }
      }
    }
    ```

5. Go to the [TiDB Cloud cluster page](https://tidbcloud.com/console/clusters) and navigate to the cluster you want to connect to.
6. Click the **Connect** button to get the connection parameters, and replace the `TIDB_HOST`, `TIDB_PORT`, `TIDB_USERNAME`, `TIDB_PASSWORD`, and `TIDB_DATABASE` values with your own.
7. Restart Claude Desktop.

For more details, see [how to configure the MCP server in Claude Desktop](https://modelcontextprotocol.io/quickstart/user).