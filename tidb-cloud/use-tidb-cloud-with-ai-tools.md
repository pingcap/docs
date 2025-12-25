---
title: Use {{{ .starter }}} with AI Tools
summary: Learn how to connect your {{{ .starter }}} cluster to AI-powered development tools that support the Model Context Protocol (MCP), such as Cursor, Claude Code, VS Code, and Windsurf.
---

# Use {{{ .starter }}} with AI Tools

This document describes how to connect your {{{ .starter }}} cluster to AI-powered development tools that support the Model Context Protocol (MCP), such as Cursor, Claude Code, Visual Studio Code (VS Code), and Windsurf.

By configuring your {{{ .starter }}} cluster as an MCP server, you can enable AI assistants in your development tools to query your database schema, understand your data model, and generate context-aware code suggestions.

## Before you begin

To complete this guide, you need the following:

- A {{{ .starter }}} cluster. If you don't have any, you can [create a {{{ .starter }}} cluster](/develop/dev-guide-build-cluster-in-cloud.md).
- [Python 3.11 or higher](https://www.python.org/downloads/) installed.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.
- An AI development tool that supports MCP, such as:

    - [Cursor](https://cursor.com)
    - [Claude Code](https://claude.com/product/claude-code)
    - [Visual Studio Code](https://code.visualstudio.com)
    - [Windsurf](https://windsurf.com)

## Connect to AI tools

After you create a {{{ .starter }}} cluster in TiDB Cloud, perform the following steps to connect it to your AI tool.

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page, click the name of your target cluster to go to its overview page. Then, click **Use with AI Tools** in the upper-right corner.
2. In the **Access `your_cluster_name` with AI tools** dialog, select the **Branch** and **Database** that you want the AI tool to access.
3. Verify that you meet all the **Prerequisites** listed. If not, follow the on-screen instructions to install the required dependencies.
4. Configure the password:

    - If you have not set a password yet, click **Generate Password** to generate a random password.

        The generated password will not show again, so save your password in a secure location.

    - If you have already set a password, enter your password in the **Enter the password for easy setup** field.
    - If you forget the password, click **Reset password** in the **Prerequisites** section to generate a new one.

        Note that resetting your password disconnects all existing root user sessions.

5. Select the tab for your AI tool: **Cursor**, **Claude Code**, **VS Code**, or **Windsurf**.
6. Complete the setup steps for the selected tool.

    For more information, see [Tool-specific setup](#tool-specific-setup).

## Tool-specific setup

### Cursor

To configure Cursor as an MCP client for TiDB, you can use one of the following methods:

- **Method 1**: in the **Access `your_cluster_name` with AI tools** dialog of the [TiDB Cloud console](https://tidbcloud.com), click **Add to Cursor** to launch Cursor, and then click **Install**.
- **Method 2**: manually add the following configuration to your `.cursor/mcp.json` file:

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "command": "uvx --from pytidb[mcp] tidb-mcp-server",
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Claude Code

To configure Claude Code as an MCP client for TiDB, you can use one of the following methods:

- **Method 1**: copy the setup command from the **Access `your_cluster_name` with AI tools** dialog of the [TiDB Cloud console](https://tidbcloud.com/), and then run it in your terminal:

    ```bash
    claude mcp add --transport stdio TiDB \
      --env TIDB_HOST='<YOUR_TIDB_HOST>' \
      --env TIDB_PORT=<YOUR_TIDB_PORT> \
      --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
      --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
      --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
      -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
    ```

- **Method 2**: add the following configuration to your project-level `.mcp.json` file. For more information, see the [Claude Code documentation](https://code.claude.com/docs/en/mcp#project-scope).

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### VS Code

To configure VS Code as an MCP client for TiDB, you can use one of the following methods:

- **Method 1**: in the **Access `your_cluster_name` with AI tools** dialog of the [TiDB Cloud console](https://tidbcloud.com/), click **Add to VS Code** to launch VS Code, and then click **Install**.
- **Method 2**: add the following configuration to your `.vscode/mcp.json` file:

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Windsurf

To add the TiDB MCP plugin to Windsurf, update your `mcp_config.json` file as follows. For more information, see the [Windsurf documentation](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin).

```json
{
  "mcpServers": {
    "TiDB": {
      "command": "uvx",
      "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
      "env": {
        "TIDB_HOST": "<YOUR_TIDB_HOST>",
        "TIDB_PORT": "<YOUR_TIDB_PORT>",
        "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
        "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
        "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
      }
    }
  }
}
```

## See also

- [Try Out TiDB + Vector Search](/vector-search/vector-search-get-started-using-python.md)
- [Developer Guide Overview](/develop/dev-guide-overview.md)
