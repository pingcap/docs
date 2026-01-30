---
title: Get started with Cursor and TiDB MCP Server
summary: This guide shows you how to configure the TiDB MCP Server in the Cursor editor.
---

# Get Started with Cursor and TiDB MCP Server

This guide shows you how to configure the TiDB MCP Server in the Cursor editor.

For one-click installation, you can click the following button:

[![Install TiDB MCP Server](https://cursor.com/deeplink/mcp-install-dark.svg)](cursor://anysphere.cursor-deeplink/mcp/install?name=TiDB&config=eyJjb21tYW5kIjoidXZ4IC0tZnJvbSBweXRpZGJbbWNwXSB0aWRiLW1jcC1zZXJ2ZXIiLCJlbnYiOnsiVElEQl9IT1NUIjoibG9jYWxob3N0IiwiVElEQl9QT1JUIjoiNDAwMCIsIlRJREJfVVNFUk5BTU0iOiJyb290IiwiVElEQl9QQVNTV09SRCI6IiIsIlRJREJfREFUQUJBU0UiOiJ0ZXN0In19)

## Prerequisites

Before you begin, ensure you have the following:

- **Cursor Editor**: Download and install Cursor from [cursor.com](https://cursor.com).
- **Python (>=3.10) and uv**: Ensure Python (version 3.10 or later) and uv are installed. Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install uv.
- **A TiDB cluster**: For a managed option, create a TiDB Cloud Starter cluster at [tidbcloud.com](https://tidbcloud.com/free-trial).

## Connect to TiDB Cloud Starter (recommended)

Use the TiDB Cloud console to create a Cursor configuration with your cluster credentials.

1. Go to the [Clusters](https://tidbcloud.com/console/clusters) page, select your cluster, and then click **Use with AI Tools** in the upper-right corner.
2. In the **Access `your_cluster_name` with AI tools** dialog, select the **Branch** and **Database** that Cursor should access.
3. Review the **Prerequisites** list in the dialog and install any missing dependencies.
4. Configure the root password:

   - If you have not set a password yet, click **Generate Password** and store it in a secure location (it is shown only once).
   - If a password already exists, enter it in the **Enter the password for easy setup** field.
   - If you forget the password, click **Reset password** in the **Prerequisites** section to generate a new one.

5. Select the **Cursor** tab, click **Add to Cursor**, and then click **Install** in Cursor.

## Manual configuration (any TiDB cluster)

If you prefer manual setup, add the following configuration to your `.cursor/mcp.json` file and replace the placeholders with your connection parameters:

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

For more details, see the [Model Context Protocol documentation](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers).

## Troubleshooting

If you encounter any issues installing the TiDB MCP Server, check the MCP logs in the Cursor editor.

1. Click **View** > **Output** in the main menu at the top of the editor.
2. Select **MCP** from the dropdown menu in the **Output** panel.
3. If you see errors like `[error] Could not start MCP server tidb-mcp-server: Error: spawn uvx ENOENT`, it means the `uvx` command may not exist in your `$PATH` system variable. For macOS users, you can install `uvx` by running `brew install uv`.
