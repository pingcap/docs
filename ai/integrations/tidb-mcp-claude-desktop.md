---
title: Get started with Claude Desktop and TiDB MCP Server
summary: このガイドでは、Claude DesktopでTiDB MCPサーバーを設定する方法を説明します。
---

# Claude DesktopとTiDB MCP Serverを使い始めましょう {#get-started-with-claude-desktop-and-tidb-mcp-server}

このガイドでは、Claude DesktopでTiDB MCPサーバーを設定する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Claude Desktop** :[クロード・アイ](https://claude.ai/download)から Claude Desktop をダウンロードしてインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10 以降) と`uv`がインストールされていることを確認します。 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をインストールします。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## セットアップ手順 {#setup-steps}

Claude DesktopでTiDB MCPサーバーを設定するには、以下の手順に従ってください。

1.  **設定**ダイアログを開きます。

2.  ダイアログの「**開発者」**タブをクリックします。

3.  **「設定の編集」**ボタンをクリックして、MCP設定ファイル`claude_desktop_config.json`を開きます。

4.  以下の設定を`claude_desktop_config.json`ファイルにコピーしてください。

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

5.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックすると、その概要ページに移動します。

6.  右上隅の**「接続」**をクリックして接続パラメータを取得し、 `TIDB_HOST` 、 `TIDB_PORT` 、 `TIDB_USERNAME` 、 `TIDB_PASSWORD` 、および`TIDB_DATABASE`の値を自分の値に置き換えてください。

7.  Claude Desktopを再起動してください。

詳細については、 [Claude DesktopでMCPサーバーを設定する方法](https://modelcontextprotocol.io/quickstart/user)を参照してください。
