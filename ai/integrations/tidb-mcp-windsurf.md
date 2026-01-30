---
title: Get started with Windsurf and TiDB MCP Server
summary: This guide shows you how to configure the TiDB MCP Server in Windsurf.
---

# Get Started with Windsurf and TiDB MCP Server

This guide shows you how to configure the TiDB MCP Server in Windsurf.

## Prerequisites

Before you begin, ensure you have the following:

- **Windsurf**: Download and install Windsurf from [windsurf.com](https://windsurf.com).
- **Python (>=3.10) and uv**: Ensure Python (version 3.10 or later) and uv are installed. Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install uv.
- **A TiDB cluster**: For a managed option, create a TiDB Cloud Starter cluster at [tidbcloud.com](https://tidbcloud.com/free-trial).

## Connect to TiDB Cloud Starter (recommended)

Use the TiDB Cloud console to gather the connection details, then update Windsurf's MCP configuration.

1. Go to the [Clusters](https://tidbcloud.com/console/clusters) page, select your cluster, and then click **Use with AI Tools** in the upper-right corner.
2. In the **Access `your_cluster_name` with AI tools** dialog, select the **Branch** and **Database** that Windsurf should access.
3. Review the **Prerequisites** list in the dialog and install any missing dependencies.
4. Configure the root password:

   - If you have not set a password yet, click **Generate Password** and store it in a secure location (it is shown only once).
   - If a password already exists, enter it in the **Enter the password for easy setup** field.
   - If you forget the password, click **Reset password** in the **Prerequisites** section to generate a new one.

5. Select the **Windsurf** tab and copy the provided connection values.
6. Update your `mcp_config.json` file using the copied values. For more information, see the [Windsurf MCP documentation](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin).

## Manual configuration (any TiDB cluster)

If you prefer manual setup, update your `mcp_config.json` file as follows and replace the placeholders with your connection parameters:

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

- [TiDB MCP Server](/ai/integrations/tidb-mcp-server.md)
