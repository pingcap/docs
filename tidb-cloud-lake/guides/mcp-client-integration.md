---
title: MCP を使用して AI ツールを TiDB Cloud Lake に接続する
summary: MCP 対応の AI ツールを TiDB Cloud Lake に接続し、安全なデータ探索のためにセッションサンドボックス保護を使用する方法を学びます。
---

# MCP を使用して AI ツールを TiDB Cloud Lake に接続する

[TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) は、[Model Context Protocol (MCP)](https://modelcontextprotocol.io/) を通じて AI アシスタントを {{{ .lake }}} に接続します。MCP 対応ツールを使用すると、自然言語の指示でデータベースオブジェクトの探索、テーブルスキーマの確認、SQL の実行ができます。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- Python 3.12 以降
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) がインストールされていること
- MCP 対応の AI ツール
- {{{ .lake }}} のアカウント、データベース、および Warehouse

## 接続文字列を取得する {#get-a-connection-string}

{{{ .lake }}} の Warehouse から host、username、password、database、および warehouse 名を取得します。詳細は、[Warehouse に接続する](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

次の形式で DSN を作成します。

```text
lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
```

## MCP クライアントを設定する {#configure-an-mcp-client}

以下の設定では、`uv` を使用して最新の `tidbcloudlake-mcp` パッケージを実行します。各例では safe mode を明示的に有効にしています。

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

次のサーバーを Cursor の MCP 設定に追加します。

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

次のサーバーを、Gemini CLI の `settings.json` ファイル内の `mcpServers` オブジェクトに追加します。

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

標準の JSON 設定を受け付ける MCP クライアントでは、次のサーバーを追加します。

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

MCP 設定を保存した後、AI ツールを再起動します。その後、データベースの一覧表示、テーブルの確認、またはクエリの実行をツールに依頼できます。

## セッションサンドボックス保護 {#session-sandbox-protection}

`LAKE_MCP_SAFE_MODE` は、サーバーが書き込み操作をセッション固有のサンドボックスに対して検証するかどうかを制御します。

| 値 | 動作 |
| --- | --- |
| `true` | AI ツールに対して本番オブジェクトは読み取り専用になります。書き込みは、現在の `mcp_sandbox_{session_id}_*` プレフィックスで始まる名前のオブジェクトに制限されます。これはデフォルトかつ推奨の設定です。 |
| `false` | サーバーは、設定された {{{ .lake }}} ユーザーに許可されている任意の SQL 操作を許可します。この設定は、信頼できるツールと最小権限のアカウントでのみ使用してください。 |

MCP ツール `get_session_sandbox_prefix` は、現在のセッションのプレフィックスを返します。

サーバーのトランスポート、設定変数、および利用可能な MCP ツールについては、[TiDB Cloud Lake MCP Server](/tidb-cloud-lake/guides/mcp-server.md) を参照してください。