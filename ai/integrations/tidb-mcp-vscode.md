---
title: Get started with Visual Studio Code and TiDB MCP Server
summary: このガイドでは、Visual Studio Code で TiDB MCP サーバーを構成する方法を説明します。
---

# Visual Studio Code と TiDB MCP サーバーを使い始める {#get-started-with-visual-studio-code-and-tidb-mcp-server}

このガイドでは、Visual Studio Code (VS Code) で TiDB MCP サーバーを構成する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Visual Studio Code** : [code.visualstudio.com](https://code.visualstudio.com)から VS Code をダウンロードしてインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して VS Code 構成を生成します。

1.  [クラスター](https://tidbcloud.com/console/clusters)ページに移動し、クラスターを選択して、右上隅の**[AI ツールで使用]**をクリックします。

2.  **AI ツールを使用して`your_cluster_name`にアクセス**ダイアログで、VS Code がアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログの**前提条件**リストを確認し、不足している依存関係をインストールします。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、 **「パスワードの生成」を**クリックして、安全な場所に保存します (1 回だけ表示されます)。
    -   パスワードがすでに存在する場合は、 **「簡単セットアップ用のパスワードを入力」**フィールドに入力します。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして、新しいパスワードを生成します。

5.  **VS Code**タブを選択し、 **VS Code に追加**をクリックして、VS Code に**インストール を**クリックします。

## 手動構成（任意の TiDB クラスター） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、次の構成を`.vscode/mcp.json`ファイルに追加し、プレースホルダーを接続パラメータに置き換えます。

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

## 参照 {#see-also}

-   [TiDB MCP サーバー](/ai/integrations/tidb-mcp-server.md)
