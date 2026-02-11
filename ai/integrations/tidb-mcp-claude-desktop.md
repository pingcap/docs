---
title: Get started with Claude Desktop and TiDB MCP Server
summary: このガイドでは、Claude Desktop で TiDB MCP サーバーを構成する方法を説明します。
---

# Claude DesktopとTiDB MCP Serverを使い始める {#get-started-with-claude-desktop-and-tidb-mcp-server}

このガイドでは、Claude Desktop で TiDB MCP サーバーを構成する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Claude Desktop** : [claude.ai](https://claude.ai/download)から Claude Desktop をダウンロードしてインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## セットアップ手順 {#setup-steps}

Claude Desktop で TiDB MCP サーバーを設定するには、以下の手順に従います。

1.  **設定**ダイアログを開きます。

2.  ダイアログの「**開発者」**タブをクリックします。

3.  **[Edit Config]**ボタンをクリックして、MCP 構成ファイル`claude_desktop_config.json`を開きます。

4.  次の設定を`claude_desktop_config.json`ファイルにコピーします。

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

5.  [TiDB Cloudクラスターページ](https://tidbcloud.com/console/clusters)に移動し、接続するクラスターに移動します。

6.  右上隅の**[接続]**をクリックして接続パラメータを取得し、 `TIDB_HOST` 、 `TIDB_PORT` 、 `TIDB_USERNAME` 、 `TIDB_PASSWORD` 、 `TIDB_DATABASE`の値を独自の値に置き換えます。

7.  Claude Desktop を再起動します。

詳細については[Claude DesktopでMCPサーバーを構成する方法](https://modelcontextprotocol.io/quickstart/user)参照してください。
