---
title: Get started with Visual Studio Code and TiDB MCP Server
summary: This guide shows you how to configure the TiDB MCP Server in Visual Studio Code.
---

# Get Started with Visual Studio Code and TiDB MCP Server

This guide shows how to configure the TiDB MCP Server in Visual Studio Code (VS Code).

## Prerequisites

Before you begin, ensure you have the following:

- **Visual Studio Code**: Download and install VS Code from [code.visualstudio.com](https://code.visualstudio.com).
- **Python (>=3.10) and uv**: Ensure Python (3.10 or later) and `uv` are installed. Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).

## Connect to TiDB Cloud Starter (recommended)

Use the TiDB Cloud console to generate a VS Code configuration.

1. Go to the [Clusters](https://tidbcloud.com/console/clusters) page, select your cluster, and then click **Use with AI Tools** in the upper-right corner.
2. In the **Access `your_cluster_name` with AI tools** dialog, select the **Branch** and **Database** that VS Code should access.
3. Review the **Prerequisites** list in the dialog and install any missing dependencies.
4. Configure the root password:

   - If you have not set a password yet, click **Generate Password** and store it in a secure location (it is shown only once).
   - If a password already exists, enter it in the **Enter the password for easy setup** field.
   - If you forget the password, click **Reset password** in the **Prerequisites** section to generate a new one.

5. Select the **VS Code** tab, click **Add to VS Code**, and then click **Install** in VS Code.

## Manual configuration (any TiDB cluster)

If you prefer manual setup, add the following configuration to your `.vscode/mcp.json` file and replace the placeholders with your connection parameters:

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

## See also

- [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md)
