---
title: Get started with Claude Code and TiDB MCP Server
summary: このガイドでは、Claude Code で TiDB MCP サーバーを構成する方法を説明します。
---

# Claude CodeとTiDB MCP Serverを使い始める {#get-started-with-claude-code-and-tidb-mcp-server}

このガイドでは、Claude Code で TiDB MCP サーバーを構成する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、次のものがあることを確認してください。

-   **Claude Code** : [claude.com](https://claude.com/product/claude-code)からインストールします。
-   **Python (&gt;=3.10) と uv** : Python (3.10以降) と`uv`インストールされていることを確認してください。4 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)手順に従って`uv`インストールしてください。
-   **TiDB Cloud Starter クラスター**: [TiDB Cloud](https://tidbcloud.com/free-trial)に無料の TiDB クラスターを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して、すぐに実行できる Claude Code コマンドを生成します。

1.  [クラスター](https://tidbcloud.com/console/clusters)ページに移動し、クラスターを選択して、右上隅の**[AI ツールで使用]**をクリックします。

2.  **AI ツールを使用して`your_cluster_name`にアクセス**ダイアログで、Claude Code がアクセスする**ブランチ**と**データベース**を選択します。

3.  ダイアログの**前提条件**リストを確認し、不足している依存関係をインストールします。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、 **「パスワードの生成」を**クリックして、安全な場所に保存します (1 回だけ表示されます)。
    -   パスワードがすでに存在する場合は、 **「簡単セットアップ用のパスワードを入力」**フィールドに入力します。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして、新しいパスワードを生成します。

5.  **Claude コード**タブを選択し、セットアップ コマンドをコピーして、ターミナルで実行します。

## 手動構成（任意の TiDB クラスター） {#manual-configuration-any-tidb-cluster}

手動でセットアップする場合は、次のいずれかの方法を使用し、プレースホルダーを接続パラメータに置き換えます。

### 方法1: CLIコマンド {#method-1-cli-command}

```bash
claude mcp add --transport stdio TiDB \
  --env TIDB_HOST='<YOUR_TIDB_HOST>' \
  --env TIDB_PORT=<YOUR_TIDB_PORT> \
  --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
  --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
  --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
  -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
```

### 方法2: プロジェクト構成ファイル {#method-2-project-config-file}

プロジェクトレベル`.mcp.json`ファイルに以下の設定を追加してください。詳細は[Claude Code MCP ドキュメント](https://code.claude.com/docs/en/mcp#project-scope)をご覧ください。

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
