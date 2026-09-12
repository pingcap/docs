---
title: TiDB Cloud Lake MCP Server
summary: 了解如何安装、运行和配置 TiDB Cloud Lake MCP server，包括传输方式、安全控制和可用工具。
---

# TiDB Cloud Lake MCP Server

[TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) 向支持 Model Context Protocol (MCP) 的客户端暴露 {{{ .lake }}} 操作。`tidbcloudlake-mcp` 包支持标准输入/输出、HTTP 和 server-sent events (SSE) 传输方式。

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- Python 3.12 或更高版本
- 一个 {{{ .lake }}} 账户、数据库和计算集群 (Warehouse)
- 一个符合以下格式的 {{{ .lake }}} DSN：

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

有关如何获取连接信息，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

## 安装 MCP server {#install-the-mcp-server}

创建并激活虚拟环境：

```shell
python3.12 -m venv .venv
source .venv/bin/activate
```

从 PyPI 安装 server：

```shell
python -m pip install tidbcloudlake-mcp
```

## 运行 MCP server {#run-the-mcp-server}

设置 {{{ .lake }}} DSN：

```shell
export LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

使用默认的 `stdio` 传输方式运行 server：

```shell
lake-mcp
```

你也可以在不将该包安装到当前激活环境中的情况下运行它：

```shell
uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

## 配置传输方式 {#configure-the-transport}

将 `LAKE_MCP_SERVER_TRANSPORT` 设置为以下值之一：

| 值 | 描述 |
| --- | --- |
| `stdio` | 通过标准输入和输出与本地 MCP 客户端通信。这是默认值。 |
| `http` | 启动一个 HTTP 服务器。 |
| `sse` | 启动一个使用服务器发送事件的服务器。 |

例如，要在默认的 loopback 地址和端口上运行一个 HTTP server：

```shell
export LAKE_MCP_SERVER_TRANSPORT=http
export LAKE_MCP_BIND_HOST=127.0.0.1
export LAKE_MCP_BIND_PORT=8001
lake-mcp
```

> **Warning:**
>
> 请将绑定地址限制在受信任的网络内。MCP server 可以使用已配置 {{{ .lake }}} 用户的权限访问数据。

## 配置 {#configuration}

| 环境变量 | 默认值 | 描述 |
| --- | --- | --- |
| `LAKE_DSN` | {{{ .lake }}} 必需 | 数据库和计算集群的连接字符串。 |
| `LAKE_MCP_SAFE_MODE` | `true` | 启用会话沙箱校验。 |
| `LAKE_QUERY_TIMEOUT` | `300` | 查询超时时间，单位为秒。 |
| `LAKE_MCP_SERVER_TRANSPORT` | `stdio` | 服务器传输方式：`stdio`、`http` 或 `sse`。 |
| `LAKE_MCP_BIND_HOST` | `127.0.0.1` | `http` 和 `sse` 传输方式的绑定地址。 |
| `LAKE_MCP_BIND_PORT` | `8001` | `http` 和 `sse` 传输方式的绑定端口。 |

## 可用工具 {#available-tools}

| 工具 | 描述 |
| --- | --- |
| `execute_sql` | 执行带有沙箱校验的 SQL。 |
| `execute_multi_sql` | 执行多条 SQL 语句。 |
| `show_databases` | 列出数据库。 |
| `show_tables` | 列出数据库中的表。 |
| `describe_table` | 返回表的 schema。 |
| `get_session_sandbox_prefix` | 返回当前会话的沙箱前缀。 |
| `list_session_sandbox_databases` | 列出当前会话的沙箱数据库。 |
| `create_session_sandbox_database` | 为当前会话创建一个沙箱数据库。 |
| `show_stages` | 列出 stage。 |
| `list_stage_files` | 列出 stage 中的文件。 |
| `create_stage` | 创建一个 stage，并受沙箱校验约束。 |
| `show_connections` | 列出连接。 |

## 安全模式 {#safe-mode}

默认启用安全模式。在安全模式下：

- `SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN` 和 `LIST` 等读操作可以访问已配置 {{{ .lake }}} 用户被允许访问的对象。
- 写操作仅限于名称以当前 `mcp_sandbox_{session_id}_*` 前缀开头的对象。
- 数据操作语句只能修改沙箱表。
- 权限变更只能针对沙箱对象和 principals。

仅当 MCP 客户端可信，且已配置 {{{ .lake }}} 用户具有所需的最小权限时，才将 `LAKE_MCP_SAFE_MODE=false`。

有关特定客户端的配置示例，请参见[使用 MCP 将 AI 工具连接到 TiDB Cloud Lake](/tidb-cloud-lake/guides/mcp-client-integration.md)。

## 相关资源 {#related-resources}

- [PyPI 上的 `tidbcloudlake-mcp`](https://pypi.org/project/tidbcloudlake-mcp/)
- [Model Context Protocol 文档](https://modelcontextprotocol.io/)
