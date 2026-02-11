---
title: Get started with Windsurf and TiDB MCP Server
summary: このガイドでは、Windsurf で TiDB MCP サーバーを構成する方法を説明します。
---

# WindsurfとTiDB MCPサーバーを使い始める {#get-started-with-windsurf-and-tidb-mcp-server}

このガイドでは、Windsurf で TiDB MCP サーバーを構成する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Windsurf** : [ウィンドサーフィン.com](https://windsurf.com)から Windsurf をダウンロードしてインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して接続の詳細を収集し、Windsurf の MCP 構成を更新します。

1.  [クラスター](https://tidbcloud.com/console/clusters)ページに移動し、クラスターを選択して、右上隅の**[AI ツールで使用]**をクリックします。

2.  **AI ツールを使用して`your_cluster_name`にアクセス**ダイアログで、Windsurf がアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログの**前提条件**リストを確認し、不足している依存関係をインストールします。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、 **「パスワードの生成」を**クリックして、安全な場所に保存します (1 回だけ表示されます)。
    -   パスワードがすでに存在する場合は、 **「簡単セットアップ用のパスワードを入力」**フィールドに入力します。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして、新しいパスワードを生成します。

5.  **Windsurf**タブを選択し、提供された接続値をコピーします。

6.  コピーした値を使用して`mcp_config.json`ファイルを更新してください。詳細については、 [Windsurf MCP ドキュメント](https://docs.windsurf.com/windsurf/cascade/mcp#adding-a-new-mcp-plugin)を参照してください。

## 手動構成（任意の TiDB クラスター） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、 `mcp_config.json`ファイルを次のように更新し、プレースホルダーを接続パラメータに置き換えます。

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

-   [TiDB MCP サーバー](/ai/integrations/tidb-mcp-server.md)
