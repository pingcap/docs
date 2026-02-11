---
title: TiDB MCP Server
summary: TiDB MCP サーバーを使用して、自然言語の指示を使用して TiDB データベースを管理します。
---

# TiDB MCP サーバー {#tidb-mcp-server}

TiDB MCP サーバーは、自然言語の指示を使用して TiDB データベースと対話できるオープンソース ツールです。

## MCP と TiDB MCP サーバーの理解 {#understanding-mcp-and-tidb-mcp-server}

[モデルコンテキストプロトコル（MCP）](https://modelcontextprotocol.io/introduction)は、LLM と外部ツール間の通信を標準化するプロトコルです。

MCP はクライアント サーバーアーキテクチャを採用しており、ホスト アプリケーションが複数の外部サーバーに接続できます。

-   **ホスト**: MCP サーバーへの接続を開始する、Claude Desktop などの AI 搭載アプリケーションや、Cursor などの IDE。

-   **クライアント**: 個々の MCP サーバーと 1 対 1 の接続を確立するホスト アプリケーション内に埋め込まれたコンポーネント。

-   **サーバー**: 外部システムと対話するためのツール、コンテキスト、プロンプトをクライアントに提供する**TiDB MCP サーバー**などの外部サービス。

**TiDB MCP サーバーは**、MCP クライアントが TiDB データベースと対話するためのツールとコンテキストを提供する MCP 互換サーバーです。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **MCP 互換クライアント**: たとえば、 [カーソル](/ai/integrations/tidb-mcp-cursor.md)または[クロード・デスクトップ](/ai/integrations/tidb-mcp-claude-desktop.md) 。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## サポートされているMCPクライアント {#supported-mcp-clients}

特定の MCP クライアントで TiDB MCP サーバーを使用する詳細な例については、次のガイドを参照してください。

-   [カーソル](/ai/integrations/tidb-mcp-cursor.md)
-   [クロード・デスクトップ](/ai/integrations/tidb-mcp-claude-desktop.md)

上記のリストに MCP クライアントが含まれていない場合は、以下のセットアップ手順に従ってください。

## セットアップ手順 {#setup-steps}

TiDB MCP サーバーは、MCP クライアントと統合するための 2 つのモードをサポートしています。

-   標準入出力（STDIO）モード（デフォルト）
-   サーバー送信イベント（SSE）モード

TiDB MCP サーバーはデフォルトで STDIO モードを使用するため、事前にスタンドアロンサーバーを起動する必要はありません。

MCP クライアントで TiDB MCP サーバーを設定するには、いずれかのモードを選択できます。

### STDIOモード {#stdio-mode}

STDIO モードを使用して MCP クライアントで TiDB MCP サーバーを設定するには、次の手順を実行します。

1.  MCPサーバーを構成する方法については、MCP クライアントのドキュメントを参照してください。

2.  [TiDB Cloudクラスター](https://tidbcloud.com/console/clusters)ページに移動し、クラスターの概要ページに移動します。

3.  クラスターの概要ページで**[接続]**をクリックして、接続パラメータを取得します。

4.  AI アプリケーションの構成ファイルの`mcpServers`セクションで、接続パラメータを使用して TiDB MCP サーバーを構成します。

    MCP 構成ファイルの例:

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

SSE モードを使用して MCP クライアントに TiDB MCP サーバーを設定するには、次の手順を実行します。

1.  MCPサーバーを構成する方法については、MCP クライアントのドキュメントを参照してください。

2.  [TiDB Cloudクラスター](https://tidbcloud.com/console/clusters)ページに移動してクラスターを選択します。

3.  接続パラメータを取得するには、クラスター ページで**[接続]**をクリックします。

4.  接続パラメータを含む`.env`ファイルを作成します。

    例`.env`ファイル:

    ```bash
    cat > .env <<EOF
    TIDB_HOST={gateway-region}.prod.aws.tidbcloud.com
    TIDB_PORT=4000
    TIDB_USERNAME={prefix}.root
    TIDB_PASSWORD={password}
    TIDB_DATABASE=test
    EOF
    ```

5.  `--transport sse`オプションで TiDB MCP サーバーを起動します。

    ```bash
    uvx --from "pytidb[mcp]" tidb-mcp-server --transport sse
    ```

6.  AI アプリケーションの構成ファイルの`mcpServers`セクションに`TiDB` MCPサーバー構成を追加します。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "url": "http://localhost:8000/sse"
        }
      }
    }
    ```

## サポートされているアクション（ツール） {#supported-actions-tools}

TiDB MCPサーバーは、MCPクライアントに以下のアクション（ツール）を提供します。これらを使用することで、自然言語による指示でTiDBプロジェクトやデータベースと対話できます。

**データベース管理**

-   `show_databases` - TiDB クラスター内のすべてのデータベースを表示します

    -   `username` : データベースユーザー名（文字列、オプション）
    -   `password` : データベースパスワード（文字列、オプション）

-   `switch_database` - 特定のデータベースに切り替える

    -   `db_name` : 切り替え先のデータベース名（文字列、必須）
    -   `username` : データベースユーザー名（文字列、オプション）
    -   `password` : データベースパスワード（文字列、オプション）

-   `show_tables` - 現在のデータベース内のすべてのテーブルを表示します

**SQLクエリと実行**

-   `db_query` - 読み取り専用SQLクエリを実行する

    -   `sql_stmt` : SQLクエリステートメント（文字列、必須）

-   `db_execute` - SQL文（DMLまたはDDL）を実行する

    -   `sql_stmts` : 単一のSQL文またはSQL文の配列（文字列または配列、必須）

**ユーザー管理**

-   `db_create_user` - 新しいデータベースユーザーを作成する

    -   `username` : 新しいユーザーの名前（文字列、必須）
    -   `password` : 新しいユーザーのパスワード（文字列、必須）

-   `db_remove_user` - 既存のデータベースユーザーを削除する

    -   `username` : 削除するユーザーの名前（文字列、必須）
