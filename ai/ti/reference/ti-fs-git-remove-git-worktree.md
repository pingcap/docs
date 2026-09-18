---
title: ti fs-git remove-git-worktree
summary: マウントされた TiDB Cloud Filesystem から、リンクされた Git worktree を削除します。
---

# ti fs-git remove-git-worktree

他の worktree で使用されている共有 Git データを保持したまま、リンクされた Git worktree を削除します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェースは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs-git remove-git-worktree
  --worktree-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--force]
  [--fs-token <string>]
  [--help]
  [--version]
```

## オプション {#options}

- `--worktree-path <string>`: リンクされた worktree のマウント済み `ti fs` パス。\[required]
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--force`: リンクされた worktree にローカル変更がある場合でも削除します。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options) を参照してください。

## 例 {#examples}

- Git worktree を削除する:

    ```bash
    # Remove a clean linked worktree.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature
    ```

- Git worktree を強制削除する:

    ```bash
    # Discard local changes only after deciding that they are no longer needed.
    ti fs-git remove-git-worktree --file-system-id <file-system-id> --worktree-path /path/to/workspace/tidb-feature --force
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem Git CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem-git.md)