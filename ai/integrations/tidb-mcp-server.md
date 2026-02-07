---
title: TiDB MCP Server
summary: Manage your TiDB databases using natural language instructions with the TiDB MCP Server.
---

# TiDB MCP Server

TiDB MCP Server is an open-source tool that lets you interact with TiDB databases using natural language instructions.

## Understanding MCP and TiDB MCP Server

The [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction) is a protocol that standardizes communication between LLMs and external tools.

MCP adopts a client-server architecture, allowing a host application to connect to multiple external servers:

- **Hosts**: AI-powered applications, such as Claude Desktop or IDEs like Cursor, that initiate connections to MCP servers.

- **Clients**: Components embedded within host applications that establish one-to-one connections with individual MCP servers.

- **Servers**: External services, such as the **TiDB MCP Server**, which provide tools, context, and prompts to clients for interacting with external systems.

The **TiDB MCP Server** is an MCP-compatible server that provides tools and context for MCP clients to interact with TiDB databases.

## Prerequisites

Before you begin, ensure you have the following:

- **An MCP-compatible client**: For example, [Cursor](/ai/integrations/tidb-mcp-cursor.md) or [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md).
- **Python (>=3.10) and uv**: Ensure Python (3.10 or later) and `uv` are installed. Follow the [installation guide](https://docs.astral.sh/uv/getting-started/installation/) to install `uv`.
- **A TiDB Cloud Starter cluster**: You can create a free TiDB cluster on [TiDB Cloud](https://tidbcloud.com/free-trial).

## Supported MCP Clients

Refer to the following guides for detailed examples of using the TiDB MCP Server with specific MCP clients:

- [Cursor](/ai/integrations/tidb-mcp-cursor.md)
- [Claude Desktop](/ai/integrations/tidb-mcp-claude-desktop.md)

If the preceding list does not include your MCP client, follow the setup steps below.

## Setup steps

The TiDB MCP Server supports two modes to integrate with MCP clients:

- Standard Input/Output (STDIO) mode (default)
- Server-Sent Events (SSE) mode

TiDB MCP Server uses STDIO mode by default, so you do not need to start a standalone server in advance.

You can choose one of the modes to set up the TiDB MCP Server in your MCP client.

### STDIO Mode

To set up the TiDB MCP Server in your MCP client using STDIO mode, take the following steps:

1. Refer to your MCP client documentation to learn how to configure your MCP server.

2. Go to your [TiDB Cloud clusters](https://tidbcloud.com/console/clusters) page and navigate to the overview page of your cluster.

3. Click **Connect** on the cluster overview page to get the connection parameters.

4. Configure the TiDB MCP Server with your connection parameters in the `mcpServers` section of your AI application’s configuration file.

      Example MCP configuration file:

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

### Server-Sent Events (SSE) Mode

To set up the TiDB MCP Server in your MCP client using SSE mode, take the following steps:

1. Refer to your MCP client documentation to learn how to configure an MCP server.

2. Go to your [TiDB Cloud clusters](https://tidbcloud.com/console/clusters) page and select your cluster.

3. Click **Connect** on the cluster page to get the connection parameters.

4. Create a `.env` file with your connection parameters.

    Example `.env` file:

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    EOF
    ```

5. Start the TiDB MCP Server with the `--transport sse` option:

    ```bash
    uvx --from "pytidb[mcp]" tidb-mcp-server --transport sse
    ```

6. Add the `TiDB` MCP server configuration to the `mcpServers` section of your AI application's configuration file.

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "url": "http://localhost:8000/sse"
        }
      }
    }
    ```

## Supported actions (tools)

The TiDB MCP Server provides the following actions (tools) to MCP clients. You can use them to interact with your TiDB projects and databases in natural language instructions.

**Database Management**

- `show_databases` - Show all databases in the TiDB cluster

    * `username`: Database username (string, optional)
    * `password`: Database password (string, optional)

- `switch_database` - Switch to a specific database

    * `db_name`: Database name to switch to (string, required)
    * `username`: Database username (string, optional)
    * `password`: Database password (string, optional)

- `show_tables` - Show all tables in the current database

**SQL query and execution**

- `db_query` - Execute read-only SQL queries

    * `sql_stmt`: SQL query statement (string, required)

- `db_execute` - Execute SQL statements (DML or DDL)

    * `sql_stmts`: A single SQL statement or an array of SQL statements (string or array, required)

**User Management**

- `db_create_user` - Create a new database user

    * `username`: Name for the new user (string, required)
    * `password`: Password for the new user (string, required)

- `db_remove_user` - Remove an existing database user

    * `username`: Name of the user to remove (string, required)
