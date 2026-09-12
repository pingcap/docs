---
title: 使用 MCP 将 AI 工具连接到 TiDB Cloud Lake
summary: 了解如何将兼容 MCP 的 AI 工具连接到 TiDB Cloud Lake，并使用会话沙箱保护来安全地探索数据。
---

# 使用 MCP 将 AI 工具连接到 TiDB Cloud Lake

[TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) 通过 [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) 将 AI 助手连接到 {{{ .lake }}}。借助兼容 MCP 的工具，你可以使用自然语言指令探索数据库对象、检查表结构，并运行 SQL。

## 前提条件 {#prerequisites}

开始之前，请确保你具备以下条件：

- Python 3.12 或更高版本
- 已安装 [`uv`](https://docs.astral.sh/uv/getting-started/installation/)
- 一个兼容 MCP 的 AI 工具
- 一个 {{{ .lake }}} 账户、数据库和计算集群 (Warehouse)

## 获取连接字符串 {#get-a-connection-string}

从你的 {{{ .lake }}} 计算集群中获取主机、用户名、密码、数据库和计算集群名称。更多信息，请参见[连接到计算集群](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse)。

使用以下格式构建 DSN：

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

## 配置 MCP 客户端 {#configure-an-mcp-client}

以下配置使用 `uv` 运行最新的 `tidbcloudlake-mcp` 包。每个示例中都显式启用了安全模式。

<SimpleTab groupId="lake-mcp-clients">

<div label="Codex" value="codex">

```shell
codex mcp add lake-mcp \
    --env LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>' \
    --env LAKE_MCP_SAFE_MODE=true \
    -- uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

</div>

<div label="Claude Code" value="claude-code">

```shell
claude mcp add lake-mcp \
    --env LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>' \
    --env LAKE_MCP_SAFE_MODE=true \
    -- uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

</div>

<div label="Cursor" value="cursor">

将以下服务器添加到你的 Cursor MCP 配置中：

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Gemini CLI" value="gemini-cli">

将以下服务器添加到你的 Gemini CLI `settings.json` 文件中的 `mcpServers` 对象：

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

<div label="Other MCP Clients" value="other">

对于接受标准 JSON 配置的 MCP 客户端，添加以下服务器：

```json
{
  "mcpServers": {
    "lake-mcp": {
      "command": "uv",
      "args": ["tool", "run", "--from", "tidbcloudlake-mcp@latest", "lake-mcp"],
      "env": {
        "LAKE_DSN": "lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>",
        "LAKE_MCP_SAFE_MODE": "true"
      }
    }
  }
}
```

</div>

</SimpleTab>

保存 MCP 配置后，重启 AI 工具。然后，你就可以让该工具列出数据库、检查表，或运行查询。

## 会话沙箱保护 {#session-sandbox-protection}

`LAKE_MCP_SAFE_MODE` 用于控制服务器是否根据会话专属的沙箱来校验写操作。

| 值 | 行为 |
| --- | --- |
| `true` | 对 AI 工具而言，生产对象是只读的。写操作仅限于名称以当前 `mcp_sandbox_{session_id}_*` 前缀开头的对象。这是默认且推荐的设置。 |
| `false` | 服务器允许已配置的 {{{ .lake }}} 用户所具备权限允许的任何 SQL 操作。仅在使用受信任的工具和最小权限账户时使用此设置。 |

MCP 工具 `get_session_sandbox_prefix` 会返回当前会话的前缀。

有关服务器传输方式、配置变量以及可用的 MCP 工具，请参见 [TiDB Cloud Lake MCP Server](/tidb-cloud-lake/guides/mcp-server.md)。