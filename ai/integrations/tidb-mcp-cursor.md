---
title: Get started with Cursor and TiDB MCP Server
summary: このガイドでは、カーソルエディタでTiDB MCPサーバーを設定する方法を説明します。
---

# CursorとTiDB MCPサーバーを使い始める {#get-started-with-cursor-and-tidb-mcp-server}

このガイドでは、カーソルエディタでTiDB MCPサーバーを設定する方法を説明します。

ワンクリックでインストールするには、次のボタンをクリックしてください。

<p><a href="cursor://anysphere.cursor-deeplink/mcp/install?name=TiDB&amp;config=eyJjb21tYW5kIjoidXZ4IC0tZnJvbSBweXRpZGJbbWNwXSB0aWRiLW1jcC1zZXJ2ZXIiLCJlbnYiOnsiVElEQl9IT1NUIjoibG9jYWxob3N0IiwiVElEQl9QT1JUIjoiNDAwMCIsIlRJREJfVVNFUk5BTU0iOiJyb290IiwiVElEQl9QQVNTV09SRCI6IiIsIlRJREJfREFUQUJBU0UiOiJ0ZXN0In19"><img alt="TiDB MCPサーバーをインストールする" src="https://cursor.com/deeplink/mcp-install-dark.svg"></img></a></p>

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Cursor** ： [cursor.com](https://cursor.com)からCursorをダウンロードしてインストールしてください。
-   **Python (&gt;=3.10) と uv** : Python (3.10 以降) と`uv`がインストールされていることを確認します。 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をインストールします。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して、 TiDB Cloud Starterインスタンスの認証情報でカーソル構成を作成します。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックして概要ページに移動し、右上隅の**[AI ツールで使用する]**をクリックします。

2.  表示されたダイアログで、カーソルがアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログに表示される**前提条件**リストを確認し、不足している依存関係があればインストールしてください。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、「パスワード**を生成」をクリックして、生成されたパスワード**を安全な場所に保存してください（パスワードは一度しか表示されません）。
    -   パスワードが既に存在する場合は、 **「簡単なセットアップのためのパスワードを入力してください」**欄に入力してください。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして新しいパスワードを生成してください。

5.  **「カーソル」**タブを選択し、 **「カーソルに追加」**をクリックしてから、「カーソルに**インストール」を**クリックします。

## 手動設定（任意のTiDBクラスタ） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、 `.cursor/mcp.json`ファイルに次の設定を追加し、プレースホルダーを接続パラメータに置き換えてください。

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

詳細については、 [モデルコンテキストプロトコルのドキュメント](https://docs.cursor.com/context/model-context-protocol#configuring-mcp-servers)を参照してください。

## トラブルシューティング {#troubleshooting}

TiDB MCPサーバーのインストールで問題が発生した場合は、CursorのMCPログを確認してください。

1.  エディタ上部のメインメニューで、 **[ビュー]** &gt; **[出力]**をクリックします。
2.  **出力**パネルのドロップダウンメニューから**「MCP」**を選択してください。
3.  `[error] Could not start MCP server tidb-mcp-server: Error: spawn uvx ENOENT`のようなエラーが表示される場合は、 `uvx`コマンドがシステム環境変数`$PATH`に存在しない可能性があります。macOS ユーザーの場合は、 `uvx`を実行して`brew install uv` 。
