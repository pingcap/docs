---
title: Get started with Claude Code and TiDB MCP Server
summary: このガイドでは、Claude CodeでTiDB MCPサーバーを設定する方法を説明します。
---

# Claude CodeとTiDB MCPサーバーを使い始める {#get-started-with-claude-code-and-tidb-mcp-server}

このガイドでは、Claude CodeでTiDB MCPサーバーを設定する方法を説明します。

## 前提条件 {#prerequisites}

始める前に、以下のものを用意してください。

-   **Claude Code** ： [claude.com](https://claude.com/product/claude-code)からインストールしてください。
-   **Python (&gt;=3.10) と uv** : Python (3.10 以降) と`uv`がインストールされていることを確認します。 [インストールガイド](https://docs.astral.sh/uv/getting-started/installation/)に従って`uv`をインストールします。
-   **TiDB Cloud Starterインスタンス**: [TiDB Cloud](https://tidbcloud.com/free-trial)で無料のTiDB Cloud Starterインスタンスを作成できます。

## TiDB Cloud Starterに接続する（推奨） {#connect-to-tidb-cloud-starter-recommended}

TiDB Cloudコンソールを使用して、すぐに実行できるClaude Codeコマンドを生成します。

1.  [**私のTiDB**](https://tidbcloud.com/tidbs)ページで、対象のTiDB Cloud Starterインスタンスの名前をクリックして概要ページに移動し、右上隅の**[AI ツールで使用する]**をクリックします。

2.  表示されたダイアログで、Claude Codeがアクセスする**ブランチ**と**データベース**を選択してください。

3.  ダイアログに表示される**前提条件**リストを確認し、不足している依存関係があればインストールしてください。

4.  ルートパスワードを設定します。

    -   まだパスワードを設定していない場合は、「パスワード**を生成」をクリックして、生成されたパスワード**を安全な場所に保存してください（パスワードは一度しか表示されません）。
    -   パスワードが既に存在する場合は、 **「簡単なセットアップのためのパスワードを入力してください」**欄に入力してください。
    -   パスワードを忘れた場合は、 **「前提条件」**セクションの**「パスワードのリセット」**をクリックして新しいパスワードを生成してください。

5.  **「Claude Code」**タブを選択し、セットアップコマンドをコピーして、ターミナルで実行してください。

## 手動設定（任意のTiDBクラスタ） {#manual-configuration-any-tidb-cluster}

手動で設定する場合は、以下のいずれかの方法を使用し、プレースホルダーを接続パラメータに置き換えてください。

### 方法1：CLIコマンド {#method-1-cli-command}

```bash
claude mcp add --transport stdio TiDB \
  --env TIDB_HOST='<YOUR_TIDB_HOST>' \
  --env TIDB_PORT=<YOUR_TIDB_PORT> \
  --env TIDB_USERNAME='<YOUR_TIDB_USERNAME>' \
  --env TIDB_PASSWORD='<YOUR_TIDB_PASSWORD>' \
  --env TIDB_DATABASE='<YOUR_TIDB_DATABASE>' \
  -- uvx --from 'pytidb[mcp]' 'tidb-mcp-server'
```

### 方法2：プロジェクト設定ファイル {#method-2-project-config-file}

次の設定をプロジェクト レベルの`.mcp.json`ファイルに追加します。詳細については、 [Claude Code MCP ドキュメント](https://code.claude.com/docs/en/mcp#project-scope)を参照してください。

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

## 関連項目 {#see-also}

-   [TiDB MCPサーバー](/ai/integrations/tidb-mcp-server.md)
