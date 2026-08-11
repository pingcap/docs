---
title: TiDB Cloud Lake MCP Server
summary: Learn how to install, run, and configure the TiDB Cloud Lake MCP server, including transports, safety controls, and available tools.
---

# TiDB Cloud Lake MCP Server

The [TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) exposes {{{ .lake }}} operations to clients that support the Model Context Protocol (MCP). The `tidbcloudlake-mcp` package supports standard input/output, HTTP, and server-sent events (SSE) transports.

## Prerequisites

Before you begin, make sure that you have the following:

- Python 3.12 or later
- A {{{ .lake }}} account, database, and warehouse
- A {{{ .lake }}} DSN in the following format:

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

For information about obtaining connection information, see [Connect to a Warehouse](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse).

## Install the MCP server

Create and activate a virtual environment:

```shell
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the server from PyPI:

```shell
python -m pip install tidbcloudlake-mcp
```

## Run the MCP server

Set the {{{ .lake }}} DSN:

```shell
export LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

Run the server with its default `stdio` transport:

```shell
lake-mcp
```

You can also run the package without installing it into the active environment:

```shell
uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

## Configure the transport

Set `LAKE_MCP_SERVER_TRANSPORT` to one of the following values:

| Value | Description |
| --- | --- |
| `stdio` | Communicates with a local MCP client through standard input and output. This is the default. |
| `http` | Starts an HTTP server. |
| `sse` | Starts a server that uses server-sent events. |

For example, to run an HTTP server on the default loopback address and port:

```shell
export LAKE_MCP_SERVER_TRANSPORT=http
export LAKE_MCP_BIND_HOST=127.0.0.1
export LAKE_MCP_BIND_PORT=8001
lake-mcp
```

> **Warning:**
>
> Keep the bind address restricted to a trusted network. The MCP server can access data with the permissions of the configured {{{ .lake }}} user.

## Configuration

| Environment variable | Default | Description |
| --- | --- | --- |
| `LAKE_DSN` | Required for {{{ .lake }}} | Connection string for the database and warehouse. |
| `LAKE_MCP_SAFE_MODE` | `true` | Enables session sandbox validation. |
| `LAKE_QUERY_TIMEOUT` | `300` | Query timeout in seconds. |
| `LAKE_MCP_SERVER_TRANSPORT` | `stdio` | Server transport: `stdio`, `http`, or `sse`. |
| `LAKE_MCP_BIND_HOST` | `127.0.0.1` | Bind address for the `http` and `sse` transports. |
| `LAKE_MCP_BIND_PORT` | `8001` | Bind port for the `http` and `sse` transports. |

## Available tools

| Tool | Description |
| --- | --- |
| `execute_sql` | Executes SQL with sandbox validation. |
| `execute_multi_sql` | Executes multiple SQL statements. |
| `show_databases` | Lists databases. |
| `show_tables` | Lists tables in a database. |
| `describe_table` | Returns the schema of a table. |
| `get_session_sandbox_prefix` | Returns the sandbox prefix for the current session. |
| `list_session_sandbox_databases` | Lists sandbox databases for the current session. |
| `create_session_sandbox_database` | Creates a sandbox database for the current session. |
| `show_stages` | Lists stages. |
| `list_stage_files` | Lists files in a stage. |
| `create_stage` | Creates a stage, subject to sandbox validation. |
| `show_connections` | Lists connections. |

## Safe mode

Safe mode is enabled by default. In safe mode:

- Read operations such as `SELECT`, `SHOW`, `DESCRIBE`, `EXPLAIN`, and `LIST` can access objects allowed by the configured {{{ .lake }}} user.
- Write operations are limited to objects whose names start with the current `mcp_sandbox_{session_id}_*` prefix.
- Data manipulation statements can modify only sandbox tables.
- Privilege changes can target only sandbox objects and principals.

Set `LAKE_MCP_SAFE_MODE=false` only when the MCP client is trusted and the configured {{{ .lake }}} user has the minimum required privileges.

For client-specific configuration examples, see [Connect AI Tools to TiDB Cloud Lake Using MCP](/tidb-cloud-lake/guides/mcp-client-integration.md).

## Related resources

- [`tidbcloudlake-mcp` on PyPI](https://pypi.org/project/tidbcloudlake-mcp/)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
