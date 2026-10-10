---
title: TiDB Cloud Lake MCP Server
summary: transport、安全制御、利用可能なツールを含め、TiDB Cloud Lake MCP server のインストール、実行、設定方法を学びます。
---

# TiDB Cloud Lake MCP Server

[TiDB Cloud Lake MCP server](https://github.com/tidbcloud/lake-mcp) は、Model Context Protocol (MCP) をサポートするクライアントに対して {{{ .lake }}} の操作を公開します。`tidbcloudlake-mcp` パッケージは、standard input/output、HTTP、および server-sent events (SSE) の transport をサポートします。

## 前提条件 {#prerequisites}

開始する前に、以下を用意してください。

- Python 3.12 以降
- {{{ .lake }}} のアカウント、データベース、および warehouse
- 次の形式の {{{ .lake }}} DSN:

    ```text
    lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>
    ```

接続情報の取得方法については、[Warehouse に接続する](/tidb-cloud-lake/guides/warehouse.md#connecting-to-a-warehouse) を参照してください。

## MCP server をインストールする {#install-the-mcp-server}

仮想環境を作成して有効化します。

```shell
python3.12 -m venv .venv
source .venv/bin/activate
```

PyPI から server をインストールします。

```shell
python -m pip install tidbcloudlake-mcp
```

## MCP server を実行する {#run-the-mcp-server}

{{{ .lake }}} DSN を設定します。

```shell
export LAKE_DSN='lake://<username>:<password>@<host>:443/<database>?warehouse=<warehouse>'
```

デフォルトの `stdio` transport で server を実行します。

```shell
lake-mcp
```

アクティブな環境にインストールせずにパッケージを実行することもできます。

```shell
uv tool run --from tidbcloudlake-mcp@latest lake-mcp
```

## transport を設定する {#configure-the-transport}

`LAKE_MCP_SERVER_TRANSPORT` に、次のいずれかの値を設定します。

| 値 | 説明 |
| --- | --- |
| `stdio` | standard input と output を通じてローカル MCP クライアントと通信します。これはデフォルトです。 |
| `http` | HTTP サーバーを起動します。 |
| `sse` | server-sent events を使用するサーバーを起動します。 |

たとえば、デフォルトの loopback address と port で HTTP サーバーを実行するには、次のようにします。

```shell
export LAKE_MCP_SERVER_TRANSPORT=http
export LAKE_MCP_BIND_HOST=127.0.0.1
export LAKE_MCP_BIND_PORT=8001
lake-mcp
```

> **Warning:**
>
> bind address は信頼できるネットワークに限定してください。MCP server は、設定された {{{ .lake }}} ユーザーの権限でデータにアクセスできます。

## 設定 {#configuration}

| 環境変数 | デフォルト | 説明 |
| --- | --- | --- |
| `LAKE_DSN` | {{{ .lake }}} では必須 | データベースおよび warehouse の接続文字列です。 |
| `LAKE_MCP_SAFE_MODE` | `true` | セッション sandbox 検証を有効にします。 |
| `LAKE_QUERY_TIMEOUT` | `300` | クエリのタイムアウト（秒）です。 |
| `LAKE_MCP_SERVER_TRANSPORT` | `stdio` | server transport: `stdio`、`http`、または `sse`。 |
| `LAKE_MCP_BIND_HOST` | `127.0.0.1` | `http` および `sse` transport の bind address です。 |
| `LAKE_MCP_BIND_PORT` | `8001` | `http` および `sse` transport の bind port です。 |

## 利用可能なツール {#available-tools}

| ツール | 説明 |
| --- | --- |
| `execute_sql` | sandbox 検証付きで SQL を実行します。 |
| `execute_multi_sql` | 複数の SQL 文を実行します。 |
| `show_databases` | データベースを一覧表示します。 |
| `show_tables` | データベース内のテーブルを一覧表示します。 |
| `describe_table` | テーブルのスキーマを返します。 |
| `get_session_sandbox_prefix` | 現在のセッションの sandbox prefix を返します。 |
| `list_session_sandbox_databases` | 現在のセッションの sandbox データベースを一覧表示します。 |
| `create_session_sandbox_database` | 現在のセッション用の sandbox データベースを作成します。 |
| `show_stages` | stage を一覧表示します。 |
| `list_stage_files` | stage 内のファイルを一覧表示します。 |
| `create_stage` | sandbox 検証の対象として stage を作成します。 |
| `show_connections` | 接続を一覧表示します。 |

## セーフモード {#safe-mode}

セーフモードはデフォルトで有効です。セーフモードでは、次の制限があります。

- `SELECT`、`SHOW`、`DESCRIBE`、`EXPLAIN`、`LIST` などの読み取り操作は、設定された {{{ .lake }}} ユーザーに許可されたオブジェクトにアクセスできます。
- 書き込み操作は、名前が現在の `mcp_sandbox_{session_id}_*` prefix で始まるオブジェクトに限定されます。
- データ操作文は sandbox テーブルのみ変更できます。
- 権限の変更は sandbox オブジェクトおよび principal のみを対象にできます。

`LAKE_MCP_SAFE_MODE=false` を設定するのは、MCP クライアントが信頼でき、かつ設定された {{{ .lake }}} ユーザーが必要最小限の権限を持っている場合のみにしてください。

クライアント固有の設定例については、[MCP を使用して AI ツールを TiDB Cloud Lake に接続する](/tidb-cloud-lake/guides/mcp-client-integration.md) を参照してください。

## 関連リソース {#related-resources}

- [PyPI の `tidbcloudlake-mcp`](https://pypi.org/project/tidbcloudlake-mcp/)
- [Model Context Protocol ドキュメント](https://modelcontextprotocol.io/)