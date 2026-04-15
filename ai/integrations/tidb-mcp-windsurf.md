---
title: Get started with Windsurf and TiDB MCP Server
summary: このガイドでは、Windsurf で TiDB MCP サーバーを設定する方法を説明します。
---

# WindsurfとTiDB MCPサーバーを使い始める {#get-started-with-windsurf-and-tidb-mcp-server}

このガイドでは、Windsurf で TiDB MCP サーバーを設定する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Windsurf** ： [windsurf.com](https://windsurf.com)からWindsurfをダウンロードしてインストールしてください。
-   **Python (&gt;=3.10) と uv** : Python (3.10 以降) と`uv`がインストールされていることを確認します。 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をインストールします。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して接続の詳細を取得し、WindsurfのMCP構成を更新してください。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックして概要ページに移動し、右上隅の**[AI ツールで使用する]**をクリックします。

2.  表示されたダイアログで、Windsurfがアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログに表示される**前提条件**リストを確認し、不足している依存関係があればインストールしてください。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、「パスワード**を生成」をクリックして、生成されたパスワード**を安全な場所に保存してください（パスワードは一度しか表示されません）。
    -   パスワードが既に存在する場合は、 **「簡単なセットアップのためのパスワードを入力してください」**欄に入力してください。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして新しいパスワードを生成してください。

5.  **「ウィンドサーフィン」**タブを選択し、表示された接続値をコピーしてください。

6.  コピーした値を使用して`mcp_config.json`ファイルを更新します。詳細については、 [Windsurf MCP ドキュメント](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin)を参照してください。

## 手動設定（任意のTiDBクラスタ） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、 `mcp_config.json`ファイルを次のように更新し、プレースホルダーを接続パラメータに置き換えてください。

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

## 関連項目 {#see-also}

-   [TiDB MCPサーバー](/ai/integrations/tidb-mcp-server.md)
