---
title: Get started with Cursor and TiDB MCP Server
summary: このガイドでは、カーソル エディターで TiDB MCP サーバーを構成する方法を説明します。
---

# カーソルと TiDB MCP サーバーを使い始める {#get-started-with-cursor-and-tidb-mcp-server}

このガイドでは、カーソル エディターで TiDB MCP サーバーを構成する方法を説明します。

ワンクリックでインストールするには、次のボタンをクリックしてください。

<p><a href="cursor://anysphere.cursor-deeplink/mcp/install?name=TiDB&amp;config=eyJjb21tYW5kIjoidXZ4IC0tZnJvbSBweXRpZGJbbWNwXSB0aWRiLW1jcC1zZXJ2ZXIiLCJlbnYiOnsiVElEQl9IT1NUIjoibG9jYWxob3N0IiwiVElEQl9QT1JUIjoiNDAwMCIsIlRJREJfVVNFUk5BTU0iOiJyb290IiwiVElEQl9QQVNTV09SRCI6IiIsIlRJREJfREFUQUJBU0UiOiJ0ZXN0In19"><img alt="TiDB MCPサーバーをインストールする" src="https://cursor.com/deeplink/mcp-install-dark.svg"></img></a></p>

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **カーソル**: [カーソル.com](https://cursor.com)からカーソルをダウンロードしてインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して、クラスター資格情報でカーソル構成を作成します。

1.  [クラスター](https://tidbcloud.com/console/clusters)ページに移動し、クラスターを選択して、右上隅の**[AI ツールで使用]**をクリックします。

2.  **AI ツールを使用して`your_cluster_name`にアクセス**ダイアログで、カーソルがアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログの**前提条件**リストを確認し、不足している依存関係をインストールします。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、 **「パスワードの生成」を**クリックして、安全な場所に保存します (1 回だけ表示されます)。
    -   パスワードがすでに存在する場合は、 **「簡単セットアップ用のパスワードを入力」**フィールドに入力します。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして、新しいパスワードを生成します。

5.  **[カーソル]**タブを選択し、 **[カーソルに追加]**をクリックして、[カーソルに**インストール] を**クリックします。

## 手動構成（任意の TiDB クラスター） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、次の構成を`.cursor/mcp.json`ファイルに追加し、プレースホルダーを接続パラメータに置き換えます。

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

詳細については[モデルコンテキストプロトコルのドキュメント](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDB MCP サーバーのインストール中に問題が発生した場合は、Cursor の MCP ログを確認してください。

1.  エディターの上部にあるメイン メニューで**[ビュー]** &gt; **[出力]**をクリックします。
2.  **出力**パネルのドロップダウン メニューから**MCP**を選択します。
3.  `[error] Could not start MCP server tidb-mcp-server: Error: spawn uvx ENOENT`ようなエラーが表示された場合は、システムの`$PATH`環境変数に`uvx`コマンドが存在しない可能性があります。macOS ユーザーの場合は、 `brew install uv`を実行して`uvx`インストールできます。
