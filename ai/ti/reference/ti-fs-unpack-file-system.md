---
title: ti fs unpack-file-system
summary: ローカル Filesystem オーバーレイ状態を復元します。
---

# ti fs unpack-file-system

リモートアーカイブから[ローカルオーバーレイ状態](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays)を復元します。

> **Note:**
>
> TiDB Cloud CLI (`ti`) は現在パブリックプレビューです。機能およびコマンドラインインターフェイスは、予告なく変更される場合があります。

## 構文 {#syntax}

```text
ti fs unpack-file-system
  [--archive-path <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--local-root <string>]
  [--mount-path <string>]
  [--mount-profile <string>]
  [--no-replace]
  [--remote-root <string>]
  [--version]
```

## オプション {#options}

- `--archive-path <string>`: パックされたアーカイブのパスです。
- `--dry-run`: 変更を適用せずにリクエストを検証します。
- `--file-system-id <string>`: ファイルシステムを選択します。`TI_FS_FILE_SYSTEM_ID` を設定することもできます。
- `--fs-token <string>`: Filesystem トークンを設定します。省略した場合、このコマンドは `TI_FS_TOKEN` 環境変数を使用します。どちらも指定されていない場合、このコマンドは選択した Filesystem 用にローカルに保存されているトークンを使用します。
- `--help`: ヘルプ情報を表示します。
- `--local-root <string>`: 復元先のローカルオーバーレイルートです。
- `--mount-path <string>`: ローカルのマウントパスです。
- `--mount-profile <string>`: [マウントプロファイル](/ai/ti/reference/ti-filesystem.md#mount-profiles-and-local-overlays) を選択します: `coding-agent`、`portable`、または `none`。省略した場合は `none` を使用します。
- `--no-replace`: アーカイブエントリを置き換える代わりにマージします。
- `--remote-root <string>`: `--archive-path` を省略した場合、指定したルートパス配下でパックされたアーカイブを検索します。\[default: /]
- `--version`: バージョン情報を表示します。

すべてのコマンドで共通のオプションについては、[グローバルオプション](/ai/ti/reference/ti-cli-reference.md#global-options)を参照してください。

## 例 {#examples}

- マウントされたワークスペースに展開する場合:

    ```bash
    # Restore the portable archive associated with an existing mount.
    ti fs unpack-file-system --file-system-id <file-system-id> --mount-path /path/to/workspace
    ```

- 置き換えを行わずに明示的なルートへ展開する場合:

    ```bash
    # Restore missing files while preserving existing destination entries.
    ti fs unpack-file-system --file-system-id <file-system-id> --local-root /path/to/local-root --remote-root /workspace --mount-profile portable --no-replace
    ```

## 関連ドキュメント {#related-documentation}

- [TiDB Cloud Filesystem CLI コマンドリファレンス](/ai/ti/reference/ti-filesystem.md)
