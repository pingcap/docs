---
title: ti fs-git add-git-worktree
summary: マウントされた TiDB Cloud Filesystem に、リンクされた Git worktree を追加します。
---

# ti fs-git add-git-worktree

ベースワークスペースから、リンクされた Git worktree を追加します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-git add-git-worktree
  --base-path <string>
  --worktree-path <string>
  [--blobless]
  [--branch-name <string>]
  [--commit-ish <string>]
  [--detach]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--hydrate <string>]
  [--version]
```

## オプション {#options}

- `--base-path <string>`: ベース Git ワークスペースのマウントされたファイルシステムパスです。\[required]
- `--worktree-path <string>`: リンクされた worktree 用のマウントされたファイルシステムパスです。\[required]
- `--blobless`: ベースワークスペースが blobless Git ストレージを使用していることを検証します。このオプションは、blobless でないワークスペースを変換しません。
- `--branch-name <string>`: リンクされた worktree 用のブランチを作成します。
- `--commit-ish <string>`: リンクされた worktree 用の任意の commit-ish です。
- `--detach`: detached なリンク済み worktree を作成します。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: ファイルシステムトークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択したファイルシステム用にローカルに保存されたトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--hydrate <string>`: クリーンデータの hydration モード: `auto`、`background`、`sync`、または `off`。`auto` では、blobless ベースにリンクされた worktree はバックグラウンドで hydration され、blobless でないベースにリンクされた worktree では個別の hydration ステップは実行されません。`background` と `sync` には blobless ベースが必要です。`off` は hydration をスキップします。\[default: auto]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共有されるオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- 新しいブランチに worktree を作成します。

    ```bash
    # Give an agent an isolated branch while sharing the base Git object store.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-feature --branch-name feature-x
    ```

- detached worktree を作成します。

    ```bash
    # Inspect a commit without creating or switching a branch.
    ti fs-git add-git-worktree --file-system-id <file-system-id> --base-path /path/to/workspace/tidb --worktree-path /path/to/workspace/tidb-review --commit-ish origin/main --detach
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)