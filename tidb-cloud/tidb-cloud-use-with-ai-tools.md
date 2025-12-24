---
title: Use {{{ .starter }}} with AI tools
summary: Learn how to use your {{{ .starter }}} cluster with AI tools.
---

# Use {{{ .starter }}} with AI tools

This document describes how to use your {{{ .starter }}} cluster with AI tools.

## Steps

After your {{{ .starter }}} cluster is created on TiDB Cloud, you can use it with AI tools via the following steps:

1. On the [**Clusters**](https://tidbcloud.com/project/clusters) page, click a cluster name to go to its overview page, and then click **Use with AI Tools** at the top of the page.
2. In the **Access `your_cluster_name` with AI tools** dialog, select the **Branch** and **Database** that you want to connect to in the AI tool.
3. Ensure that you meet the **Prerequisites**. If not, follow the instructions on the page to install the required dependencies.
4. For the password:

    1. If you have not set a password yet, click **Generate Password** to generate a random password. The generated password will not be shown again, so save your password in a secure location.
    2. If you have already set a password:
        1. You can enter your password in the **Enter the password for easy setup** input box.
        2. If you forget your password, clicking **Reset password** in the **Prerequisites** section to get a new password. Be aware that resetting the password will drop root's connection to the current cluster.

5. Switch to the tab you want: **Cursor**, **Claude Code**, **VS Code**, or **Windsurf**.
6. Follow the tool-specific setup steps in the selected tab.

## Tool-specific setup

### Cursor

1. Click **Add to Cursor** to open Cursor, and then click **Install** to finish the setup.
2. Or add the configuration to `.cursor/mcp.json`, as follows:

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

1. Click the first copy button to copy the command.
2. Open the terminal and add the MCP server by running the copied command, as follows:

    ```bash
    claude mcp add --transport stdio TiDB \
      --env TIDB_HOST='<YOUR_TIDB_HOST>' \
      --env TIDB_PORT=<YOUR_TIDB_PORT> \
      --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
      --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
      --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
      -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
    ```

3. Alternatively, follow [Claude Code's documentation](https://code.claude.com/docs/en/mcp#project-scope) to add the configuration to `.mcp.json` for project scope, as follows:

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

1. Click **Add to VS Code** to open VS Code, and then click **Install** to finish the setup.
2. Or add the configuration to `.vscode/mcp.json`, as follows:

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

Follow [Windsurf's documentation](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin) to add the configuration to `mcp_config.json`, as follows:

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

- [Try Out TiDB + Vector](/vector-search/vector-search-get-started-using-python.md)
