---
title: TiDB MCP Server
summary: TiDB MCPサーバーを使用すると、自然言語による指示でTiDBデータベースを管理できます。
---

# TiDB MCPサーバー {#tidb-mcp-server}

TiDB MCP Serverは、自然言語による指示を用いてTiDBデータベースとやり取りできるオープンソースツールです。

## MCPとTiDB MCPサーバーの理解 {#understanding-mcp-and-tidb-mcp-server}

[モデルコンテキストプロトコル（MCP）](https://modelcontextprotocol.io/introduction)は、LLMと外部ツール間の通信を標準化するプロトコルです。

MCPはクライアント/サーバーアーキテクチャを採用しており、ホストアプリケーションが複数の外部サーバーに接続できるようになっている。

-   **ホスト**：Claude DesktopやCursorなどのIDEといった、MCPサーバーへの接続を開始するAI搭載アプリケーション。

-   **クライアント**：ホストアプリケーションに組み込まれたコンポーネントで、個々のMCPサーバーと1対1の接続を確立する。

-   **サーバー**： **TiDB MCPサーバー**などの外部サービスで、クライアントが外部システムとやり取りするためのツール、コンテキスト、およびプロンプトを提供します。

**TiDB MCPサーバーは**、MCP互換サーバーであり、MCPクライアントがTiDBデータベースとやり取りするためのツールとコンテキストを提供します。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **MCP 互換クライアント**: 例:[カーソル](/ai/integrations/tidb-mcp-cursor.md)や[クロード・デスクトップ](/ai/integrations/tidb-mcp-claude-desktop.md)。
-   **Python (&gt;=3.10) と uv** : Python (3.10 以降) と`uv`がインストールされていることを確認します。 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をインストールします。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## サポートされているMCPクライアント {#supported-mcp-clients}

TiDB MCPサーバーを特定のMCPクライアントで使用する詳細な例については、以下のガイドを参照してください。

-   [カーソル](/ai/integrations/tidb-mcp-cursor.md)
-   [クロード・デスクトップ](/ai/integrations/tidb-mcp-claude-desktop.md)

上記のリストにMCPクライアントが含まれていない場合は、以下のセットアップ手順に従ってください。

## セットアップ手順 {#setup-steps}

TiDB MCPサーバーは、MCPクライアントとの統合に関して2つのモードをサポートしています。

-   標準入出力（STDIO）モード（デフォルト）
-   サーバー送信イベント（SSE）モード

TiDB MCPサーバーはデフォルトでSTDIOモードを使用するため、事前にスタンドアロンサーバーを起動する必要はありません。

MCPクライアントでTiDB MCPサーバーを設定するには、以下のいずれかのモードを選択できます。

### STDIOモード {#stdio-mode}

STDIOモードを使用してMCPクライアントにTiDB MCPサーバーを設定するには、以下の手順を実行してください。

1.  MCPサーバーの設定方法については、MCPクライアントのドキュメントを参照してください。

2.  TiDB Cloudコンソールで、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Starterインスタンスの名前をクリックして概要ページに移動します。

3.  接続パラメータを取得するには、右上隅の**「接続」**をクリックしてください。

4.  AIアプリケーションの設定ファイルの`mcpServers`セクションで、接続パラメータを使用してTiDB MCPサーバーを設定します。

    MCP設定ファイルの例：

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

### サーバー送信イベント（SSE）モード {#server-sent-events-sse-mode}

MCPクライアントでSSEモードを使用してTiDB MCPサーバーを設定するには、以下の手順を実行してください。

1.  MCPサーバーの設定方法については、MCPクライアントのドキュメントを参照してください。

2.  TiDB Cloudコンソールで、[**私のTiDB**](https://tidbcloud.com/tidbs)ページに移動し、対象のTiDB Cloud Starterインスタンスの名前をクリックして概要ページに移動します。

3.  接続パラメータを取得するには、右上隅の**「接続」**をクリックしてください。

4.  接続パラメータを含む`.env`ファイルを作成します。

    `.env`ファイルの例:

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    EOF
    ```

5.  `--transport sse`オプションを指定して TiDB MCP サーバーを起動します。

    ```bash
    uvx --from "pytidb[mcp]" tidb-mcp-server --transport sse
    ```

6.  `TiDB` MCPサーバー構成を、AIアプリケーション構成ファイルの`mcpServers`セクションに追加します。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "url": "http://localhost:8000/sse"
        }
      }
    }
    ```

## サポートされている操作（ツール） {#supported-actions-tools}

TiDB MCPサーバーは、MCPクライアントに以下の操作（ツール）を提供します。これらのツールを使用すると、自然言語による指示でTiDBプロジェクトやデータベースを操作できます。

**データベース管理**

-   `show_databases` - TiDB Cloud Starterインスタンス内のすべてのデータベースを表示します

    -   `username` : データベースユーザー名（文字列、オプション）
    -   `password` : データベースパスワード（文字列、オプション）

-   `switch_database` - 特定のデータベースに切り替える

    -   `db_name` : 切り替え先のデータベース名（文字列、必須）
    -   `username` : データベースユーザー名（文字列、オプション）
    -   `password` : データベースパスワード（文字列、オプション）

-   `show_tables` - 現在のデータベース内のすべてのテーブルを表示します

**SQLクエリと実行**

-   `db_query` - 読み取り専用のSQLクエリを実行します

    -   `sql_stmt` : SQLクエリステートメント（文字列、必須）

-   `db_execute` - SQLステートメント（DMLまたはDDL）を実行します

    -   `sql_stmts` : 単一のSQL文、またはSQL文の配列（文字列または配列、必須）

**ユーザー管理**

-   `db_create_user` - 新しいデータベースユーザーを作成します

    -   `username` : 新規ユーザーの名前（文字列、必須）
    -   `password` : 新規ユーザーのパスワード（文字列、必須）

-   `db_remove_user` - 既存のデータベースユーザーを削除します

    -   `username` : 削除するユーザーの名前（文字列、必須）
