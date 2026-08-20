---
title: Use TiDB Cloud Starter with AI Tools
summary: TiDB Cloud Starter クラスターを、Cursor、Claude Code、VS Code、Windsurf などのモデル コンテキスト プロトコル (MCP) をサポートする AI 搭載開発ツールに接続する方法を学習します。
---

# TiDB Cloud Starter を AI ツールと併用する {#use-tidb-cloud-starter-with-ai-tools}

このドキュメントでは、Cursor、Claude Code、Visual Studio Code (VS Code)、Windsurf などのモデル コンテキスト プロトコル (MCP) をサポートする AI 搭載開発ツールにTiDB Cloud Starter クラスターを接続する方法について説明します。

TiDB Cloud Starter クラスターを MCPサーバーとして構成すると、開発ツールの AI アシスタントを有効にして、データベーススキーマを照会し、データ モデルを理解し、コンテキストに応じたコード提案を生成できるようになります。

## 始める前に {#before-you-begin}

このガイドを完了するには、次のものが必要です。

-   TiDB Cloud Starter クラスター。まだお持ちでない場合は、 [TiDB Cloud Starterクラスターを作成する](/develop/dev-guide-build-cluster-in-cloud.md)を実行できます。
-   [Python 3.11以上](https://www.python.org/downloads/)がインストールされていること。
-   [uv](https://docs.astral.sh/uv/getting-started/installation/)がインストールされていること。
-   MCP をサポートする AI 開発ツール:

    -   [Cursor](https://cursor.com)
    -   [Claude Code](https://claude.com/product/claude-code)
    -   [Visual Studio Code](https://code.visualstudio.com)
    -   [Windsurf](https://windsurf.com)

## AIツールに接続する {#connect-to-ai-tools}

TiDB CloudでTiDB Cloud Starter クラスターを作成したら、次の手順を実行してそれを AI ツールに接続します。

1.  [**クラスター**](https://tidbcloud.com/project/clusters)ページで、ターゲットクラスターの名前をクリックして概要ページに移動します。次に、右上隅の**Use with AI Tools**をクリックします。

2.  **Access `your_cluster_name` with AI tools**ダイアログで、AI ツールがアクセスする**Branch**と**Database**を選択します。

3.  記載されているすべての**Prerequisites**を満たしていることを確認してください。満たしていない場合は、画面の指示に従って必要な依存関係をインストールしてください。

4.  パスワードを設定します。

    -   まだパスワードを設定していない場合は、 **Generate Password**をクリックしてランダムなパスワードを生成します。

        生成されたパスワードは再度表示されないため、パスワードは安全な場所に保存してください。

    -   すでにパスワードを設定している場合は、 **Enter the password for easy setup**フィールドにパスワードを入力します。

    -   パスワードを忘れた場合は、 **Prerequisites**セクションの**Reset password**をクリックして、新しいパスワードを生成します。

        パスワードをリセットすると、既存のすべての root ユーザー セッションが切断されることに注意してください。

5.  AI ツールのタブを選択します: **Cursor** 、 **Claude Code** 、 **VS Code** 、または**Windsurf** 。

6.  選択したツールのセットアップ手順を完了します。

    詳細については[ツール固有の設定](#tool-specific-setup)を参照してください。

## ツール固有の設定 {#tool-specific-setup}

### Cursor {#cursor}

Cursor を TiDB の MCP クライアントとして構成するには、次のいずれかの方法を使用できます。

-   **方法 1** : [TiDB Cloudコンソール](https://tidbcloud.com)の**Access `your_cluster_name` with AI tools**ダイアログで、**Add to Cursor**をクリックしてCursorを起動し、**Install**をクリックします。
-   **方法 2** : 次の構成を`.cursor/mcp.json`ファイルに手動で追加します。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "command": "uvx --from pytidb[mcp] tidb-mcp-server",
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Claude Code {#claude-code}

Claude Code を TiDB の MCP クライアントとして構成するには、次のいずれかの方法を使用できます。

-   **方法 1** : [TiDB Cloudコンソール](https://tidbcloud.com/)の**Access `your_cluster_name` with AI tools**ダイアログからセットアップ コマンドをコピーし、ターミナルで実行します。

    ```bash
    claude mcp add --transport stdio TiDB \
      --env TIDB_HOST='<YOUR_TIDB_HOST>' \
      --env TIDB_PORT=<YOUR_TIDB_PORT> \
      --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
      --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
      --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
      -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
    ```

-   **方法2** ：プロジェクトレベル`.mcp.json`ファイルに以下の設定を追加します。詳細については、 [Claude Codeのドキュメント](https://code.claude.com/docs/en/mcp#project-scope)を参照してください。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### VS Code {#vs-code}

VS Code を TiDB の MCP クライアントとして構成するには、次のいずれかの方法を使用できます。

-   **方法 1** : [TiDB Cloudコンソール](https://tidbcloud.com/)の**Access `your_cluster_name` with AI tools**ダイアログで、 **Add to VS Code**をクリックして VS Code を起動し、 **Install**をクリックします。
-   **方法 2** : `.vscode/mcp.json`ファイルに次の構成を追加します。

    ```json
    {
      "mcpServers": {
        "TiDB": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
          "env": {
            "TIDB_HOST": "<YOUR_TIDB_HOST>",
            "TIDB_PORT": "<YOUR_TIDB_PORT>",
            "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
            "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
            "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
          }
        }
      }
    }
    ```

### Windsurf {#windsurf}

TiDB MCPプラグインをWindsurfに追加するには、 `mcp_config.json`ファイルを以下のように更新してください。詳細については、 [Windsurfのドキュメント](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin)を参照してください。

```json
{
  "mcpServers": {
    "TiDB": {
      "command": "uvx",
      "args": ["--from", "pytidb[mcp]", "tidb-mcp-server"],
      "env": {
        "TIDB_HOST": "<YOUR_TIDB_HOST>",
        "TIDB_PORT": "<YOUR_TIDB_PORT>",
        "TIDB_USERNAME": "<YOUR_TIDB_USERNAME>",
        "TIDB_PASSWORD": "<YOUR_TIDB_PASSWORD>",
        "TIDB_DATABASE": "<YOUR_TIDB_DATABASE>"
      }
    }
  }
}
```

## 参照 {#see-also}

-   [TiDB + Vector Search を試す](/ai/quickstart-via-python.md)
-   [開発者ガイドの概要](https://docs.pingcap.com/developer/)
