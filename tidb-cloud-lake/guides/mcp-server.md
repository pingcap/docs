---
title: TiDB Cloud Lake MCP サーバー
summary: トランスポート、安全制御、利用可能なツールを含め、TiDB Cloud Lake MCP サーバーのインストール、実行、設定方法を学びます。
---

# TiDB Cloud Lake MCP サーバー

[TiDB Cloud Lake MCP サーバー](https://github.com/tidbcloud/lake-mcp) は、Model Context Protocol (MCP) をサポートするクライアントに対して {{{ .lake }}} の操作を公開します。`tidbcloudlake-mcp` パッケージは、standard input/output、HTTP、および server-sent events (SSE) のトランスポートをサポートします。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- Python 3.12 以降
- {{{ .lake }}} のアカウント、データベース、および Warehouse
- 次の形式の {{{ .lake }}} DSN:

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

接続情報の取得方法については、[Warehouse に接続する](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

## MCP サーバーをインストールする {#install-the-mcp-server}

仮想環境を作成して有効化します。

```shell
python3.12 -m venv .venv
source .venv/bin/activate
```

PyPI からサーバーをインストールします。

```shell
python -m pip install tidbcloudlake-mcp
```

## MCP サーバーを実行する {#run-the-mcp-server}

{{{ .lake }}} DSN を設定します。

```shell
export LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

デフォルトの `stdio` トランスポートでサーバーを実行します。

```shell
lake-mcp
```

アクティブな環境にインストールせずにパッケージを実行することもできます。

```shell
uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

## トランスポートを設定する {#configure-the-transport}

`LAKE_MCP_SERVER_TRANSPORT` に、次のいずれかの値を設定します。

| 値 | 説明 |
| --- | --- |
| `stdio` | 標準入出力を通じてローカル MCP クライアントと通信します。これはデフォルトです。 |
| `http` | HTTP サーバーを起動します。 |
| `sse` | server-sent events を使用するサーバーを起動します。 |

たとえば、デフォルトのループバックアドレスとポートで HTTP サーバーを実行するには、次のようにします。

```shell
export LAKE_MCP_SERVER_TRANSPORT=http
export LAKE_MCP_BIND_HOST=127.0.0.1
export LAKE_MCP_BIND_PORT=8001
lake-mcp
```

> **Warning:**
>
> バインドアドレスは信頼できるネットワークに限定してください。MCP サーバーは、設定された {{{ .lake }}} ユーザーの権限でデータにアクセスできます。

## 設定 {#configuration}

| 環境変数 | デフォルト | 説明 |
| --- | --- | --- |
| `LAKE_DSN` | {{{ .lake }}} では必須 | データベースおよび Warehouse の接続文字列です。 |
| `LAKE_MCP_SAFE_MODE` | `true` | セッションのサンドボックス検証を有効にします。 |
| `LAKE_QUERY_TIMEOUT` | `300` | クエリのタイムアウト（秒）です。 |
| `LAKE_MCP_SERVER_TRANSPORT` | `stdio` | サーバーのトランスポート: `stdio`、`http`、または `sse`。 |
| `LAKE_MCP_BIND_HOST` | `127.0.0.1` | `http` および `sse` トランスポートのバインドアドレスです。 |
| `LAKE_MCP_BIND_PORT` | `8001` | `http` および `sse` トランスポートのバインドポートです。 |

## 利用可能なツール {#available-tools}

| ツール | 説明 |
| --- | --- |
| `execute_sql` | サンドボックス検証付きで SQL を実行します。 |
| `execute_multi_sql` | 複数の SQL 文を実行します。 |
| `show_databases` | データベースを一覧表示します。 |
| `show_tables` | データベース内のテーブルを一覧表示します。 |
| `describe_table` | テーブルのスキーマを返します。 |
| `get_session_sandbox_prefix` | 現在のセッションのサンドボックスのプレフィックスを返します。 |
| `list_session_sandbox_databases` | 現在のセッションのサンドボックスデータベースを一覧表示します。 |
| `create_session_sandbox_database` | 現在のセッション用のサンドボックスデータベースを作成します。 |
| `show_stages` | stage を一覧表示します。 |
| `list_stage_files` | stage 内のファイルを一覧表示します。 |
| `create_stage` | サンドボックス検証を経て stage を作成します。 |
| `show_connections` | 接続を一覧表示します。 |

## セーフモード {#safe-mode}

セーフモードはデフォルトで有効です。セーフモードでは、次の制限があります。

- `SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`、`LIST` などの読み取り操作は、設定された {{{ .lake }}} ユーザーに許可されたオブジェクトにアクセスできます。
- 書き込み操作は、名前が現在の `mcp_sandbox_{session_id}_*` プレフィックスで始まるオブジェクトに限定されます。
- データ操作文はサンドボックステーブルのみ変更できます。
- 権限の変更はサンドボックスオブジェクトおよびプリンシパルのみを対象にできます。

`LAKE_MCP_SAFE_MODE=false` を設定するのは、MCP クライアントが信頼でき、かつ設定された {{{ .lake }}} ユーザーが必要最小限の権限を持っている場合のみにしてください。

クライアント固有の設定例については、[MCP を使用して AI ツールを TiDB Cloud Lake に接続する](/tidb-cloud-lake/guides/mcp-client-integration.md) を参照してください。

## 関連リソース {#related-resources}

- [PyPI の `tidbcloudlake-mcp`](https://pypi.org/project/tidbcloudlake-mcp/)
- [Model Context Protocol ドキュメント](https://modelcontextprotocol.io/)